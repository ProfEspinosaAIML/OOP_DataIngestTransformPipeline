"""Pure functional transformations for validated transaction records."""

from collections.abc import Iterable, Mapping
from types import MappingProxyType

from pipeline.schema import (
    AnalyzedTransaction,
    TaxAdjustedTransaction,
    TransactionRecord,
)

REGIONAL_TAX_RATES: Mapping[str, float] = MappingProxyType(
    {
        "Northeast": 0.0825,
        "South": 0.0725,
        "Midwest": 0.0675,
        "West": 0.0875,
    }
)


def isolate_active_transactions(
    records: Iterable[TransactionRecord],
) -> list[TransactionRecord]:
    """Return active bookings without changing the input collection."""
    return list(filter(lambda record: record.is_active, records))


def adjust_regional_tax_rates(
    records: Iterable[TransactionRecord],
    regional_tax_rates: Mapping[str, float] = REGIONAL_TAX_RATES,
) -> list[TaxAdjustedTransaction]:
    """Pair each transaction with its region's rate using a new result list."""
    return [
        TaxAdjustedTransaction(
            record=record,
            regional_tax_rate=regional_tax_rates[record.region],
        )
        for record in records
    ]


def _calculate_net_margin(
    adjusted: TaxAdjustedTransaction,
) -> AnalyzedTransaction:
    tax_amount = adjusted.record.revenue * adjusted.regional_tax_rate
    return AnalyzedTransaction(
        record=adjusted.record,
        regional_tax_rate=adjusted.regional_tax_rate,
        tax_amount=tax_amount,
        net_margin=adjusted.record.revenue
        - adjusted.record.operating_cost
        - tax_amount,
    )


def compute_net_margins(
    records: Iterable[TaxAdjustedTransaction],
) -> list[AnalyzedTransaction]:
    """Calculate net margins with map; source and intermediate rows stay intact."""
    return list(map(_calculate_net_margin, records))

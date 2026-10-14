"""Immutable data models and domain values for the pipeline."""

from dataclasses import dataclass
from datetime import date

APPAREL_NAMES = frozenset(
    {"Bridal Gown", "Tuxedo", "Bridesmaid Dress", "Wedding Suit", "Accessories"}
)
SUPPORTED_REGIONS = frozenset({"Northeast", "South", "Midwest", "West"})


@dataclass(frozen=True, slots=True)
class TransactionRecord:
    """A validated wedding-related sale from one source system."""

    transaction_id: str
    venue_id: str
    transaction_date: date
    region: str
    revenue: float
    operating_cost: float
    apparel_name: str
    source: str
    is_active: bool


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """Reasons that one source row was excluded from the analysis."""

    row_number: int
    transaction_id: str
    source: str
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TaxAdjustedTransaction:
    """A transaction paired with the tax rate for its region."""

    record: TransactionRecord
    regional_tax_rate: float


@dataclass(frozen=True, slots=True)
class AnalyzedTransaction:
    """A tax-adjusted transaction with its calculated net margin."""

    record: TransactionRecord
    regional_tax_rate: float
    tax_amount: float
    net_margin: float

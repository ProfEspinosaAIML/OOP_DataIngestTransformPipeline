"""Command-line entry point for the wedding venue data pipeline."""

from pipeline.reporter import format_report
from pipeline.transformer import (
    adjust_regional_tax_rates,
    compute_net_margins,
    isolate_active_transactions,
)
from pipeline.validator import validate_records


def load_synthetic_records() -> list[dict[str, object]]:
    """Return fresh example rows from several imaginary booking systems."""
    return [
        {
            "transaction_id": "TX-1001",
            "venue_id": "VEN-01",
            "transaction_date": "2026-05-16",
            "region": "Northeast",
            "revenue": "14500.00",
            "operating_cost": "9100.00",
            "apparel_name": "Bridal Gown",
            "source": "VenueCRM",
            "is_active": True,
        },
        {
            "transaction_id": "TX-1002",
            "venue_id": "VEN-02",
            "transaction_date": "2026-06-20",
            "region": "South",
            "revenue": "21800",
            "operating_cost": "14900",
            "apparel_name": "Tuxedo",
            "source": "WeddingPortal",
            "is_active": True,
        },
        {
            "transaction_id": "TX-1003",
            "venue_id": "VEN-01",
            "transaction_date": "2026-07-04",
            "region": "Midwest",
            "revenue": "9800",
            "operating_cost": "6900",
            "apparel_name": "Bridesmaid Dress",
            "source": "PartnerPOS",
            "is_active": False,
        },
        {
            "transaction_id": "TX-1004",
            "venue_id": "VEN-03",
            "transaction_date": "2026-08-22",
            "region": "West",
            "revenue": "30200",
            "operating_cost": "22100",
            "apparel_name": "Accessories",
            "source": "VenueCRM",
            "is_active": True,
        },
        {
            "transaction_id": "TX-1005",
            "venue_id": "VEN-04",
            "transaction_date": "2026-09-12",
            "region": "Northeast",
            "revenue": "18750",
            "operating_cost": "13200",
            "apparel_name": "Wedding Suit",
            "source": "PaperBooking",
            "is_active": True,
        },
        {
            "transaction_id": "TX-1006",
            "venue_id": "VEN-02",
            "transaction_date": "2026-10-03",
            "region": "South",
            "revenue": "12500",
            "operating_cost": "8700",
            "apparel_name": "Bridal Gown",
            "source": "WeddingPortal",
            "is_active": True,
        },
        {
            "transaction_id": "TX-2001",
            "venue_id": "VEN-05",
            "transaction_date": "2026-10-10",
            "region": "West",
            "revenue": "-2500",
            "operating_cost": "800",
            "apparel_name": "Tuxedo",
            "source": "PartnerPOS",
            "is_active": True,
        },
        {
            "transaction_id": "TX-2002",
            "venue_id": "VEN-03",
            "transaction_date": "2026-02-30",
            "region": "Midwest",
            "revenue": "11400",
            "operating_cost": "7800",
            "apparel_name": "Accessories",
            "source": "PaperBooking",
            "is_active": True,
        },
        {
            "transaction_id": "TX-2003",
            "venue_id": "",
            "transaction_date": "2026-11-14",
            "region": "South",
            "revenue": "16200",
            "operating_cost": "10100",
            "apparel_name": "Wedding Suit",
            "source": "VenueCRM",
            "is_active": True,
        },
        {
            "transaction_id": "TX-2004",
            "venue_id": "VEN-06",
            "transaction_date": "2026-12-05",
            "region": "Northeast",
            "revenue": "13900",
            "operating_cost": "9200",
            "apparel_name": "Space Suit",
            "source": "WeddingPortal",
            "is_active": True,
        },
    ]


def run_pipeline() -> str:
    """Validate fresh source rows, analyze active bookings, and build a report."""
    source_records = load_synthetic_records()
    valid_records, validation_issues = validate_records(source_records)
    active_records = isolate_active_transactions(valid_records)
    tax_adjusted_records = adjust_regional_tax_rates(active_records)
    analyzed_records = compute_net_margins(tax_adjusted_records)

    return format_report(
        source_record_count=len(source_records),
        valid_records=valid_records,
        validation_issues=validation_issues,
        active_record_count=len(active_records),
        analyzed_records=analyzed_records,
    )


def main() -> None:
    """Run the example pipeline and print its terminal report."""
    print(run_pipeline())


if __name__ == "__main__":
    main()

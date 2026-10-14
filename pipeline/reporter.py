"""Summary aggregation and terminal-friendly report formatting."""

from collections.abc import Sequence

from pipeline.schema import AnalyzedTransaction, TransactionRecord, ValidationIssue


def format_report(
    source_record_count: int,
    valid_records: Sequence[TransactionRecord],
    validation_issues: Sequence[ValidationIssue],
    active_record_count: int,
    analyzed_records: Sequence[AnalyzedTransaction],
) -> str:
    """Build a report string without printing or changing pipeline data."""
    total_revenue = sum(record.record.revenue for record in analyzed_records)
    total_cost = sum(record.record.operating_cost for record in analyzed_records)
    total_tax = sum(record.tax_amount for record in analyzed_records)
    total_margin = sum(record.net_margin for record in analyzed_records)

    lines = [
        "Wedding Venue Transaction Pipeline",
        "=" * 72,
        f"Source rows: {source_record_count}",
        f"Valid rows: {len(valid_records)}",
        f"Active rows analyzed: {active_record_count}",
        f"Inactive rows skipped: {len(valid_records) - active_record_count}",
        f"Malformed rows flagged: {len(validation_issues)}",
        "",
        "Active transaction analysis",
        "-" * 72,
        (
            f"{'ID':<10} {'Venue':<9} {'Region':<10} {'Tax':>6} "
            f"{'Revenue':>11} {'Net margin':>12}"
        ),
    ]

    lines.extend(
        f"{item.record.transaction_id:<10} "
        f"{item.record.venue_id:<9} "
        f"{item.record.region:<10} "
        f"{item.regional_tax_rate:>5.2%} "
        f"${item.record.revenue:>10,.2f} "
        f"${item.net_margin:>11,.2f}"
        for item in analyzed_records
    )

    lines.extend(
        [
            "",
            "Active transaction totals",
            "-" * 72,
            f"Revenue:      ${total_revenue:,.2f}",
            f"Operating cost: ${total_cost:,.2f}",
            f"Regional tax: ${total_tax:,.2f}",
            f"Net margin:   ${total_margin:,.2f}",
            "",
            "Validation flags",
            "-" * 72,
        ]
    )

    if validation_issues:
        lines.extend(
            f"Row {issue.row_number} ({issue.transaction_id}, {issue.source}): "
            + "; ".join(issue.reasons)
            for issue in validation_issues
        )
    else:
        lines.append("No malformed rows.")

    return "\n".join(lines)

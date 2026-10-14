"""Procedural checks and type casting for records from source systems."""

from collections.abc import Iterable, Mapping
from datetime import date
import math

from pipeline.schema import (
    APPAREL_NAMES,
    SUPPORTED_REGIONS,
    TransactionRecord,
    ValidationIssue,
)


def _parse_date(value: object) -> date | None:
    try:
        return date.fromisoformat(str(value).strip())
    except (TypeError, ValueError):
        return None


def _parse_number(value: object) -> float | None:
    if isinstance(value, bool):
        return None
    if not isinstance(value, (int, float, str)):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _parse_active(value: object) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().casefold()
        if normalized in {"true", "1", "yes"}:
            return True
        if normalized in {"false", "0", "no"}:
            return False
    return None


def validate_records(
    raw_records: Iterable[Mapping[str, object]],
) -> tuple[list[TransactionRecord], list[ValidationIssue]]:
    """Cast valid rows into records and flag every row with invalid fields."""
    valid_records: list[TransactionRecord] = []
    issues: list[ValidationIssue] = []

    for row_number, raw in enumerate(raw_records, start=1):
        transaction_id = str(raw.get("transaction_id", "")).strip()
        source = str(raw.get("source", "Unknown source")).strip() or "Unknown source"
        reasons: list[str] = []

        if not transaction_id:
            reasons.append("missing transaction ID")

        venue_id = str(raw.get("venue_id", "")).strip()
        if not venue_id:
            reasons.append("missing venue ID")

        transaction_date = _parse_date(raw.get("transaction_date"))
        if transaction_date is None:
            reasons.append("invalid transaction date (expected YYYY-MM-DD)")

        region = str(raw.get("region", "")).strip().title()
        if region not in SUPPORTED_REGIONS:
            reasons.append(f"unsupported region: {region or '(missing)'}")

        revenue = _parse_number(raw.get("revenue"))
        if revenue is None:
            reasons.append("revenue must be a finite number")
        elif revenue < 0:
            reasons.append("revenue cannot be negative")

        operating_cost = _parse_number(raw.get("operating_cost"))
        if operating_cost is None:
            reasons.append("operating cost must be a finite number")
        elif operating_cost < 0:
            reasons.append("operating cost cannot be negative")

        apparel_name = str(raw.get("apparel_name", "")).strip()
        canonical_apparel = next(
            (
                allowed_name
                for allowed_name in APPAREL_NAMES
                if allowed_name.casefold() == apparel_name.casefold()
            ),
            None,
        )
        if canonical_apparel is None:
            reasons.append(f"unknown apparel name: {apparel_name or '(missing)'}")

        is_active = _parse_active(raw.get("is_active"))
        if is_active is None:
            reasons.append("active status must be a boolean")

        if reasons:
            issues.append(
                ValidationIssue(
                    row_number=row_number,
                    transaction_id=transaction_id or "(missing)",
                    source=source,
                    reasons=tuple(reasons),
                )
            )
            continue

        if (
            transaction_date is None
            or revenue is None
            or operating_cost is None
            or canonical_apparel is None
            or is_active is None
        ):
            raise RuntimeError("Validated transaction fields were unexpectedly missing")

        valid_records.append(
            TransactionRecord(
                transaction_id=transaction_id,
                venue_id=venue_id,
                transaction_date=transaction_date,
                region=region,
                revenue=revenue,
                operating_cost=operating_cost,
                apparel_name=canonical_apparel,
                source=source,
                is_active=is_active,
            )
        )

    return valid_records, issues

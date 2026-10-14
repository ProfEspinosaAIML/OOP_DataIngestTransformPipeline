# Wedding Venue Data Pre-processing Pipeline

An introductory, object-oriented Python tutorial project for first-year college
students. It demonstrates how to validate and analyze wedding-related
transaction records with a small, modular data pipeline.

The example data represents records from several imaginary booking and point-of-
sale systems. The pipeline flags malformed records, keeps valid active bookings,
applies a regional tax rate, calculates net margins, and prints a summary report.
All records are synthetic; this project does not connect to real venues or
external data sources.

## Requirements

- Python 3.10 or newer
- No third-party packages (the project uses the Python standard library only)

`requirements.txt` is included to show where project dependencies would be
listed if external packages are added later.

## Run the program

From the project root, run:

```console
python main.py
```

The script prints a report containing the number of source, valid, active, and
malformed rows; active transaction margins and totals; and the reason each
malformed row was rejected.

## Project structure

```text
OOP_DataIngestTransformPipeline/
├── main.py                 # Entry point and pipeline orchestration
├── requirements.txt        # Third-party dependencies (none currently)
└── pipeline/
    ├── __init__.py         # Package initialization
    ├── schema.py           # Immutable transaction and result data classes
    ├── validator.py        # Procedural validation and type conversion
    ├── transformer.py      # Functional filtering and calculations
    └── reporter.py         # Summary aggregation and report formatting
```

## Pipeline walkthrough

1. `main.py` creates fresh synthetic source rows with
   `load_synthetic_records()`. The rows are shaped like records from different
   imaginary systems and include both valid and malformed examples.
2. `pipeline.validator.validate_records()` checks and converts input values.
   Valid rows become `TransactionRecord` instances; invalid rows are recorded as
   `ValidationIssue` instances with their row number, source, and reasons.
3. `pipeline.transformer.isolate_active_transactions()` filters out inactive
   bookings. `adjust_regional_tax_rates()` associates each booking with its
   region's sample rate, and `compute_net_margins()` uses `map` to calculate
   results.
4. `pipeline.reporter.format_report()` aggregates the analyzed bookings and
   returns a printable report.

The data classes in `schema.py` are frozen, and the transformation functions
create new lists and result objects rather than changing source records. Each
call to `run_pipeline()` loads fresh example data, so analytical operations are
stateless and repeatable.

## Validation examples

The sample data includes a negative revenue, an impossible calendar date, a
missing venue ID, and an unsupported apparel name. The validator also checks
that transaction IDs and venue IDs are present; dates use the `YYYY-MM-DD`
format; regions and apparel names are supported; revenue and operating costs
are finite, non-negative numbers; and the active flag is a boolean or a
recognized string value.

Invalid records are flagged and excluded from analysis. Valid inactive records
are retained after validation but skipped by the active-transaction filter.

## Functional calculations

Regional tax rates are illustrative constants in
`pipeline/transformer.py`; they are for demonstrating a data transformation,
not for real tax, legal, or financial decisions.

For each valid active transaction, the example calculates:

```text
tax amount = revenue × regional tax rate
net margin = revenue − operating cost − tax amount
```

The active filter uses `filter`, net margin calculation uses `map`, and regional
tax association uses a list comprehension. These operations preserve their
inputs, making them easier to reason about and rerun.

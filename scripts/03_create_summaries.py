
import pandas as pd
from pathlib import Path

print("Starting fraud analysis summary generation...")

input_file = Path("paysim_cleaned.csv")
output_folder = Path("summaries")
output_folder.mkdir(exist_ok=True)

if not input_file.exists():
    raise FileNotFoundError("paysim_cleaned.csv was not found.")

# Read the cleaned dataset
df = pd.read_csv(input_file)

print("Dataset loaded:", df.shape)

# 1. Overall fraud summary
overall = pd.DataFrame({
    "metric": [
        "Total Transactions",
        "Fraudulent Transactions",
        "Legitimate Transactions",
        "Fraud Rate Percent",
        "Total Transaction Amount",
        "Fraudulent Transaction Amount"
    ],
    "value": [
        len(df),
        int(df["isFraud"].sum()),
        int((df["isFraud"] == 0).sum()),
        round(df["isFraud"].mean() * 100, 4),
        round(df["amount"].sum(), 2),
        round(df.loc[df["isFraud"] == 1, "amount"].sum(), 2)
    ]
})

overall.to_csv(output_folder / "overall_fraud_summary.csv", index=False)

# 2. Summary by transaction type
by_type = (
    df.groupby("type", as_index=False)
    .agg(
        total_transactions=("transaction_id", "count"),
        fraudulent_transactions=("isFraud", "sum"),
        total_amount=("amount", "sum"),
        average_amount=("amount", "mean")
    )
)

by_type["fraud_rate_percent"] = (
    by_type["fraudulent_transactions"]
    / by_type["total_transactions"] * 100
).round(4)

by_type.to_csv(output_folder / "fraud_by_type.csv", index=False)

# 3. Summary by simulation step
by_step = (
    df.groupby("step", as_index=False)
    .agg(
        total_transactions=("transaction_id", "count"),
        fraudulent_transactions=("isFraud", "sum"),
        total_amount=("amount", "sum")
    )
)

by_step["fraud_rate_percent"] = (
    by_step["fraudulent_transactions"]
    / by_step["total_transactions"] * 100
).round(4)

by_step.to_csv(output_folder / "fraud_by_step.csv", index=False)

# 4. Summary by transaction type and fraud status
by_type_status = (
    df.groupby(["type", "fraud_status"], as_index=False)
    .agg(
        total_transactions=("transaction_id", "count"),
        total_amount=("amount", "sum"),
        average_amount=("amount", "mean")
    )
)

by_type_status.to_csv(
    output_folder / "fraud_by_type_and_status.csv", index=False
)

# 5. Summary of the built-in flag
by_flag = (
    df.groupby(["flag_status", "fraud_status"], as_index=False)
    .agg(total_transactions=("transaction_id", "count"))
)

by_flag.to_csv(output_folder / "fraud_flag_summary.csv", index=False)

print("\nSummary files created:")
for file in sorted(output_folder.glob("*.csv")):
    print(f"- {file} ({file.stat().st_size / 1024:.1f} KB)")

print("\nSummary generation completed successfully.")

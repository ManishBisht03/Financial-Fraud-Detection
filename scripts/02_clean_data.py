
import pandas as pd
from pathlib import Path

print("Starting Financial Fraud Detection data preparation...")

# File paths
input_file = Path("paysim.csv")
output_file = Path.cwd() / "paysim_cleaned.csv"

# Check whether the source dataset exists
if not input_file.exists():
    raise FileNotFoundError(
        "paysim.csv was not found. "
        "Place it in the project folder."
    )

# Load the original dataset
df = pd.read_csv(input_file)

print("\nOriginal dataset shape:", df.shape)

# Check required columns
required_columns = [
    "step", "type", "amount", "nameOrig",
    "oldbalanceOrg", "newbalanceOrig", "nameDest",
    "oldbalanceDest", "newbalanceDest",
    "isFraud", "isFlaggedFraud"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# Keep the expected columns in a consistent order
df = df[required_columns].copy()

# Remove exact duplicate records, if any
duplicates_removed = int(df.duplicated().sum())
df = df.drop_duplicates().copy()

# Validate essential fields
if df[required_columns].isnull().any().any():
    raise ValueError(
        "Missing values detected. Investigate before exporting."
    )

if (df["amount"] < 0).any():
    raise ValueError(
        "Negative transaction amounts detected. Investigate first."
    )

if not df["isFraud"].isin([0, 1]).all():
    raise ValueError("Unexpected values found in isFraud.")

if not df["isFlaggedFraud"].isin([0, 1]).all():
    raise ValueError("Unexpected values found in isFlaggedFraud.")

# Create an analysis-friendly transaction identifier
df.insert(
    0,
    "transaction_id",
    range(1, len(df) + 1)
)

# Create a readable fraud label
df["fraud_status"] = df["isFraud"].map({
    0: "Legitimate",
    1: "Fraudulent"
})

# Create a readable flag label
df["flag_status"] = df["isFlaggedFraud"].map({
    0: "Not Flagged",
    1: "Flagged"
})

# Save the prepared dataset
df.to_csv(output_file, index=False)

# Report results
print("\n--- DATA PREPARATION SUMMARY ---")
print("Rows after cleaning:", len(df))
print("Columns after preparation:", len(df.columns))
print("Duplicate rows removed:", duplicates_removed)
print("Missing values:", int(df.isnull().sum().sum()))
print("Zero-value transactions retained:", int((df["amount"] == 0).sum()))
print("Fraudulent transactions:", int(df["isFraud"].sum()))
print("Legitimate transactions:", int((df["isFraud"] == 0).sum()))
print("Output file:", output_file.resolve())
print("Output file size (MB):", round(
    output_file.stat().st_size / (1024 * 1024), 2
))

print("\nData preparation completed successfully.")

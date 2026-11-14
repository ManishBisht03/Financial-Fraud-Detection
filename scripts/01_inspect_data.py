
import pandas as pd
from pathlib import Path

# Locate the dataset in the project folder
file_path = Path("paysim.csv")

# Check that the file exists
if not file_path.exists():
    print("ERROR: paysim.csv was not found in the project folder.")
else:
    print("Dataset found! Reading the data...")

    # Load the dataset
    df = pd.read_csv(file_path)

    # Display basic information
    print("\n--- DATASET OVERVIEW ---")
    print("Number of rows:", df.shape[0])
    print("Number of columns:", df.shape[1])

    print("\n--- COLUMN NAMES ---")
    print(df.columns.tolist())

    print("\n--- FIRST 5 TRANSACTIONS ---")
    print(df.head())

    print("\n--- DATA TYPES AND MISSING VALUES ---")
    df.info()


print("\n--- FRAUD DISTRIBUTION ---")

fraud_counts = df["isFraud"].value_counts().sort_index()

print("Legitimate transactions (0):", fraud_counts.get(0, 0))
print("Fraudulent transactions (1):", fraud_counts.get(1, 0))

fraud_rate = (df["isFraud"].sum() / len(df)) * 100

print(f"Fraud rate: {fraud_rate:.4f}%")


print("\n--- DATA QUALITY CHECK ---")

print("Duplicate rows:", df.duplicated().sum())
print("Missing values:", df.isnull().sum().sum())
print("Negative transaction amounts:", (df["amount"] < 0).sum())
print("Zero-value transactions:", (df["amount"] == 0).sum())

print("\n--- TRANSACTION TYPES ---")
print(df["type"].value_counts())



print("\n--- FRAUD ANALYSIS BY TRANSACTION TYPE ---")

fraud_by_type = df.groupby("type").agg(
    total_transactions=("isFraud", "size"),
    fraudulent_transactions=("isFraud", "sum"),
    total_transaction_amount=("amount", "sum")
)

fraud_by_type["fraud_rate_percent"] = (
    fraud_by_type["fraudulent_transactions"]
    / fraud_by_type["total_transactions"] * 100
)

print(fraud_by_type.round(2))



print("\n--- DETAILED FRAUD SUMMARY ---")

summary = df.groupby("type").agg(
    total_transactions=("isFraud", "size"),
    fraudulent_transactions=("isFraud", "sum"),
    total_transaction_amount=("amount", "sum")
)

summary["fraud_rate_percent"] = (
    summary["fraudulent_transactions"]
    / summary["total_transactions"] * 100
)

print(summary.to_string(
    formatters={
        "total_transaction_amount": "{:,.2f}".format,
        "fraud_rate_percent": "{:.4f}%".format
    }
))

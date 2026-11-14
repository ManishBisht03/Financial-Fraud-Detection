
import sqlite3
from pathlib import Path

database_file = Path("fraud_analysis.db")
sql_file = Path("05_fraud_analysis.sql")

if not database_file.exists():
    raise FileNotFoundError("fraud_analysis.db was not found.")

if not sql_file.exists():
    raise FileNotFoundError("05_fraud_analysis.sql was not found.")

# Read the SQL file
sql_text = sql_file.read_text(encoding="utf-8")

# Split the file into individual queries
queries = [
    query.strip()
    for query in sql_text.split(";")
    if query.strip()
]

with sqlite3.connect(database_file) as connection:
    cursor = connection.cursor()

    for number, query in enumerate(queries, start=1):
        print(f"\n{'=' * 60}")
        print(f"QUERY {number}")
        print("=" * 60)

        cursor.execute(query)

        # Display column names
        if cursor.description:
            column_names = [
                description[0]
                for description in cursor.description
            ]
            print(" | ".join(column_names))
            print("-" * 60)

            rows = cursor.fetchall()

            for row in rows:
                print(" | ".join(str(value) for value in row))

            print(f"\nRows returned: {len(rows)}")
        else:
            print("Query executed successfully.")

print("\nAll SQL queries executed successfully.")

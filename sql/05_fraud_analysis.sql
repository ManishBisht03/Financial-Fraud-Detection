
-- Query 1: Overall fraud and legitimate transaction counts
SELECT
    metric,
    value
FROM overall_fraud_summary;


-- Query 2: Compare fraud risk across transaction types
SELECT
    type,
    total_transactions,
    fraudulent_transactions,
    ROUND(fraud_rate_percent, 4) AS fraud_rate_percent,
    ROUND(average_amount, 2) AS average_transaction_amount
FROM fraud_by_type
ORDER BY fraud_rate_percent DESC;


-- Query 3: Find transaction types with the most fraud cases
SELECT
    type,
    fraudulent_transactions,
    total_transactions
FROM fraud_by_type
ORDER BY fraudulent_transactions DESC;


-- Query 4: Find the simulation steps with the highest fraud rates
SELECT
    step,
    total_transactions,
    fraudulent_transactions,
    fraud_rate_percent
FROM fraud_by_step
WHERE fraudulent_transactions > 0
ORDER BY fraud_rate_percent DESC
LIMIT 10;


-- Query 5: Compare the built-in flag with actual fraud labels
SELECT
    flag_status,
    fraud_status,
    total_transactions
FROM fraud_flag_summary
ORDER BY flag_status, fraud_status;

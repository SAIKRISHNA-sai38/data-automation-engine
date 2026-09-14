import pandas as pd
import numpy as np


def process_products(products):

    # Convert input data into DataFrame
    df = pd.DataFrame(products)

    # Check if data exists
    if df.empty:
        raise ValueError("No data available for processing.")

    # Check required columns
    required_columns = ["name", "price"]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required column(s): {', '.join(missing_columns)}"
        )

    # Count original records
    total_records = len(df)

    # Remove rows with missing product names
    df["name"] = df["name"].astype(str).str.strip()

    df = df[df["name"] != ""]

    # Clean price values
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    # Convert prices to numbers
    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    # Remove invalid prices
    df = df.dropna(subset=["price"])

    # Count valid records
    valid_records = len(df)

    # Calculate invalid records
    invalid_records = total_records - valid_records

    # Handle case where every record is invalid
    if df.empty:
        raise ValueError(
            "No valid product records found after data cleaning."
        )

    # Calculate statistics
    average_price = np.mean(df["price"])
    highest_price = np.max(df["price"])
    lowest_price = np.min(df["price"])

    return (
        df,
        average_price,
        highest_price,
        lowest_price,
        total_records,
        valid_records,
        invalid_records
    )
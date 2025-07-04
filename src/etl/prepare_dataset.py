"""
ETL script for processing campaign, lead, and inscription data.

This script loads data from local JSON files, cleans and enriches the dataset,
detects anomalies in conversion records, and uploads the sanitized data to MongoDB.
"""

import pandas as pd
import numpy as np
from upload_to_mongo import upload_dataframe_to_mongo


def parse_currency(euro_str):
    """
    Convert a European-style currency string to a float.

    Handles currency strings such as "€1.234,56" and returns 1234.56.

    Args:
        euro_str (str): The currency string.

    Returns:
        float or np.nan: Parsed float value or NaN if input is null.
    """
    if pd.isna(euro_str):
        return np.nan
    return float(
        euro_str
        .replace("€", "")
        .replace("\xa0", "")
        .replace(".", "")
        .replace(",", ".")
        .strip()
    )


def load_data():
    """
    Load campaign, lead, and inscription data from JSON files.

    Returns:
        tuple: Three pandas DataFrames: (campaigns, leads, inscriptions)
    """
    campaigns = pd.read_json("data/campaigns.json")
    leads = pd.read_json("data/leads.json")
    inscriptions = pd.read_json("data/inscriptions.json")
    return campaigns, leads, inscriptions


def sanitize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sanitizes a DataFrame for MongoDB insertion:
    - Converts datetime64 columns to native Python datetime or None
    - Replaces NaN/NaT with None for other data types

    Args:
        df (pd.DataFrame): Input DataFrame to sanitize.

    Returns:
        pd.DataFrame: A sanitized copy of the original DataFrame.
    """
    df_sanitized = df.copy()

    # Process datetime columns
    datetime_cols = df_sanitized.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns
    for col in datetime_cols:
        df_sanitized[col] = df_sanitized[col].astype(object).where(df_sanitized[col].notnull(), None)

    # Replace other NaNs with None
    df_sanitized = df_sanitized.where(pd.notnull(df_sanitized), None)

    return df_sanitized


def detect_anomaly(row):
    """
    Detects the type of anomaly in a conversion record.

    Rules:
        - If inscription_created_at is missing and marked as converted → 'MISSING_INSCRIPTION_DATE'
        - If inscription is before lead → 'NEGATIVE_CONVERSION_TIME'
        - Otherwise → 'NO_ANOMALY'

    Args:
        row (pd.Series): A row from the merged dataset.

    Returns:
        str: Anomaly type.
    """
    if row["converted"] and pd.isna(row["inscription_created_at"]):
        return "MISSING_INSCRIPTION_DATE"
    if row["converted"] and row["conversion_time_days"] < 0:
        return "NEGATIVE_CONVERSION_TIME"
    return "NO_ANOMALY"


def prepare_dataset(campaigns, leads, inscriptions):
    """
    Merge, clean, and enrich campaign, lead, and inscription datasets.

    - Merges leads with campaigns using input_channel (not renaming to campaign_id).
    - Converts date fields.
    - Parses currency fields into float.
    - Calculates conversion time.
    - Flags valid conversions.
    - Detects anomalies.

    Args:
        campaigns (pd.DataFrame): Campaign metadata.
        leads (pd.DataFrame): Lead information.
        inscriptions (pd.DataFrame): Enrollment records.

    Returns:
        pd.DataFrame: Merged and enriched dataset ready for analysis.
    """
    # Merge leads with campaigns using input_channel
    leads_campaigns = leads.merge(campaigns, left_on="input_channel", right_on="campaign_id", how="left")

    # Merge with inscriptions (join on lead_id)
    df = leads_campaigns.merge(
        inscriptions,
        on="lead_id",
        how="left",
        suffixes=('', '_insc')
    )

    # Convert datetime fields
    df["lead_created_at"] = pd.to_datetime(df["created_at"])
    df["inscription_created_at"] = pd.to_datetime(df["created_at_insc"])

    # Convert monetary fields
    df["cost_float"] = df["cost"].apply(parse_currency)
    df["amount_float"] = df["amount"].apply(parse_currency)

    # Calculate time to convert
    df["conversion_time_days"] = (
        df["inscription_created_at"] - df["lead_created_at"]
    ).dt.days

    # Flag: converted if there is an inscription
    df["converted"] = ~df["inscription_created_at"].isna()

    # Flag: valid conversion (i.e., inscription not before lead)
    df["conversion_valid"] = df["conversion_time_days"] >= 0

    # Label anomaly types
    df["conversion_anomaly_type"] = df.apply(detect_anomaly, axis=1)

    return df


if __name__ == "__main__":
    # Load data from JSON files
    campaigns_df, leads_df, inscriptions_df = load_data()
    # Prepare the merged dataset
    merged_df = prepare_dataset(campaigns_df, leads_df, inscriptions_df)
    # Sanitize DataFrame (convert datetime, replace NaN with None)
    merged_df = sanitize_dataframe(merged_df)
    # Upload to MongoDB using external module
    upload_dataframe_to_mongo(merged_df)
    print("ETL completed and data uploaded to MongoDB Atlas")
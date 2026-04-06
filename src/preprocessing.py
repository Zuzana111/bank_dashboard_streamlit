from __future__ import annotations

import pandas as pd


def clean_client_data(client_df: pd.DataFrame) -> pd.DataFrame:
    """Fill simple missing values in the client table."""
    df = client_df.copy()
    df["job"] = df["job"].fillna("unknown")
    df["age"] = df["age"].fillna(df["age"].median())
    return df


def clean_client_products(client_products_df: pd.DataFrame) -> pd.DataFrame:
    """Normalize product flags to lowercase yes/no values."""
    df = client_products_df.copy()
    replacements = {"y": "yes", "n": "no"}
    for column in ["has_deposits", "loan", "has_insurance", "has_mortgage"]:
        df[column] = (
            df[column]
            .fillna("unknown")
            .astype(str)
            .str.strip()
            .str.lower()
            .replace(replacements)
        )
    return df


def add_age_bands(df: pd.DataFrame) -> pd.DataFrame:
    """Create readable age buckets for charts."""
    result = df.copy()
    bins = [17, 29, 39, 49, 59, 69, 100]
    labels = ["18-29", "30-39", "40-49", "50-59", "60-69", "70+"]
    result["age_band"] = pd.cut(result["age"], bins=bins, labels=labels)
    return result


def compare_segment_mix(
    overall_df: pd.DataFrame,
    selected_df: pd.DataFrame,
    column: str,
    top_n: int = 8,
) -> pd.DataFrame:
    """Compare segment share in the full base against the selected clients."""
    overall = (
        overall_df[column]
        .fillna("unknown")
        .value_counts(normalize=True)
        .rename("overall_share")
    )
    selected = (
        selected_df[column]
        .fillna("unknown")
        .value_counts(normalize=True)
        .rename("selected_share")
    )
    comparison = pd.concat([overall, selected], axis=1).fillna(0).reset_index()
    comparison = comparison.rename(columns={"index": column})
    comparison["share_lift"] = comparison["selected_share"] - comparison["overall_share"]
    return comparison.sort_values("selected_share", ascending=False).head(top_n)


def campaign_success_by_segment(
    first_round_df: pd.DataFrame,
    column: str,
    min_count: int = 20,
) -> pd.DataFrame:
    """Compute campaign volume and success rate by segment."""
    grouped = (
        first_round_df.groupby(column, dropna=False)
        .agg(
            clients=("client_id", "nunique"),
            success_rate=("invested", "mean"),
            avg_balance=("mean_balance", "mean"),
        )
        .reset_index()
    )
    grouped[column] = grouped[column].fillna("unknown")
    grouped = grouped[grouped["clients"] >= min_count]
    return grouped.sort_values("success_rate", ascending=False)

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pandas as pd


MAIN_TABLES = ["client", "client_products", "balances", "inv_campaign_eval"]


def load_table(db_path: str, table_name: str) -> pd.DataFrame:
    """Load a single table from SQLite into a DataFrame."""
    query = f"SELECT * FROM {table_name}"
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)


def list_tables(db_path: str) -> list[str]:
    """Return all table names in the SQLite database."""
    with sqlite3.connect(db_path) as conn:
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        tables = pd.read_sql_query(query, conn)
    return tables["name"].tolist()


def load_all_tables(
    db_path: str,
    tables: list[str] | None = None,
) -> dict[str, pd.DataFrame]:
    """Load the main SQLite tables needed by the artifact builder."""
    selected_tables = tables or MAIN_TABLES
    return {table: load_table(db_path, table) for table in selected_tables}


def load_dashboard_artifacts(artifacts_dir: str | Path) -> dict[str, object]:
    """Load all dashboard artifacts written by the build script."""
    artifacts_path = Path(artifacts_dir)
    required_files = {
        "client_base": artifacts_path / "client_base.csv",
        "first_round": artifacts_path / "first_round_clients.csv",
        "eligible_clients": artifacts_path / "scored_eligible_clients.csv",
        "selected_clients": artifacts_path / "selected_clients.csv",
        "model_results": artifacts_path / "model_comparison.csv",
        "roc_curve": artifacts_path / "roc_curve.csv",
        "feature_importance": artifacts_path / "feature_importance.csv",
        "overview_metrics": artifacts_path / "overview_metrics.json",
        "metadata": artifacts_path / "metadata.json",
    }

    missing = [str(path) for path in required_files.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing dashboard artifacts in the published `artifacts/` folder. "
            f"Missing: {missing}"
        )

    with open(required_files["overview_metrics"], "r", encoding="utf-8") as handle:
        overview_metrics = json.load(handle)
    with open(required_files["metadata"], "r", encoding="utf-8") as handle:
        metadata = json.load(handle)

    assets = {
        "client_base": pd.read_csv(required_files["client_base"]),
        "first_round": pd.read_csv(required_files["first_round"]),
        "eligible_clients": pd.read_csv(required_files["eligible_clients"]),
        "selected_clients": pd.read_csv(required_files["selected_clients"]),
        "model_results": pd.read_csv(required_files["model_results"]),
        "roc_curve": pd.read_csv(required_files["roc_curve"]),
        "feature_importance": pd.read_csv(required_files["feature_importance"]),
        "overview_metrics": overview_metrics,
        "metadata": metadata,
        "best_model_name": overview_metrics["best_model_by_roc_auc"],
        "selected_model_name": overview_metrics["selected_model_name"],
        "train_rows": overview_metrics["train_rows"],
        "test_rows": overview_metrics["test_rows"],
    }
    return assets

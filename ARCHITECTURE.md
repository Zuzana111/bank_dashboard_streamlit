# Dashboard Architecture

## Separation of concerns

- `master_notebook.ipynb`
  Experimentation, feature selection, model comparison, and final model choice.
- `app.py`
  Streamlit presentation layer only. It reads saved files from `artifacts/` and renders the dashboard.
- `src/data_loader.py`
  Small loading helpers for artifacts and source tables.
- `src/preprocessing.py`
  Lightweight cleaning and chart-preparation helpers used by the app.

## Published app structure

The published repository is intentionally artifact-based. The app loads precomputed files from `artifacts/`:

- `overview_metrics.json`
- `model_comparison.csv`
- `roc_curve.csv`
- `feature_importance.csv`
- `selected_clients.csv`
- `scored_eligible_clients.csv`
- `client_base.csv`
- `first_round_clients.csv`
- `metadata.json`

## Source of truth

- Selected deployment model: `Logistic Regression`
- Best model by test ROC AUC: tracked separately in the saved metrics
- Second-round ranking and top-3000 selection: saved in the published artifact files
- Realized second-round outcomes: reflected in the saved overview metrics

## Why this structure

- The Streamlit app loads quickly and does not retrain models on page load.
- Dashboard numbers stay consistent with the notebook story.
- The GitHub repo is self-contained for portfolio review and deployment.

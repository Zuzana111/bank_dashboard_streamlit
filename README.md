# Bank Investment Campaign Dashboard

Streamlit dashboard for a bank investment campaign case study.  
The project analyzes first-round campaign results, compares classification models, and presents a notebook-aligned targeting strategy for selecting the top 3,000 clients for a second-round campaign.

## Features

- Overview of campaign KPIs and business impact
- Customer profile view for the selected target group
- Model comparison and ROC curve visualization
- Artifact-based architecture to keep Streamlit aligned with notebook outputs

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## Project Structure

- `app.py` – Streamlit presentation layer
- `artifacts/` – saved dashboard inputs
- `src/data_loader.py` – artifact loading utilities
- `src/preprocessing.py` – helper functions for dashboard analysis

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import load_dashboard_artifacts
from src.preprocessing import (
    compare_segment_mix,
)


ARTIFACTS_DIR = Path(__file__).parent / "artifacts"
PAGES = ["Overview", "Customer Profile", "Model Results"]


st.set_page_config(
    page_title="Bank Investment Campaign Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def get_dashboard_assets() -> dict[str, object]:
    return load_dashboard_artifacts(ARTIFACTS_DIR)


def format_int(value: float | int) -> str:
    return f"{int(round(value)):,}"


def format_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def format_czk(value: float) -> str:
    return f"{value:,.0f} CZK"


def render_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    *,
    title: str,
    color: str | None = None,
    height: int | None = None,
) -> None:
    st.markdown(f"**{title}**")
    chart = data.copy()
    chart_kwargs = {"use_container_width": True}
    if height is not None:
        chart_kwargs["height"] = height
    if color:
        pivoted = chart.pivot(index=x, columns=color, values=y).fillna(0)
        st.bar_chart(pivoted, **chart_kwargs)
    else:
        st.bar_chart(chart.set_index(x)[y], **chart_kwargs)


def render_line_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    *,
    title: str,
    color: str | None = None,
) -> None:
    st.markdown(f"**{title}**")
    chart = data.copy()
    if color:
        pivoted = chart.pivot_table(index=x, columns=color, values=y, aggfunc="mean")
        st.line_chart(pivoted, use_container_width=True)
    else:
        st.line_chart(chart.set_index(x)[y], use_container_width=True)


def apply_custom_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background:
                    radial-gradient(circle at top right, rgba(14, 116, 144, 0.08), transparent 26%),
                    linear-gradient(180deg, #f3f6fa 0%, #eef3f8 100%);
                color: #0f172a;
            }

            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #0f172a 0%, #172554 100%);
                border-right: 1px solid rgba(255, 255, 255, 0.06);
            }

            section[data-testid="stSidebar"] * {
                color: #e2e8f0 !important;
            }

            .block-container {
                padding-top: 2rem;
                padding-bottom: 2.75rem;
                max-width: 1180px;
            }

            .hero-card {
                background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 20px;
                padding: 2.1rem 2.2rem;
                box-shadow: 0 20px 50px rgba(15, 23, 42, 0.14);
                color: #f8fafc;
                margin-bottom: 1.25rem;
            }

            .eyebrow {
                text-transform: uppercase;
                letter-spacing: 0.14em;
                font-size: 0.72rem;
                font-weight: 700;
                color: #bfdbfe;
                margin-bottom: 0.75rem;
            }

            .hero-title {
                font-size: 2.35rem;
                font-weight: 800;
                line-height: 1.1;
                margin-bottom: 0.8rem;
                max-width: 720px;
            }

            .hero-text {
                font-size: 1rem;
                line-height: 1.65;
                max-width: 760px;
                color: rgba(248, 250, 252, 0.88);
                margin-bottom: 0;
            }

            .section-card {
                background: rgba(255, 255, 255, 0.94);
                border: 1px solid #dbe4ee;
                border-radius: 18px;
                padding: 1.35rem 1.4rem;
                box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
                height: 100%;
            }

            .section-label {
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #2563eb;
                margin-bottom: 0.55rem;
            }

            .section-title {
                font-size: 1rem;
                font-weight: 800;
                color: #0f172a;
                margin-bottom: 0.5rem;
            }

            .section-text {
                color: #475569;
                line-height: 1.68;
                font-size: 0.96rem;
                margin-bottom: 0;
            }

            .divider-title {
                font-size: 1.05rem;
                font-weight: 800;
                color: #0f172a;
                margin: 1.5rem 0 0.85rem 0;
            }

            div[data-testid="stMetric"] {
                background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
                border: 1px solid #d9e3ef;
                border-radius: 18px;
                padding: 1.05rem 1rem 0.95rem 1rem;
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
                color: #0f172a !important;
            }

            div[data-testid="stMetricLabel"] {
                font-weight: 700;
                font-size: 0.82rem;
            }

            div[data-testid="stMetric"] *,
            div[data-testid="stMetricLabel"] p,
            div[data-testid="stMetricLabel"] label,
            div[data-testid="stMetricLabel"] span {
                color: #64748b !important;
            }

            div[data-testid="stMetricValue"] {
                font-weight: 800;
                font-size: 1.45rem;
            }

            div[data-testid="stMetricValue"] *,
            div[data-testid="stMetricValue"] p,
            div[data-testid="stMetricValue"] span {
                color: #0f172a !important;
                line-height: 1.15;
            }

            [data-testid="metric-container"] {
                color: #0f172a !important;
            }

            [data-testid="metric-container"] * {
                color: inherit !important;
            }

            .note-card {
                background: linear-gradient(90deg, #eaf2ff 0%, #f4f8fc 100%);
                border: 1px solid #cfe0f5;
                border-radius: 18px;
                padding: 1.25rem 1.4rem;
                margin-top: 1rem;
                box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
            }

            .note-text {
                color: #334155;
                line-height: 1.7;
                margin: 0;
                font-size: 0.97rem;
            }

            .impact-strip {
                background: linear-gradient(90deg, #fef3c7 0%, #fde68a 100%);
                border: 1px solid #f5d46b;
                border-radius: 18px;
                padding: 1.2rem 1.4rem;
                margin-top: 1rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 10px 24px rgba(161, 98, 7, 0.10);
            }

            .impact-strip-title {
                color: #92400e;
                font-size: 0.76rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.4rem;
            }

            .impact-strip-text {
                color: #78350f;
                font-size: 1.08rem;
                line-height: 1.55;
                margin: 0;
            }

            .impact-number {
                font-size: 1.32rem;
                font-weight: 800;
                color: #92400e;
                white-space: nowrap;
            }

            div[data-baseweb="select"] > div {
                background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%) !important;
                border: 1px solid #c7d4e3 !important;
                border-radius: 12px !important;
                box-shadow: 0 6px 16px rgba(15, 23, 42, 0.08) !important;
            }

            div[data-baseweb="select"] > div:hover {
                background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%) !important;
                border-color: #94a3b8 !important;
                box-shadow: 0 8px 18px rgba(15, 23, 42, 0.10) !important;
            }

            div[data-baseweb="select"] > div:focus-within {
                background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%) !important;
                border-color: #2563eb !important;
                box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.14) !important;
            }

            div[data-baseweb="select"] *,
            div[data-baseweb="select"] span,
            div[data-baseweb="select"] input,
            div[data-baseweb="select"] div {
                background: transparent !important;
                color: #0f172a !important;
                font-weight: 600 !important;
            }

            div[data-baseweb="select"] input::placeholder {
                color: #475569 !important;
                opacity: 1 !important;
            }

            div[data-baseweb="select"] svg {
                fill: #334155 !important;
                color: #334155 !important;
            }

            div[role="listbox"],
            ul[role="listbox"],
            ul[data-baseweb="menu"] {
                background: #ffffff !important;
                color: #0f172a !important;
                border: 1px solid #cbd5e1 !important;
                border-radius: 12px !important;
                box-shadow: 0 12px 28px rgba(15, 23, 42, 0.12) !important;
            }

            div[role="option"],
            li[role="option"],
            ul[data-baseweb="menu"] li {
                background: #ffffff !important;
                color: #0f172a !important;
            }

            div[role="option"]:hover,
            li[role="option"]:hover,
            ul[data-baseweb="menu"] li:hover {
                background: #eff6ff !important;
                color: #0f172a !important;
            }

            label[data-testid="stWidgetLabel"] p {
                color: #334155;
                font-weight: 700;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title: str, description: str, eyebrow: str) -> None:
    description_html = (
        f'<p class="hero-text">{description}</p>' if description.strip() else ""
    )
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="eyebrow">{eyebrow}</div>
            <div class="hero-title">{title}</div>
            {description_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_card(label: str, title: str, text: str) -> None:
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-label">{label}</div>
            <div class="section-title">{title}</div>
            <p class="section-text">{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview_page(assets: dict[str, object]) -> None:
    metrics = assets["overview_metrics"]

    render_hero(
        title="Bank Investment Campaign Dashboard",
        eyebrow="Investment Targeting Case Study",
        description="",
    )

    render_section_card(
        "Objective",
        "Project Goal",
        (
            "The objective was to improve campaign efficiency by identifying clients with the highest likelihood of investing "
            "in the second campaign round. Using first-round campaign outcomes as the decision basis, clients were ranked by "
            "predicted probability of investment and the top 3,000 were selected for targeted outreach."
        ),
    )

    st.markdown('<div class="divider-title">Key Performance Indicators</div>', unsafe_allow_html=True)
    row_one = st.columns(3, gap="large")
    row_one[0].metric("Total Clients", format_int(metrics["total_clients"]))
    row_one[1].metric(
        "Clients Selected for Campaign",
        format_int(metrics["selected_clients"]),
    )
    row_one[2].metric(
        "Data-Driven Solution Predicted",
        format_pct(metrics["data_driven_solution_predicted"]),
    )

    row_two = st.columns(3, gap="large")
    row_two[0].metric(
        "Model Based Investment",
        format_czk(metrics["model_based_investment_czk"]),
    )
    row_two[1].metric(
        "Random Selection Investment",
        format_czk(metrics["random_selection_investment_czk"]),
    )
    row_two[2].metric(
        "Potential Increase In Clients' Investments",
        format_czk(metrics["potential_increase_czk"]),
    )

    st.markdown(
        f"""
        <div class="impact-strip">
            <div class="impact-strip-title">Business Impact</div>
            <p class="impact-strip-text">
                Using the data-driven targeting approach could increase client investments by
                <span class="impact-number">{format_czk(metrics['potential_increase_czk'])}</span>
                compared with random campaign selection.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_section_card(
        "Method",
        "Model Summary",
        (
            "Four classifiers were compared on the first-round client set. AdaBoost achieved the highest test ROC AUC, "
            "but Logistic Regression was chosen for deployment because it balanced strong performance with simplicity "
            "and interpretability. It was used to rank the second-round pool and select the top 3,000 clients."
        ),
    )

    st.markdown(
        """
        <div class="note-card">
            <div class="section-title">Assumption Used In The App</div>
            <p class="note-text">
                The Streamlit app does not retrain models on page load. Notebook-exported model artifacts are treated as
                the source of truth for model comparison, selected-client ranking, and second-round KPI reporting.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_customer_profile_page(assets: dict[str, object]) -> None:
    client_base = assets["client_base"].copy()
    selected = assets["selected_clients"].copy()

    render_hero(
        title="Customer Profile",
        eyebrow="Selection Profile",
        description="Selected campaign target group.",
    )

    top_job = selected["job"].mode().iloc[0]
    top_education = selected["education"].mode().iloc[0]

    metric_cols = st.columns(3, gap="large")
    metric_cols[0].metric("Median Age", f"{selected['age'].median():.0f}")
    metric_cols[1].metric("Most Common Occupation", top_job.title())
    metric_cols[2].metric("Top Education Level", top_education.title())

    st.markdown('<div class="divider-title">Segment Mix</div>', unsafe_allow_html=True)
    segment = st.selectbox(
        "Select customer attribute",
        ["job", "education", "marital", "gender", "currency"],
    )
    segment_titles = {
        "job": "Occupation",
        "education": "Education",
        "marital": "Marital Status",
        "gender": "Gender",
        "currency": "Currency",
    }
    segment_mix = compare_segment_mix(client_base, selected, segment, top_n=10)
    segment_chart = segment_mix.melt(
        id_vars=[segment],
        value_vars=["overall_share", "selected_share"],
        var_name="population",
        value_name="share",
    )
    segment_chart["population"] = segment_chart["population"].map(
        {"overall_share": "Full client base", "selected_share": "Selected top 3,000"}
    )

    render_bar_chart(
        segment_chart,
        x=segment,
        y="share",
        color="population",
        title=segment_titles[segment],
        height=420,
    )

    st.markdown('<div class="divider-title">Top Ranked Clients</div>', unsafe_allow_html=True)
    table = selected[
        [
            "client_id",
            "predicted_probability",
            "age",
            "job",
            "education",
            "gender",
            "has_deposits",
            "has_mortgage",
            "mean_balance",
            "currency",
        ]
    ].head(20)
    table["predicted_probability"] = table["predicted_probability"] * 100
    st.dataframe(
        table.rename(
            columns={
                "client_id": "Client ID",
                "predicted_probability": "Predicted investment probability",
                "age": "Age",
                "job": "Job",
                "education": "Education",
                "gender": "Gender",
                "has_deposits": "Deposits",
                "has_mortgage": "Mortgage",
                "mean_balance": "Mean balance",
                "currency": "Currency",
            }
        ),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Predicted investment probability": st.column_config.NumberColumn(format="%.1f%%"),
            "Mean balance": st.column_config.NumberColumn(format="%.2f"),
        },
    )


def render_model_results_page(assets: dict[str, object]) -> None:
    model_results = assets["model_results"].copy()
    roc_curve = assets["roc_curve"].copy()
    feature_importance = assets["feature_importance"].copy()
    overview_metrics = assets["overview_metrics"]

    render_hero(
        title="Model Results",
        eyebrow="Training And Ranking",
        description="",
    )

    best_model_row = model_results.sort_values("roc_auc", ascending=False).iloc[0]
    selected_model_row = model_results.loc[
        model_results["model"] == assets["selected_model_name"]
    ].iloc[0]
    metric_cols = st.columns(4, gap="small")
    metric_cols[0].metric("Selected Model", assets["selected_model_name"])
    metric_cols[1].metric("Selected Model ROC AUC", f"{selected_model_row['roc_auc']:.3f}")
    metric_cols[2].metric("Best ROC AUC Model", best_model_row["model"])
    metric_cols[3].metric("Realized Investors", format_int(overview_metrics["actual_successes"]))

    st.markdown('<div class="divider-title">Model Comparison</div>', unsafe_allow_html=True)
    st.dataframe(
        model_results[
            ["model", "accuracy", "f1", "roc_auc", "average_precision"]
        ].rename(
            columns={
                "model": "Model",
                "accuracy": "Accuracy",
                "f1": "F1 Score",
                "roc_auc": "AUC-ROC",
                "average_precision": "Average Precision",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    roc_col, importance_col = st.columns(2, gap="large")
    with roc_col:
        roc_curve_chart = roc_curve.copy()
        roc_curve_chart["model"] = roc_curve_chart["model"].replace(
            {
                "Random Forest": "Random Forest",
                "Logistic Regression": "Logistic Regression",
                "Neural Network": "Neural Network",
            }
        )
        roc_auc_lookup = (
            model_results.set_index("model")["roc_auc"].to_dict()
        )
        roc_order = ["Random Forest", "Logistic Regression", "KNN", "AdaBoost", "Neural Network"]
        roc_colors = {
            "Random Forest": "#ff2d2d",
            "Logistic Regression": "#39ff14",
            "KNN": "#00e5ff",
            "AdaBoost": "#ff00ff",
            "Neural Network": "#ffe600",
        }
        fig = px.line(
            roc_curve_chart,
            x="fpr",
            y="tpr",
            color="model",
            category_orders={"model": roc_order},
            color_discrete_map=roc_colors,
            template="plotly_white",
        )
        for trace in fig.data:
            model_name = trace.name
            auc_value = roc_auc_lookup.get(model_name)
            if auc_value is not None:
                trace.name = f"{model_name} (AUC = {auc_value:.3f})"
            trace.line.width = 2.2

        fig.add_scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            name="Random",
            line=dict(color="#9ca3af", width=2, dash="dash"),
        )
        fig.update_layout(
            title="ROC Curve on test data",
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            font=dict(color="#0f172a"),
            xaxis=dict(
                title="False Positive Rate",
                color="#0f172a",
                gridcolor="rgba(15,23,42,0.08)",
                zeroline=False,
            ),
            yaxis=dict(
                title="True Positive Rate",
                color="#0f172a",
                gridcolor="rgba(15,23,42,0.08)",
                zeroline=False,
            ),
            legend=dict(
                title="",
                bgcolor="rgba(255,255,255,0.92)",
                bordercolor="rgba(148,163,184,0.8)",
                borderwidth=1,
                yanchor="bottom",
                y=0.02,
                xanchor="right",
                x=0.98,
            ),
            margin=dict(l=10, r=10, t=48, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    with importance_col:
        if feature_importance.empty:
            st.info("Feature importance is not available for the selected model.")
        else:
            st.markdown("**Feature Importance**")
            importance_chart = feature_importance.sort_values("importance", ascending=False).copy()
            fig = px.bar(
                importance_chart,
                x="importance",
                y="feature",
                orientation="h",
                text="importance",
                color="importance",
                color_continuous_scale=[
                    [0.0, "#c7d2fe"],
                    [0.45, "#60a5fa"],
                    [1.0, "#1d4ed8"],
                ],
                template="plotly_white",
            )
            fig.update_traces(
                texttemplate="%{text:.3f}",
                textposition="outside",
                marker_line_width=0,
            )
            fig.update_layout(
                xaxis_title="Importance",
                yaxis_title="",
                coloraxis_showscale=False,
                margin=dict(l=0, r=10, t=10, b=0),
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                yaxis=dict(categoryorder="total ascending"),
            )
            st.plotly_chart(
                fig,
                use_container_width=True,
            )


def main() -> None:
    apply_custom_styles()
    try:
        assets = get_dashboard_assets()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.stop()

    st.sidebar.markdown("## Dashboard Sections")
    page = st.sidebar.radio("Go to", PAGES, label_visibility="collapsed")

    if page == "Overview":
        render_overview_page(assets)
    elif page == "Customer Profile":
        render_customer_profile_page(assets)
    else:
        render_model_results_page(assets)


if __name__ == "__main__":
    main()

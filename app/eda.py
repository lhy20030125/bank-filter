import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app.data_loader import NUMERIC_COLS


def show_overview(df: pd.DataFrame):
    """Show dataset overview: shape, dtypes, missing values."""
    col1, col2, col3 = st.columns(3)
    col1.metric("样本数", f"{len(df):,}")
    col2.metric("特征数", f"{len(df.columns)}")
    col3.metric("目标变量", "subscribe")

    st.subheader("字段信息")
    info_df = pd.DataFrame(
        {
            "字段": df.columns,
            "类型": df.dtypes.astype(str).values,
            "非空数": df.notna().sum().values,
            "缺失数": df.isna().sum().values,
            "唯一值": [df[c].nunique() for c in df.columns],
        }
    )
    st.dataframe(info_df, use_container_width=True, hide_index=True)


def show_target_distribution(df: pd.DataFrame):
    """Show target variable distribution."""
    st.subheader("目标变量分布")
    counts = df["subscribe"].value_counts().reset_index()
    counts.columns = ["subscribe", "count"]
    fig = px.pie(counts, names="subscribe", values="count", title="认购分布 (yes/no)")
    fig.update_traces(textinfo="percent+value")
    st.plotly_chart(fig, use_container_width=True)


def show_numeric_distribution(df: pd.DataFrame, col: str):
    """Show histogram for a numeric column, split by target."""
    fig = px.histogram(
        df,
        x=col,
        color="subscribe",
        barmode="overlay",
        opacity=0.7,
        title=f"{col} 分布 (按 subscribe)",
        color_discrete_map={"yes": "#2ecc71", "no": "#e74c3c"},
    )
    st.plotly_chart(fig, use_container_width=True)


def show_categorical_distribution(df: pd.DataFrame, col: str):
    """Show bar chart for a categorical column, split by target."""
    grouped = df.groupby([col, "subscribe"]).size().reset_index(name="count")
    fig = px.bar(
        grouped,
        x=col,
        y="count",
        color="subscribe",
        barmode="group",
        title=f"{col} 分布 (按 subscribe)",
        color_discrete_map={"yes": "#2ecc71", "no": "#e74c3c"},
    )
    st.plotly_chart(fig, use_container_width=True)


def show_subscribe_rate_by_category(df: pd.DataFrame, col: str):
    """Show subscription rate grouped by a categorical column."""
    rate = df.groupby(col)["subscribe"].apply(lambda x: (x == "yes").mean()).reset_index()
    rate.columns = [col, "subscribe_rate"]
    fig = px.bar(
        rate,
        x=col,
        y="subscribe_rate",
        title=f"各 {col} 的认购率",
        text_auto=".1%",
        color="subscribe_rate",
        color_continuous_scale="RdYlGn",
    )
    fig.update_layout(yaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)


def show_correlation_heatmap(df: pd.DataFrame):
    """Show correlation heatmap for numeric features."""
    numeric_df = df[NUMERIC_COLS + ["subscribe"]].copy()
    numeric_df["subscribe"] = numeric_df["subscribe"].map({"yes": 1, "no": 0})
    corr = numeric_df.corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale="RdBu_r",
            zmin=-1,
            zmax=1,
            text=corr.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 10},
        )
    )
    fig.update_layout(title="数值特征相关性热力图", width=700, height=600)
    st.plotly_chart(fig, use_container_width=True)

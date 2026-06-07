import streamlit as st

from app.config import TRAIN_CSV
from app.data_loader import CATEGORICAL_COLS, NUMERIC_COLS, load_raw
from app.eda import (
    show_categorical_distribution,
    show_correlation_heatmap,
    show_numeric_distribution,
    show_overview,
    show_subscribe_rate_by_category,
    show_target_distribution,
)

st.set_page_config(page_title="数据分析", page_icon="📊", layout="wide")
st.title("📊 银行营销数据分析")

df = load_raw(TRAIN_CSV)

# Sidebar filters
st.sidebar.header("筛选条件")
selected_jobs = st.sidebar.multiselect("职业 (job)", sorted(df["job"].unique()), default=None)
if selected_jobs:
    df = df[df["job"].isin(selected_jobs)]

# Overview
show_overview(df)
st.divider()

# Target distribution
show_target_distribution(df)
st.divider()

# Feature analysis
st.header("特征分布分析")
analysis_type = st.radio(
    "分析类型",
    ["单变量分布", "交叉分析(认购率)", "相关性热力图"],
    horizontal=True,
)

if analysis_type == "单变量分布":
    feat_type = st.selectbox("特征类型", ["数值特征", "分类特征"])
    if feat_type == "数值特征":
        selected = st.selectbox("选择数值特征", NUMERIC_COLS)
        show_numeric_distribution(df, selected)
    else:
        selected = st.selectbox("选择分类特征", CATEGORICAL_COLS)
        show_categorical_distribution(df, selected)

elif analysis_type == "交叉分析(认购率)":
    selected = st.selectbox("选择分类特征", CATEGORICAL_COLS)
    show_subscribe_rate_by_category(df, selected)

elif analysis_type == "相关性热力图":
    show_correlation_heatmap(df)

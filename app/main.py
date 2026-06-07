import streamlit as st

from app.config import TRAIN_CSV
from app.data_loader import load_train_val
from app.model import model_exists, save_model, train_model

st.set_page_config(page_title="银行营销分析与预测", page_icon="🏦", layout="wide")
st.title("🏦 银行营销分析与预测系统")
st.markdown("使用左侧导航栏选择功能页面。")

# Auto-train model on first launch
if not model_exists():
    with st.spinner("首次启动,正在训练模型..."):
        X_train, X_val, y_train, y_val = load_train_val(TRAIN_CSV)
        pipeline = train_model(X_train, y_train)
        save_model(pipeline)
    st.success("模型训练完成!请选择左侧页面开始使用。")

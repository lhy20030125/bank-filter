import pandas as pd
import plotly.express as px
import streamlit as st

from app.config import TRAIN_CSV
from app.data_loader import (
    CATEGORICAL_COLS,
    NUMERIC_COLS,
    get_categorical_options,
    get_feature_names,
    get_numeric_ranges,
)
from app.model import load_model, model_exists, predict

st.set_page_config(page_title="在线预测", page_icon="🔮", layout="wide")
st.title("🔮 客户认购预测")

if not model_exists():
    st.error("模型尚未训练,请先启动应用完成模型训练。")
    st.stop()

pipeline = load_model()
cat_options = get_categorical_options(TRAIN_CSV)
num_ranges = get_numeric_ranges(TRAIN_CSV)

st.markdown("请通过点选和滑块输入客户特征信息,然后点击 **预测** 按钮获取结果。")

# Input form
with st.form("prediction_form"):
    st.subheader("分类特征")
    cat_cols = st.columns(3)
    user_input = {}

    for i, col in enumerate(CATEGORICAL_COLS):
        with cat_cols[i % 3]:
            options = cat_options[col]
            user_input[col] = st.selectbox(col, options, key=f"cat_{col}")

    st.subheader("数值特征")
    num_cols = st.columns(3)
    for i, col in enumerate(NUMERIC_COLS):
        with num_cols[i % 3]:
            lo, hi = num_ranges[col]
            # Use float for all numeric inputs
            step = max((hi - lo) / 100, 0.01)
            val = st.slider(
                col,
                min_value=float(lo),
                max_value=float(hi),
                value=float((lo + hi) / 2),
                step=step,
                key=f"num_{col}",
            )
            user_input[col] = val

    submitted = st.form_submit_button("预测", use_container_width=True)

if submitted:
    # Build input DataFrame
    input_df = pd.DataFrame([user_input])

    # Ensure column order matches training
    input_df = input_df[get_feature_names()]

    result = predict(pipeline, input_df)

    st.divider()
    st.subheader("预测结果")

    col1, col2 = st.columns(2)
    with col1:
        if result["prediction"] == "yes":
            st.success(f"**预测结果: 会认购** (概率 {result['probability_yes']:.1%})")
        else:
            st.warning(f"**预测结果: 不会认购** (概率 {result['probability_no']:.1%})")

    with col2:
        st.metric("认购概率", f"{result['probability_yes']:.1%}")

    # Top 5 feature importances
    st.subheader("影响最大的 Top 5 特征")
    feature_names = get_feature_names()
    importances = result["feature_importances"]
    imp_df = pd.DataFrame({"feature": feature_names, "importance": importances})
    imp_df = imp_df.sort_values("importance", ascending=False).head(5)

    fig = px.bar(
        imp_df,
        x="importance",
        y="feature",
        orientation="h",
        title="Top 5 特征重要性",
        text_auto=".3f",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

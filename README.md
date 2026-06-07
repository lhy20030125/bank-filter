# bank_filter

基于银行营销数据的 Web 应用:数据可视化分析 + 客户认购在线预测。

## 快速启动

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
streamlit run app/main.py --server.port 8004
```

## Docker

```bash
docker build -t bank_filter .
docker run -p 8004:8004 bank_filter
```

## 开发

```bash
pip install -r requirements.txt -r requirements-dev.txt
ruff format --check .
ruff check .
pytest --cov --cov-fail-under=80
```

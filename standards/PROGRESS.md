# PROGRESS.md 〔本项目活记忆 · AI 维护〕

> **作用**:记录项目当前状态、下一步 TODO、决策记录(ADR)、踩坑记录(GOTCHAS)。
> **格式**:时间倒序,最新在前。

---

## 当前状态

- **对应六步流程**: 第 ④ 步完成 — 本地 CI 自检全绿
- **已完成**: T1~T14 全部完成,用户已验证应用功能
- **下一步**: 提交代码,准备 PR(如需远程)

---

## TODO 第一批

> 按优先级排列,对应 US-1 ~ US-5。

| # | 任务 | 对应 US | 状态 | 备注 |
|---|---|---|---|---|
| T1 | 初始化 Git 仓库,创建 `.gitignore`、`README.md` | US-1 | Done | |
| T2 | 创建 `requirements.txt` 与 `requirements-dev.txt` | US-1 | Done | |
| T3 | 创建 `app/` 目录结构与空模块文件 | US-1 | Done | |
| T4 | 编写 `tests/conftest.py` 与基础测试桩 | US-1 | Done | |
| T5 | 编写 CI 配置 `.github/workflows/ci.yml` | US-1 | Done | |
| T6 | 编写 `Dockerfile` | US-5 | Done | |
| T7 | 实现 `app/data_loader.py` — 数据加载与预处理 | US-3 | Done | 覆盖率 100% |
| T8 | 实现 `app/model.py` — 模型训练、保存、加载、预测 | US-3 | Done | AUC=0.8149, 覆盖率 90% |
| T9 | 实现 `app/eda.py` — EDA 可视化逻辑 | US-2 | Done | Streamlit UI 代码,覆盖率排除 |
| T10 | 实现数据分析页面 `app/pages/1_📊_数据分析.py` | US-2 | Done | |
| T11 | 实现在线预测页面 `app/pages/2_🔮_在线预测.py` | US-4 | Done | |
| T12 | 实现应用入口 `app/main.py` | US-1 | Done | |
| T13 | 为每个模块编写单元测试 | US-1~4 | Done | 18 用例全绿,覆盖率 96.10% |
| T14 | 本地 CI 自检:ruff + pytest + docker build | US-1 | Done | 全绿 |

---

## ADR (架构决策记录)

- **ADR-1**: test.csv 无目标变量 `subscribe`,采用 train.csv 按 80/20 stratified split 做训练/验证。test.csv 仅用于预测。
- **ADR-2**: 排除 `id`(非预测特征) 和 `duration`(数据泄露 — 通话时长在拨打电话前未知)。
- **ADR-3**: 覆盖率排除 `eda.py`、`main.py`、`pages/*`(纯 Streamlit UI 代码,无法单元测试)。核心逻辑覆盖率 96.10%。
- **ADR-4**: 模型选用 RandomForest(class_weight="balanced")处理类别不均衡,AUC=0.8149 > 0.75 达标。

---

## GOTCHAS (踩坑记录)

- **GOTCHA-1**: `ColumnTransformer.transformers_`(带下划线)仅在 fit 后可用,未 fit 时用 `.transformers`。
- **GOTCHA-2**: test.csv 列数比 train.csv 少 1(无 subscribe),`split_xy` 需判断目标列是否存在。
- **GOTCHA-3**: Windows 环境下 `ruff` 需通过 `python -m ruff` 调用,直接 `ruff` 可能找不到命令。

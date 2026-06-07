# 00 · 项目上下文 〔本项目活记忆 · AI 维护〕

> **作用**:项目的"身份档案"。AI 接管项目时先读这里。
> **更新时机**:架构、技术栈、目录结构、端口、部署目录、重要约束变化时更新。

---

## 1. 项目是什么

- **项目名称**: `bank_filter`
- **一句话目标**: 基于银行营销数据,提供数据可视化分析与客户认购预测的 Web 应用。
- **使用者/受益者**: 银行营销分析师 / 业务人员,通过数据分析洞察客户特征,并在线预测新客户是否会认购定期存款产品。
- **核心功能**:
  - 数据分析交互页面:多维度可视化展示客户画像与营销数据分布。
  - 在线预测系统:基于离线训练模型,用户通过点选输入特征,实时获得认购预测结果。
- **输入/数据**:
  - 来源: 银行营销数据集(Portuguese Bank Marketing)。
  - 规模: 训练集 22500 条,测试集 7500 条,22 个字段(含目标变量 `subscribe`)。
  - 敏感性: 教学数据,不含真实客户隐私,可进 Git。
  - 路径: `data/train.csv`, `data/test.csv`(CSV 格式,逗号分隔)。

## 2. 技术栈

| 层 | 选型 | 理由 |
|---|---|---|
| 语言/运行时 | Python 3.11 | 用户指定,稳定且生态丰富 |
| Web 框架 | Streamlit | 用户指定,快速构建交互式数据应用,适合非前端开发者 |
| 测试 | pytest | Python 社区标准,易用且插件丰富 |
| 格式/静态检查 | ruff | 用户指定,极快的 Python linter + formatter |
| 打包/运行 | Docker | 用户指定,保证环境一致性 |
| CI/CD | GitHub Actions | 通用、可视化、适合教学与团队协作 |

## 3. 目录地图

```text
bank_filter/
├── standards/                 # AI 项目记忆与通用规范
├── data/                      # 训练与测试数据(进 Git,教学数据)
│   ├── train.csv
│   └── test.csv
├── app/                       # Streamlit 应用源码
│   ├── __init__.py
│   ├── main.py                # 应用入口(多页面导航)
│   ├── pages/
│   │   ├── 1_📊_数据分析.py    # 数据分析交互页面
│   │   └── 2_🔮_在线预测.py    # 在线预测页面
│   ├── data_loader.py         # 数据加载与预处理
│   ├── eda.py                 # EDA 与可视化逻辑
│   ├── model.py               # 模型训练、保存、加载、预测
│   └── config.py              # 应用配置(路径、端口等)
├── models/                    # 模型产物(不进 Git,运行时生成)
├── tests/                     # 测试目录
│   ├── conftest.py
│   ├── test_data_loader.py
│   ├── test_eda.py
│   ├── test_model.py
│   └── test_app.py
├── requirements.txt           # 生产运行依赖
├── requirements-dev.txt       # CI/本地检查依赖
├── Dockerfile
├── .github/workflows/
│   └── ci.yml
├── .gitignore
└── README.md
```

> 新增目录前先更新本节,避免项目越做越散。

## 4. 质量门槛

| 类型 | 本项目标准 |
|---|---|
| 格式检查 | `ruff format --check .` |
| 静态检查 | `ruff check .` |
| 单元测试 | `pytest` |
| 覆盖率 | `pytest --cov --cov-fail-under=80` |
| 构建 | `docker build .` |
| 业务/模型指标 | 模型 AUC ≥ 0.75 |

## 5. 不变约束

- 密钥、密码、私钥、Token **绝不写进代码或文档**,只进 GitHub Secrets / 环境变量。
- 数据文件(`data/`)为教学数据,可进 Git;模型产物(`models/`)不进 Git。
- `main` 分支受保护,日常开发必须走 feature 分支 + PR。
- CI 红灯不合并。

## 6. 部署/CI 占位符取值

| 占位符 | 本项目取值 | 说明 |
|---|---|---|
| `<APP>` | `bank_filter` | 应用名/容器名 |
| `<DEPLOY_DIR>` | 本地部署,无远程目录 | 本地 Docker 运行 |
| `<PORT>` | `8004` | Streamlit 服务端口 |
| `<PYVER>` | `3.11` | Python 版本 |
| `<HEALTHCHECK>` | `_stcore/health` | Streamlit 内置健康检查端点 |

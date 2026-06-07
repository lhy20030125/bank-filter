# 01 · 需求 / 活 PRD 〔本项目活记忆 · AI 维护〕

> **作用**:本项目唯一的需求文档。所有新功能、缺陷、技术债都追加到这里。
> **更新时机**:每次有新需求、需求变更、验收标准变化时更新。

---

## 1. 需求来源

| 类型 | 来源 | 进入方式 |
|---|---|---|
| 功能需求 Feature | 用户(课程项目) | 写成用户故事 |

---

## 2. Issue 生命周期

| 阶段 | 状态 | 动作 |
|---|---|---|
| 提出 | Open | 写清场景、目标、验收标准 |
| 排期 | Backlog / Todo | 决定优先级 |
| 开发 | In Progress | 从 main 开 feature 分支 |
| 评审 | In Review | 提 PR,等待 CI 和 Review |
| 合并 | Done | PR 合并 main |
| 验收 | Verified | 按验收标准确认 |

---

## 3. 用户故事模板

```text
### US-<编号> <一句话标题> · 状态: Backlog
作为 <角色>,
我想要 <能力>,
以便 <价值>。

验收标准:
- AC1: Given <前提>,When <动作>,Then <可验证结果>。
- AC2: <补充标准>

技术备注:
- <可选:约束、边界、风险>
```

---

## 4. 需求清单

### US-1 项目初始化与 CI · 状态: Backlog

作为 **项目开发者**,
我想要 项目具备基础工程结构、测试框架与 CI 流水线,
以便 后续每次开发都能自动检查代码质量。

验收标准:
- AC1: 项目目录结构符合 `00-project-context.md` 目录地图。
- AC2: `requirements.txt` 与 `requirements-dev.txt` 分离,依赖可正常安装。
- AC3: `.gitignore` 正确排除 `models/`、`__pycache__/`、`.pytest_cache/` 等。
- AC4: PR 触发 CI,包含格式检查(`ruff format --check .`)、静态检查(`ruff check .`)、单元测试(`pytest --cov --cov-fail-under=80`)。
- AC5: CI 全绿,`docker build .` 成功。

技术备注:
- 只做 CI,不做 CD(本地部署)。
- 端口 8004。

---

### US-2 数据分析交互页面 · 状态: Backlog

作为 **银行营销分析师**,
我想要 一个交互式数据看板,从多维度探索银行营销数据,
以便 快速了解客户画像、营销效果和关键影响因素。

验收标准:
- AC1: Given 用户打开应用,When 进入"数据分析"页面,Then 可看到数据集概览(行数、列数、字段类型、缺失值统计)。
- AC2: Given 用户在侧边栏选择特征维度(如 age、job、education 等),When 点击筛选,Then 页面展示对应的分布图(直方图/柱状图/饼图)。
- AC3: Given 用户选择两个变量,When 进行交叉分析,Then 展示分组统计与可视化(如不同 job 的 subscribe 比例)。
- AC4: Given 用户查看数据,When 点击相关性分析,Then 展示数值特征的相关性热力图。
- AC5: 页面响应时间 < 3 秒(本地环境)。

技术备注:
- 使用 Streamlit 原生组件 + Plotly/Matplotlib/Seaborn 可视化。
- 数据从 `data/train.csv` 加载。

---

### US-3 离线模型训练 · 状态: Backlog

作为 **数据科学家**,
我想要 在应用启动时自动完成数据预处理与模型训练,
以便 在线预测页面可以加载已训练好的模型进行实时预测。

验收标准:
- AC1: Given 应用启动,When 加载数据,Then 自动完成缺失值处理、类别特征编码、数值特征标准化。
- AC2: Given 预处理完成,When 训练模型,Then 使用分类算法(如 RandomForest/XGBoost)训练,并将模型持久化到 `models/` 目录。
- AC3: Given 模型训练完成,When 评估模型,Then 测试集 AUC ≥ 0.75,并输出分类报告(精确率、召回率、F1)。
- AC4: Given `models/` 目录已有模型文件,When 应用再次启动,Then 直接加载已有模型,不重复训练。

技术备注:
- 模型文件不进 Git(`.gitignore` 排除 `models/`)。
- 目标变量: `subscribe`(yes/no → 1/0)。
- 训练/测试数据分别在 `data/train.csv` 和 `data/test.csv`。

---

### US-4 在线预测系统 · 状态: Backlog

作为 **银行营销人员**,
我想要 通过点选输入新客户的特征信息,系统即时预测该客户是否会认购,
以便 有针对性地制定营销策略,提高营销效率。

验收标准:
- AC1: Given 用户进入"在线预测"页面,When 页面加载完成,Then 展示所有可输入特征的点选控件(下拉框/单选按钮),无文本输入框。
- AC2: Given 用户选择完所有特征,When 点击"预测"按钮,Then 在 2 秒内展示预测结果(是否认购 + 认购概率)。
- AC3: Given 预测结果展示,When 用户查看结果,Then 同时展示影响该预测的 Top 5 重要特征及其贡献度。
- AC4: Given 用户输入不合理组合(如 age=5 且 job=management),When 点击预测,Then 给出友好提示但仍可预测。

技术备注:
- 点选选项来源于训练数据中各分类特征的唯一值。
- 数值特征使用滑块(Slider)输入,范围取训练数据的 min-max。
- 模型从 `models/` 目录加载。

---

### US-5 Docker 容器化 · 状态: Backlog

作为 **运维人员**,
我想要 应用可通过 Docker 一键构建和运行,
以便 保证环境一致性,简化部署流程。

验收标准:
- AC1: `docker build -t bank_filter .` 成功构建。
- AC2: `docker run -p 8004:8004 bank_filter` 启动后,访问 `http://localhost:8004` 可正常使用全部功能。
- AC3: 容器内健康检查 `curl http://localhost:8004/_stcore/health` 返回 200。

技术备注:
- Dockerfile 使用 Python 3.11 基础镜像。
- 生产依赖与开发依赖分离,镜像只安装 `requirements.txt`。

---

## 5. 非功能需求

- **安全**: 密钥只进 Secrets,不进 Git。
- **可维护**: 一需求一小 PR,避免大爆炸式提交。
- **可测试**: 核心逻辑(数据加载、模型训练、预测)必须有单元测试。
- **可部署**: 本地 Docker 部署,端口 8004。
- **不做 CD**: 仅 CI,本地手动运行 Docker。

# 医院智能导诊问答系统

基于 ReAct 与 RAG 的医院智能导诊问答系统 - 完整可运行工程化系统

## 项目介绍

本系统是基于简历项目"项目二"实现的完整可运行系统，具备以下功能：

1. **多轮对话问诊**：用户输入症状描述，系统智能推荐科室
2. **医生排班查询**：根据推荐科室，查询该科室的医生排班信息
3. **费用估算**：根据科室和检查项目，估算总费用和医保报销金额
4. **流式输出（SSE）**：对话界面支持打字机效果的流式输出

## 技术架构

### 系统架构（五层全栈）

```
┌────────────────────────────────────────────────────┐
│  Layer 5: 前端展示层 (纯 HTML/JS + CSS)           │
│  对话 UI(SSE 流) / 科室推荐卡 / 医生查询    │
├────────────────────────────────────────────────────┤
│  Layer 4: API 网关 (FastAPI + Nginx)               │
│  统一入口 / CORS / 限流 / 日志                      │
├────────────────────────────────────────────────────┤
│  Layer 3: 后端服务层 (Python FastAPI)             │
│  对话管理 / 科室引擎 / 医生匹配 / 费用计算       │
├────────────────────────────────────────────────────┤
│  Layer 2: RAG 知识检索层                         │
│  医疗知识库 / 向量索引 (Milvus + OpenAI)         │
├────────────────────────────────────────────────────┤
│  Layer 1: LLM 推理层                             │
│  CoT 推理链(多链路并行) / ReAct Agent         │
└────────────────────────────────────────────────────┘
```

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | 纯 HTML/JS + CSS | 无需 Node.js，直接浏览器打开 |
| 前端 | EventSource API | SSE 流式通信 |
| 后端 | FastAPI (Python 3.10+) | API 框架 |
| RAG | LangChain | 链路编排 |
| 向量 | Milvus + OpenAI Embeddings | 向量数据库 + 嵌入模型 |
| LLM | OpenAI API | 底部推理（需配置 API Key） |
| 部署 | Docker Compose | 容器化（backend + milvus + frontend） |

## 快速启动

### 最简单方式：一键启动（推荐）

**Windows 用户**：
1. 双击运行 `start.bat` 文件
2. 等待后端启动（显示 "Uvicorn running on http://0.0.0.0:8000"）
3. 在浏览器中打开 http://localhost:8000

**Linux/Mac 用户**：
1. 终端执行：`bash start.sh`
2. 等待后端启动
3. 在浏览器中打开 http://localhost:8000

### 方式二：手动启动

1. **创建虚拟环境并安装依赖**
   ```bash
   cd backend
   python -m venv venv
   ./venv/Scripts/pip.exe install -r requirements.txt
   cd ..
   ```

2. **启动后端**
   ```bash
   cd backend
   ./venv/Scripts/uvicorn.exe app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **访问系统**
   浏览器打开：http://localhost:8000

### 方式三：Docker Compose 启动（需要 Docker）

1. **复制环境变量模板**
   ```bash
   cp .env.example .env
   ```

2. **编辑 `.env` 文件，填入 OpenAI API Key**
   ```
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ```

3. **启动所有服务**
   ```bash
   docker-compose up -d
   ```
   首次启动会下载 Docker 镜像，需要等待几分钟。

4. **查看服务状态**
   ```bash
   docker-compose ps
   ```

5. **初始化知识库（首次）**
   ```bash
   docker-compose exec backend python init_knowledge_base.py
   ```

6. **访问前端**
   浏览器打开：http://localhost:8080

7. **查看后端 API 文档**
   浏览器打开：http://localhost:8000/docs

### 方式二：本地运行（用于开发调试）

1. **安装后端依赖**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env，填入 OpenAI API Key
   ```

3. **启动后端**
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **启动前端**
   直接用浏览器打开 `frontend/index.html` 文件。
   注意：需要修改 `frontend/js/utils.js` 中的 `API_BASE_URL` 为 `http://localhost:8000/api/v1`。

## 示例对话流程

1. **打开前端页面**（http://localhost:8080）
2. **输入症状描述**
   - 示例："我头痛3天了，有时候会恶心"
3. **查看推荐科室**
   - 系统会推荐：神经内科（置信度94%）、心血管内科等
4. **查询医生排班**
   - 点击推荐的科室，查看该科室的医生排班信息
5. **估算费用**
   - 查看该科室的常见检查项目价格和医保报销比例

## 项目结构

```
hospital-guide-system/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── chains/        # CoT 推理链
│   │   ├── rag/           # RAG 知识检索
│   │   ├── agent/         # ReAct Agent
│   │   ├── models/        # 数据模型
│   │   └── data/         # 示例数据（JSON）
│   ├── requirements.txt   # Python 依赖
│   └── Dockerfile        # 后端容器
├── frontend/              # 前端代码
│   ├── index.html         # 主页面
│   ├── css/              # 样式
│   ├── js/               # JavaScript 逻辑
│   └── Dockerfile        # 前端容器
├── docker-compose.yml     # 容器编排
├── .env.example          # 环境变量示例
└── README.md             # 本文件
```

## API 文档

启动后端后，访问 http://localhost:8000/docs 查看完整的 Swagger API 文档。

### 主要接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/chat/session` | POST | 创建新会话 |
| `/api/v1/chat/send` | POST | 发送消息（非流式） |
| `/api/v1/chat/stream` | GET | 发送消息（SSE 流式） |
| `/api/v1/department/recommend` | POST | 推荐科室 |
| `/api/v1/doctors` | GET | 查询医生 |
| `/api/v1/cost/estimate` | POST | 估算费用 |

## 注意事项

1. **OpenAI API Key**：需要用户自行配置到 `.env` 文件中。如果没有 OpenAI API Key，可以修改为兼容接口（如 DeepSeek、通义千问等）。

2. **Milvus 资源需求**：Milvus 需要较高内存（建议 4GB+ 可用内存）。如果资源不足，可以先用简单向量检索（scikit-learn 余弦相似度）代替。

3. **数据规模**：示例数据已内置在 `data/` 目录，足够演示和测试。实际部署时可以替换为真实医院数据。

4. **SSE 限制**：浏览器 `EventSource` API 只支持 GET 请求。对于需要发送大量数据的场景，可以用 `POST + ReadableStream` 或者将参数编码到 URL 中。

## 后续优化方向

1. **集成真实 LLM**：当前使用规则推理，后续可接入 OpenAI API 实现更智能的症状分析和科室推荐。
2. **完善 RAG 检索**：集成 Milvus 向量数据库，实现基于医疗知识库的检索增强生成。
3. **实现多链路并行推理**：同时执行科室推荐链、医生匹配链、费用医保链。
4. **实现 ReAct Agent**：让系统能自主决策调用工具（如查询天气、查询交通路线等）。
5. **添加用户认证**：实现用户登录、会话管理、历史记录查询。

## 联系方式

如有问题，请提交 Issue 或联系开发者。

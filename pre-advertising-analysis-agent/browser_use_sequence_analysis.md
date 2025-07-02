# Browser Use Local Test 时序图分析

## 概述
`browser_use_local_test.py` 是一个基于 AWS Bedrock 和浏览器自动化的 AI 代理测试脚本。以下是详细的调用流程分析。

## 主要组件
1. **Main Script** (`browser_use_local_test.py`)
2. **AWS Bedrock LLM** (`ChatBedrockConverse`)
3. **Browser Profile & Session** (`BrowserProfile`, `BrowserSession`)
4. **Agent** (`browser_use.Agent`)
5. **Controller** (`browser_use.Controller`)
6. **Message Manager** (内部组件)
7. **Playwright Browser** (底层浏览器控制)

## 详细时序流程

### 1. 初始化阶段 (Initialization Phase)

```
Main Script → Environment Setup
├── load_dotenv() - 加载环境变量
├── logging.basicConfig() - 配置日志
└── argparse.ArgumentParser() - 解析命令行参数

Main Script → AWS Bedrock LLM Setup
├── boto3.client('bedrock-runtime') - 创建 Bedrock 客户端
├── Config(retries={'max_attempts': 10}) - 配置重试策略
└── ChatBedrockConverse() - 初始化 Claude 3.7 Sonnet 模型
    ├── model_id: 'us.anthropic.claude-3-7-sonnet-20250219-v1:0'
    ├── temperature: 0.0
    └── max_tokens: None

Main Script → Browser Setup
├── BrowserProfile() - 创建浏览器配置
│   └── executable_path: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
└── BrowserSession() - 创建浏览器会话
    └── browser_profile: BrowserProfile

Main Script → Agent Initialization
└── Agent() - 创建 AI 代理
    ├── task: CNN 新闻分析任务
    ├── llm: ChatBedrockConverse 实例
    ├── controller: Controller() 实例
    ├── browser_session: BrowserSession 实例
    └── validate_output: True
```

### 2. 执行阶段 (Execution Phase)

```
Main Script → Agent.run(max_steps=30)
│
├── Agent.run() [异步方法]
│   ├── SignalHandler.register() - 注册信号处理器
│   ├── self._log_agent_run() - 记录代理运行日志
│   │
│   └── for step in range(max_steps): [主执行循环]
│       │
│       ├── Agent.step(step_info) [每步执行]
│       │   │
│       │   ├── BrowserSession.get_state_summary() [获取浏览器状态]
│       │   │   ├── 获取当前页面信息
│       │   │   ├── 提取 DOM 元素
│       │   │   ├── 识别可点击元素
│       │   │   └── 生成页面摘要
│       │   │
│       │   ├── BrowserSession.get_current_page() [获取当前页面]
│       │   │   └── 返回 Playwright Page 对象
│       │   │
│       │   ├── Controller.registry.get_prompt_description() [获取可用动作]
│       │   │   ├── 过滤页面特定动作
│       │   │   └── 生成动作描述
│       │   │
│       │   ├── MessageManager.add_state_message() [添加状态消息]
│       │   │   ├── 添加浏览器状态摘要
│       │   │   ├── 添加上一步结果
│       │   │   └── 添加视觉信息（如果启用）
│       │   │
│       │   ├── LLM.ainvoke() [调用 AI 模型]
│       │   │   ├── 发送消息到 AWS Bedrock
│       │   │   ├── Claude 模型分析当前状态
│       │   │   ├── 生成下一步动作决策
│       │   │   └── 返回结构化动作序列
│       │   │
│       │   ├── Controller.multi_act() [执行动作序列]
│       │   │   │
│       │   │   └── for action in actions:
│       │   │       ├── Controller.act() [执行单个动作]
│       │   │       │   ├── 验证动作参数
│       │   │       │   ├── 调用对应动作处理器
│       │   │       │   └── 返回动作结果
│       │   │       │
│       │   │       └── 动作类型处理:
│       │   │           ├── GoToUrlAction → Page.goto()
│       │   │           ├── ClickElementAction → Element.click()
│       │   │           ├── InputTextAction → Element.fill()
│       │   │           ├── ScrollAction → Page.evaluate()
│       │   │           └── DoneAction → 任务完成
│       │   │
│       │   ├── 更新代理状态
│       │   │   ├── self.state.n_steps += 1
│       │   │   ├── self.state.last_result = result
│       │   │   └── 检查失败计数
│       │   │
│       │   └── 检查终止条件
│       │       ├── 任务完成 (DoneAction)
│       │       ├── 最大失败次数
│       │       └── 用户中断
│       │
│       └── 步骤完成回调 (如果有)
│
└── 执行完成处理
    ├── 生成历史记录
    ├── 保存对话记录
    └── 触发完成回调
```

### 3. 清理阶段 (Cleanup Phase)

```
Main Script → Cleanup
└── BrowserSession.close() [异步方法]
    ├── 关闭所有浏览器标签页
    ├── 关闭浏览器上下文
    ├── 关闭浏览器实例
    └── 清理临时文件
```

## 关键异步调用模式

### 异步方法调用链
```
asyncio.run(main()) 
└── Agent.run()
    └── Agent.step()
        ├── BrowserSession.get_state_summary()
        ├── BrowserSession.get_current_page()
        ├── LLM.ainvoke()
        ├── Controller.multi_act()
        │   └── Controller.act()
        │       └── Playwright API calls
        └── BrowserSession.close()
```

## 数据流分析

### 输入数据流
```
Task Description → Agent → MessageManager → LLM → Action Decisions
```

### 状态数据流
```
Browser State → DOM Analysis → State Summary → Context Messages → LLM Input
```

### 输出数据流
```
LLM Output → Action Parsing → Controller Execution → Browser Actions → Results
```

## 错误处理机制

1. **重试机制**: AWS Bedrock 客户端配置了最大 10 次重试
2. **失败计数**: Agent 跟踪连续失败次数，达到阈值后停止
3. **信号处理**: 支持 CTRL+C 优雅退出
4. **异常捕获**: 各层级都有相应的异常处理

## 性能优化点

1. **缓存机制**: 浏览器状态摘要使用缓存
2. **异步执行**: 所有 I/O 操作都是异步的
3. **资源管理**: 及时清理浏览器资源
4. **批量操作**: 支持多动作批量执行

## 扩展点

1. **自定义动作**: 通过 Controller 注册新动作
2. **记忆系统**: 支持程序性记忆存储
3. **规划器**: 可配置 LLM 规划器
4. **回调机制**: 支持步骤开始/结束回调

这个架构展现了现代 AI 代理系统的典型设计模式：
- 分层架构
- 异步编程
- 状态管理
- 错误恢复
- 可扩展性

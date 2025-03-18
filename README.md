# README Generator

## 项目描述

`readme-generator` 是一个利用大型语言模型（LLM）的工具，用于自动生成项目的README文档。它通过分析代码结构和内容，生成具有良好格式的文档，帮助开发者快速创建项目说明。

## 主要特性

- 自动解析代码仓库以提取关键信息
- 生成标准化的README格式
- 支持多种配置和自定义模板
- 使用OpenAI的API进行文本生成
- 易于集成和使用

## 安装说明

要安装`readme-generator`，请按照以下步骤操作：

1. 克隆该仓库：

   ```bash
   git clone https://github.com/yourusername/readme-generator.git
   cd readme-generator
   ```

2. 安装依赖项：

   ```bash
   pip install -r requirements.txt
   ```

3. 运行安装程序：

   ```bash
   python setup.py install
   ```

## 使用示例

使用命令行工具生成README：

```bash
readme-generator
```

这将自动分析当前目录下的代码文件并生成README文档。

## 项目架构

该项目的目录结构如下：

```
readme-generator/
├── config/
│   └── config.py            # 配置文件
├── examples/
│   ├── example_repo/        # 示例代码仓库
│   └── generated_readmes/   # 生成的README示例
├── prompt.txt               # 提示模板文件
├── requirements.txt         # 依赖库列表
├── setup.py                 # 安装脚本
├── src/
│   ├── api/
│   │   ├── openai_client.py # OpenAI API客户端
│   │   └── __init__.py
│   ├── main.py              # 主程序入口
│   ├── models/
│   │   └── agent.py         # LLM代理模型
│   ├── services/
│   │   ├── code_analyzer.py # 代码分析服务
│   │   └── readme_generator.py # README生成服务
│   └── utils/
│       ├── code_parser.py    # 代码解析工具
│       ├── file_handler.py    # 文件处理工具
│       └── prompt_templates.py # 提示模板工具
└── tests/
    ├── test_agent.py         # 代理模型单元测试
    ├── test_code_analyzer.py # 代码分析服务单元测试
    └── test_readme_generator.py # README生成服务单元测试
```

### 主要组件

- **API**: 与OpenAI API的交互和请求处理
- **Models**: 定义和实现LLM代理
- **Services**: 提供核心功能的服务，包括代码分析和README生成
- **Utils**: 辅助工具和功能

## 技术栈

- Python 3.8+
- OpenAI API
- Langchain
- 其他Python库（详见`requirements.txt`）

## 贡献指南

欢迎任何形式的贡献！请遵循以下步骤：

1. Fork此仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个新的Pull Request

## 许可证

该项目采用MIT许可证。详情请参见`LICENSE`文件。
```

# AlgoRhythm

AlgoRhythm 是一个音频分析与谱面生成应用，旨在为用户提供一个互动的音乐节奏游戏体验。该项目允许用户上传音频文件，自动生成谱面，并通过游戏引擎进行音频播放和音符互动。

## 主要特性

- **音频上传**：用户可以选择并上传音频文件。
- **谱面生成**：自动生成与音频节奏相匹配的谱面。
- **游戏模式**：用户可以通过键盘控制，参与互动游戏，测试音乐节奏感。
- **音频分析**：使用先进的音频处理工具进行音频分析，以提取节奏和音符信息。

## 安装说明

要在本地环境中运行 AlgoRhythm，请按照以下步骤进行安装：

1. 克隆该仓库：
   ```bash
   git clone https://github.com/yourusername/AlgoRhythm.git
   cd AlgoRhythm
   ```

2. 创建并激活虚拟环境（可选）：
   ```bash
   python -m venv venv
   source venv/bin/activate  # 在Windows上使用 venv\Scripts\activate
   ```

3. 安装项目依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 启动应用：
   ```bash
   python main.py
   ```

5. 打开浏览器访问 `http://127.0.0.1:5000`。

## 使用示例

1. 在主页上传音频文件。
2. 设置难度级别并提交。
3. 开始游戏，通过按键控制音符的点击。

## 项目架构

AlgoRhythm 的项目结构如下：

```
AlgoRhythm/
├── config.py
├── main.py
├── package-lock.json
├── package.json
├── requirements.txt
├── samples/
│   ├── Hello Friend (Electric).mp3
│   └── Ignite (Instrumental).mp3
├── src/
│   ├── __init__.py
│   ├── audio/
│   │   ├── __init__.py
│   │   ├── analyzer.py
│   │   └── features.py
│   ├── chart/
│   │   ├── __init__.py
│   │   ├── generator.py
│   │   └── models.py
│   ├── game/
│   │   ├── __init__.py
│   │   ├── audio_manager.py
│   │   ├── engine.py
│   │   └── renderer.py
│   └── utils/
│       ├── __init__.py
│       ├── chart_storage.py
│       └── file_handler.py
├── static/
│   ├── charts/
│   ├── css/
│   │   └── style.css
│   ├── fonts/
│   ├── img/
│   ├── js/
│   └── uploads/
└── templates/
    ├── index.html
    ├── play.html
    └── upload.html
```

### 主要组件

- **src/audio**：处理音频分析和特征提取。
- **src/chart**：生成音符和谱面模型。
- **src/game**：管理游戏引擎与音频交互。
- **static**：存放静态文件，包括样式表、脚本和上传的音频。
- **templates**：HTML模板，用于构建用户界面。

## 技术栈

- **后端**：Python, Flask
- **前端**：HTML, CSS, JavaScript
- **音频处理**：librosa, numpy, scipy
- **数据可视化**：matplotlib

## 贡献指南

欢迎任何形式的贡献！请遵循以下步骤：

1. Fork 此仓库。
2. 创建你的特性分支 (`git checkout -b feature/YourFeature`)。
3. 提交你的更改 (`git commit -m 'Add some feature'`)。
4. 推送到分支 (`git push origin feature/YourFeature`)。
5. 创建一个新的 Pull Request。

## 许可证

该项目采用 MIT 许可证，详细信息请查看 [LICENSE](LICENSE) 文件。
# OCRmyPDF

OCRmyPDF 是一个用于在扫描的 PDF 文件上添加光学字符识别（OCR）文本层的工具，从而使其可以进行搜索。该项目利用现代 OCR 技术，提高了用户处理 PDF 文档的效率和可用性。

## 主要特性

- 将 OCR 文本层添加到扫描的 PDF 文件中
- 支持多种语言的 OCR 处理
- 提供多种格式的输入和输出选项
- 支持图像优化和压缩
- 可通过命令行接口或 Web 服务使用
- 支持 Docker 部署

## 安装说明

### 系统要求

- Python 3.10 或更高版本
- Ghostscript
- Tesseract OCR

### 安装步骤

1. 克隆该仓库：

   ```bash
   git clone https://github.com/ocrmypdf/OCRmyPDF.git
   cd OCRmyPDF
   ```

2. 使用 `pip` 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 运行 Docker（可选）：

   你可以使用 Docker 来运行 OCRmyPDF：

   ```bash
   docker build -t ocrmypdf .
   docker run -v $(pwd):/input ocrmypdf input.pdf output.pdf
   ```

## 使用示例

### 命令行使用

运行 OCRmyPDF 的基本命令：

```bash
ocrmypdf input.pdf output.pdf
```

### Web 服务

OCRmyPDF 还可以通过 Web 服务提供 OCR 功能。请参见 `webservice.py` 文件获取更多信息。

## 项目架构

该项目的主要模块包括：

- `src/ocrmypdf`：核心处理逻辑
- `src/ocrmypdf/pdfinfo`：提取 PDF 文件信息
- `misc`：附加工具和脚本
- `tests`：包含测试用例
- `docs`：项目文档

### 主要组件

- **OCR 处理**：`ocrmypdf/__main__.py` 是命令行入口，处理 OCR 逻辑。
- **插件系统**：`pluginspec.py` 定义了插件与核心功能的交互。
- **PDF 信息提取**：`pdfinfo/info.py` 用于提取和处理 PDF 文件的信息。

## 技术栈

- 编程语言：Python
- 依赖库：`pikepdf`, `pdfminer.six`, `Pillow`, `img2pdf`, `Tesseract`
- 测试框架：`pytest`

## 贡献指南

欢迎贡献！请参阅 `CONTRIBUTING.md` 文件了解详细的贡献流程和指南。

## 许可证

本项目采用 [Mozilla Public License 2.0](https://opensource.org/licenses/MPL-2.0)。有关详细信息，请查看 `LICENSE` 文件。
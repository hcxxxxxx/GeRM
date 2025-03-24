# IronRDP

IronRDP是一个功能强大的远程桌面协议（RDP）实现，旨在提供高效的远程桌面访问和控制。该项目采用多种技术栈，包括Rust、TypeScript、HTML和CSS，旨在实现高性能、可扩展和安全的远程桌面服务。

## 主要特性

- 支持多种RDP功能，包括输入事件处理、显示更新和音频服务。
- 提供现代化的客户端和服务器实现，支持TLS加密。
- 包含示例和测试套件，以确保代码的可靠性和稳定性。
- 提供Web和桌面客户端解决方案，适用于不同的使用场景。

## 安装说明

1. 确保你已安装Rust和Cargo。
2. 克隆此仓库：
   ```bash
   git clone https://github.com/yourusername/IronRDP.git
   cd IronRDP
   ```
3. 安装依赖：
   ```bash
   cargo build
   ```
4. 运行示例服务器：
   ```bash
   cargo run --bin example_server
   ```

## 使用示例

在`crates/ironrdp/examples/server.rs`中，你可以找到如何使用`ironrdp-server` crate来创建一个RDP服务器的示例。通过简单的命令行参数配置，你可以快速启动并运行一个RDP服务。

```rust
fn main() {
    // 解析命令行参数
    let args = parse_args();
    setup_logging();
    
    // 启动服务器
    let server = RdpServer::new(args.bind_addr);
    server.run();
}
```

## 项目架构

IronRDP主要分为以下几个模块：

- **ironrdp-server**: 实现RDP服务器，负责监听连接、处理输入事件和显示更新。
- **ironrdp-client**: 提供RDP客户端实现，支持图形界面和输入事件。
- **ironrdp-pdu**: 定义协议数据单元（PDU），用于RDP中的数据传输。
- **ironrdp-dvc**: 实现动态虚拟通道（DRDYNVC）功能。
- **ironrdp-displaycontrol**: 处理显示控制相关的消息和布局。
- **ironrdp-svc**: 管理静态虚拟通道的通信。

## 技术栈

- **Rust**: 作为主要编程语言，以其内存安全、并发和高性能特点著称。
- **TypeScript**: 用于Web客户端的开发，提供类型安全的JavaScript代码。
- **HTML/CSS**: 用于构建用户界面。
- **tokio**: 异步运行时，用于处理并发任务。

## 贡献指南

欢迎对IronRDP进行贡献！请遵循以下步骤：

1. Fork本仓库。
2. 创建新的特性分支：
   ```bash
   git checkout -b feature/YourFeature
   ```
3. 提交你的更改：
   ```bash
   git commit -m 'Add some feature'
   ```
4. 推送到分支：
   ```bash
   git push origin feature/YourFeature
   ```
5. 提交Pull Request。

## 许可证

本项目根据Apache 2.0和MIT许可证发布。有关详细信息，请查看LICENSE-APACHE和LICENSE-MIT文件。
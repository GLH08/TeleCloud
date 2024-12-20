# TeleCloud

一个基于 Telegram 机器人的云存储解决方案，支持自动将文件上传至 OneDrive。

## 目录
- [功能特点](#功能特点)
- [系统要求](#系统要求)
- [快速开始](#快速开始)
- [详细配置](#详细配置)
- [使用指南](#使用指南)
- [开发指南](#开发指南)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 功能特点

### 核心功能
- ✨ 通过 Telegram 机器人接收文件
- 📤 自动上传文件至 OneDrive
- 🔗 生成文件分享链接
- 📊 查看存储统计信息

### 高级特性
- 🔐 用户权限管理
- ⚡ 文件自动备份
- 📝 详细的操作日志
- 🚀 支持大文件断点续传

## 系统要求

### 环境依赖
- Docker 20.10+
- Docker Compose 2.0+
- 80 端口（可选，用于 OAuth2 回调）

### 第三方服务
- Telegram Bot Token
- OneDrive API 凭据
  - Client ID
  - Client Secret
  - Redirect URI

### 硬件推荐配置
- CPU: 1 核心+
- 内存: 1GB+
- 存储: 10GB+

## 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/telecloud.git
cd telecloud

### 2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息

### 3. 启动服务
docker-compose up -d

### 4. 初始化数据库
docker-compose exec telecloud python scripts/init_db.py

## 详细配置
### 环境变量说明
```bash
# Bot 配置
BOT_TOKEN=your_telegram_bot_token
ADMIN_USER_IDS=123456,789012

# OneDrive 配置
ONEDRIVE_CLIENT_ID=your_client_id
ONEDRIVE_CLIENT_SECRET=your_client_secret


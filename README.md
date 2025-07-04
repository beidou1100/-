# Telegram ChatGPT Bot

## 简介
这是一个基于 python-telegram-bot 和 OpenAI GPT-3.5 的 Telegram 机器人，支持中文多轮对话。

## 部署步骤
1. 在 Telegram 使用 @BotFather 创建机器人，获取 BOT_TOKEN。
2. 在 OpenAI 官网注册账号，获取 OPENAI_API_KEY。
3. Fork 或上传本项目到你的 GitHub 仓库。
4. 在 GitHub 仓库设置 Secrets，添加 BOT_TOKEN 和 OPENAI_API_KEY。
5. 推送代码到 main 分支，GitHub Actions 会自动部署并运行机器人。

## 运行与使用
- 在 Telegram 搜索你的机器人，发送 /start 开始对话。
- 机器人支持多轮上下文，输入问题即可得到回答。

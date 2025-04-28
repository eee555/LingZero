# LingZero

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![UI](https://img.shields.io/badge/UI-PySide6-lightgrey.svg)
![Lines of Code](https://img.shields.io/badge/code-~300_lines-orange.svg)


> 离线翻译 & 截屏翻译，轻巧强大，作者自用！

LingZero 能够为你带来截屏翻译 + 离线翻译的极致体验！没有复杂配置，没有联网等待，一切都在本地悄然完成，真正做到极简、无感、丝滑流畅。

告别卡顿、告别跳转，LingZero 利用本地计算资源，释放出超越在线 API 的翻译速度。**点一下、截个图，翻译就来了！**这不仅是工具，这是打破语言壁垒的一把快刀。

## ✨ 核心功能

- 🚀 **开箱即用**：无需安装，也无需配置环境，直接运行。
- 📸 **截屏翻译**：快速截图识别 + 翻译（基于 [pytesseract](https://github.com/madmaze/pytesseract)）。
- 📋 **复制翻译**：复制即翻译，提升阅读效率。
- 💎 **词典翻译**：翻译单个词语时，首选调用词典翻译，直接查询本地词典，包含690000个单词或短语（基于[ECDICT](https://github.com/skywind3000/ECDICT)）。
- 🧠 **离线翻译**：翻译段落或句子时，集成深度学习翻译引擎（基于 [Argos Translate](https://github.com/argosopentech/argos-translate)）。
- 🐧 **腾讯翻译**：翻译段落或句子时，假如联网，还能调用腾讯翻译（每月500万字免费），自动优化翻译结果。

## ✅ 推荐使用场景

- 阅读英文新闻、论文、技术文档等。

## ❌ 不推荐使用场景

- 中文 ➝ 英文 翻译（通常使用聊天机器人）。
- 英文 ➝ 非中文 翻译（本人只使用中文）。

## 💻 系统兼容

- Windows 10 / 11

## 👣 安装步骤

1. 从[发行版](https://github.com/eee555/LingZero/releases)下载最新版，解压后放到合适的位置。
2. 假如要使用腾讯翻译，新建"secret.ini"文件如下，前往[腾讯云官网](https://console.cloud.tencent.com/cam/capi)免费领取个人令牌，并写在文件中。
```
[DEFAULT]
tencent_secret_id  = A*********************************ZO
tencent_secret_key = e******************************p
```

##  📈 效果展示

<img src="pic/2.png" alt="" width="300">

## 📦 TODO / 开发计划

- UI 优化，根据文档背景颜色，自动调整窗口背景颜色

欢迎 Star ⭐、Fork 🍴 或提 Issue 🚀，一起打造更丝滑的离线翻译体验！

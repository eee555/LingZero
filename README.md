# LingZero

[![](https://img.shields.io/github/release/eee555/LingZero.svg)](https://github.com/eee555/LingZero/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![UI](https://img.shields.io/badge/UI-PySide6-lightgrey.svg)
[![pytesseract](https://img.shields.io/badge/Powered_by-pytesseract-brightgreen)](https://github.com/madmaze/pytesseract)
[![ECDICT](https://img.shields.io/badge/Powered_by-ECDICT-brightgreen)](https://github.com/skywind3000/ECDICT)
[![Argos_Translate](https://img.shields.io/badge/Powered_by-Argos_Translate-brightgreen)](https://github.com/argosopentech/argos-translate)
[![](https://img.shields.io/github/downloads/eee555/LingZero/total.svg)](https://github.com/eee555/LingZero/releases)

> 离线翻译 & 截屏翻译 & 复制翻译，轻巧强大，作者自用！

由于市面上的翻译软件越做越烂，作者一怒之下开发出了自用的翻译软件——LingZero！

卡片式悬浮窗设计，可以任意拖动，点击窗口外部即可关闭。截屏翻译+离线翻译+复制翻译，无需注册登录、无需充会员，真正做到极简、无感、丝滑流畅。左键点击即可对比原文和译文，右键复制文本。0切屏、0等待，保护心流状态，完全为英文文献阅读而设计！

## ✨ 核心功能

- 🚀 **开箱即用**：无需安装，也无需配置环境，直接运行。
- 🛸 **卡片式悬浮窗**：左键可以任意拖动，点击周围即可关闭，点击切换原文和译文。
- 📸 **截屏翻译**：快速截图识别 + 翻译（基于 [pytesseract](https://github.com/madmaze/pytesseract)）。
- 📋 **复制翻译**：复制即翻译，提升阅读效率。
- 💎 **词典翻译**：翻译单个词语（或短语）时，首选调用词典翻译，直接查询本地词典，包含690000个单词或短语（基于[ECDICT](https://github.com/skywind3000/ECDICT)）。
- 🧠 **离线翻译**：翻译段落或句子时，集成深度学习翻译引擎（基于 [Argos Translate](https://github.com/argosopentech/argos-translate)）。
- 🐧 **腾讯翻译**：翻译段落或句子时，假如联网，还能调用腾讯翻译（每月500万字免费，含标点），自动优化翻译结果。
- 💨 **中文改写英文**：选中一段可编辑的中文文本，按下快捷键，就可以直接将其改为英文，并且剪贴板同步修改。假如要用英文关键词搜索、回帖，非常方便。此功能必须联网使用。
- 🚗 **关键性能**：占用磁盘约800M、内存700M。翻译单词可瞬时出结果；翻译段落时，首次翻译延时约3秒、之后每次延时约1秒。

\* *使用教程及快捷键配置见`config.ini`，如不习惯可自行修改*

## 💯 翻译质量

以 Attention Is All You Need 前三句话为例：

> The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.

将各个软件的翻译结果列举如下，供用户对比：

LingZero-腾讯api：主要的序列转换模型基于复杂的循环或卷积神经网络，其中包括编码器和解码器。性能最好的模型还通过注意力机制连接编码器和解码器。我们提出了一个新的简单的网络架构，Transformer，完全基于注意力机制，完全免除递归和卷积。

LingZero-离线：主导序列转录模型基于复杂的反复或演化神经网络,其中包括一个编码器和一个解码器. 性能最好的模型也通过注意机制连接编码器和解码器. 我们提出一个新的简单的网络架构,即变形器, 完全基于关注机制, 完全不重复和演变。

Chatgpt 3.5：主流的序列转换模型通常基于复杂的循环神经网络（RNN）或卷积神经网络（CNN），这些模型包括一个编码器和一个解码器。性能最好的模型还通过注意力机制将编码器和解码器连接起来。我们提出了一种全新的、结构简单的网络架构——Transformer，它完全基于注意力机制，彻底摒弃了循环和卷积结构。

Deepseek-R1：主流的序列转导模型基于复杂的循环或卷积神经网络，这些网络通常包含编码器和解码器结构。性能最佳的模型还通过注意力机制连接编码器和解码器。我们提出了一种名为Transformer的新型简单网络架构，该架构完全基于注意力机制，彻底舍弃了循环与卷积结构。

文心一言4.5：主流的序列转换模型基于复杂的循环神经网络或卷积神经网络构建，这些网络包含编码器（encoder）和解码器（decoder）两部分。性能最优的模型还通过注意力机制（attention mechanism）将编码器和解码器连接起来。我们提出了一种全新的简单网络架构——Transformer，它完全基于注意力机制构建，彻底摒弃了循环结构和卷积操作。

有道翻译：主流的序列转换模型基于复杂的循环神经网络或卷积神经网络，这些网络包含编码器和解码器。表现最佳的模型还通过注意力机制将编码器和解码器连接起来。我们提出了一种新的简单网络架构——Transformer，它完全基于注意力机制，摒弃了循环和卷积。

Deepl：主导的序列转换模型基于复杂的循环或卷积神经网络，这些网络包含编码器和解码器。性能最佳的模型还通过注意力机制将编码器和解码器连接起来。我们提出了一种新的简单网络架构——Transformer，该架构仅基于注意力机制，完全摒弃了循环和卷积。

## ✅ 推荐使用的场景或用户

- 希望阅读英文新闻，缩小语言问题带来的信息差。
- 需要阅读英文文献的科研人员等。
- 需要阅读技术文档的工程师、程序员等。
- 中文 ➝ 英文的一般质量翻译。
- 内网电脑使用的场景。

## ❌ 不推荐使用的场景或用户

- 中文 ➝ 英文的SCI写作级超高质量翻译（通常使用聊天机器人）。
- 英文 ➝ 非中文 翻译（本人只使用中文）。
- 排斥使用快捷键的用户，部分功能只能快捷键触发。
- 受限于开发条件，暂时不支持多屏幕（需要帮助）。
- 非Windows 10 / 11的操作系统。

## 👣 安装步骤

1. 从[发行版](https://github.com/eee555/LingZero/releases)下载最新版，解压后放到合适的位置。
2. 假如要使用腾讯翻译，打开"secret.ini"文件如下，前往[腾讯云官网](https://console.cloud.tencent.com/cam/capi)免费领取个人令牌，并填写在文件中。
```
[DEFAULT]
tencent_secret_id  = A*********************************ZO
tencent_secret_key = e******************************p
tencent_region = ap-shanghai
```

##  📈 效果展示

- 截屏翻译大段段落
![截屏翻译](./pic/2.png)

- 词典翻译，详细解释单词的多种含义，复制或截屏均可启用
![词典翻译](./pic/3.png)

## 📦 TODO / 开发计划

- UI 优化，根据文档背景颜色，自动调整窗口背景颜色
- 接入百度、谷歌、阿里巴巴等翻译api

欢迎 Star ⭐、Fork 🍴 或提 Issue 🚀，一起打造更丝滑的离线翻译体验！

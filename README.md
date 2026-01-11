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

- 🚀 **开箱即用**：无需安装，也无需配置环境，直接运行。自动创建默认配置文件。
- 🛸 **卡片式悬浮窗**：左键可以任意拖动，点击周围即可关闭。左键点击切换原文和译文，右键点击可以将弹窗切换为“可选择”模式。
- 📸 **截屏翻译**：快速截图识别 + 翻译（基于 [pytesseract](https://github.com/madmaze/pytesseract)），支持多屏幕。
- 📋 **复制翻译**：复制即翻译，提升阅读效率。
- 💎 **词典翻译**：翻译单个词语（或短语）时，调用词典翻译，直接查询本地词典，包含690000个单词或短语（基于[ECDICT](https://github.com/skywind3000/ECDICT)）。
- 🧠 **离线翻译**：翻译段落或句子时，集成深度学习翻译引擎（基于 [Argos Translate](https://github.com/argosopentech/argos-translate)）。
- 🐧 **腾讯翻译**：翻译段落或句子时，假如联网，还能调用腾讯翻译（每月500万字免费，含标点，默认设置下超出不偷偷扣费），自动优化翻译结果。
- 🤖 **DeepSeek API翻译**：支持接入DeepSeek API进行翻译，可自定义翻译提示词，提供高质量翻译。
- 💨 **中文改写英文**：选中一段可编辑的中文文本，按下快捷键，就可以直接将其改为英文，并且剪贴板同步修改。假如要用英文关键词搜索、回帖，非常方便。此功能必须联网使用。
- 🚗 **关键性能**：占用磁盘约800M、内存700M。翻译单词可瞬时出结果；翻译段落时，首次翻译延时约3秒、之后每次延时约1秒。
- 🔍 **调试功能**：提供详细的翻译过程调试信息输出。

* *使用教程及快捷键配置见`config.ini`，如不习惯可自行修改*

## 💯 翻译质量测评

以 `Attention Is All You Need` 前三句话为例：

> The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.

将各个软件的翻译结果列举如下，供用户对比：

- LingZero-腾讯api：主要的序列转换模型基于复杂的循环或卷积神经网络，其中包括编码器和解码器。性能最好的模型还通过注意力机制连接编码器和解码器。我们提出了一个新的简单的网络架构，Transformer，完全基于注意力机制，完全免除递归和卷积。

- LingZero-离线：主导序列转录模型基于复杂的反复或演化神经网络,其中包括一个编码器和一个解码器. 性能最好的模型也通过注意机制连接编码器和解码器. 我们提出一个新的简单的网络架构,即变形器, 完全基于关注机制, 完全不重复和演变。

- 有道翻译：主流的序列转换模型基于复杂的循环神经网络或卷积神经网络，这些网络包含编码器和解码器。表现最佳的模型还通过注意力机制将编码器和解码器连接起来。我们提出了一种新的简单网络架构——Transformer，它完全基于注意力机制，摒弃了循环和卷积。

- Deepl：主导的序列转换模型基于复杂的循环或卷积神经网络，这些网络包含编码器和解码器。性能最佳的模型还通过注意力机制将编码器和解码器连接起来。我们提出了一种新的简单网络架构——Transformer，该架构仅基于注意力机制，完全摒弃了循环和卷积。

- 文心一言4.5：主流的序列转换模型基于复杂的循环神经网络或卷积神经网络构建，这些网络包含编码器（encoder）和解码器（decoder）两部分。性能最优的模型还通过注意力机制（attention mechanism）将编码器和解码器连接起来。我们提出了一种全新的简单网络架构——Transformer，它完全基于注意力机制构建，彻底摒弃了循环结构和卷积操作。

- Chatgpt 3.5：主流的序列转换模型通常基于复杂的循环神经网络（RNN）或卷积神经网络（CNN），这些模型包括一个编码器和一个解码器。性能最好的模型还通过注意力机制将编码器和解码器连接起来。我们提出了一种全新的、结构简单的网络架构——Transformer，它完全基于注意力机制，彻底摒弃了循环和卷积结构。

- Deepseek-R1：主流的序列转导模型基于复杂的循环或卷积神经网络，这些网络通常包含编码器和解码器结构。性能最佳的模型还通过注意力机制连接编码器和解码器。我们提出了一种名为Transformer的新型简单网络架构，该架构完全基于注意力机制，彻底舍弃了循环与卷积结构。

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
- 非Windows 10 / 11的操作系统。

## 👣 安装步骤

1. 从[发行版](https://github.com/eee555/LingZero/releases)下载最新版，解压后放到合适的位置。
2. 打开LingZero文件夹，打开config.ini，按照习惯的配置自行修改键位。
3. 【推荐】右键`translation.exe`，点击`显示更多选项`->`固定到任务栏`。
4. 【可选】配置翻译API（腾讯翻译或DeepSeek API）：
   - **腾讯翻译**：打开"secret.ini"文件，前往[腾讯云官网](https://console.cloud.tencent.com/cam/capi)免费领取个人令牌，并填写在文件中。
   - **DeepSeek API**：在"secret.ini"文件中添加 `deepseek_api_key` 字段，填入您的DeepSeek API Key，并在config.ini中自定义翻译提示词。

```ini
[DEFAULT]
tencent_secret_id = A*********************************ZO
tencent_secret_key = e******************************p
tencent_region = ap-shanghai
deepseek_api_key = 
```

## 🔧 deepseek 提示词推荐

1. 请将以下英文文本翻译成中文，保持原意不变，尽量简洁。
2. 请将以下英文文本翻译成中文，保持原意不变，对于专业名词和缩写，保持原有的英文名称。
3. 专注于意译翻译，旨在捕捉不仅仅是文字，而是背后的意义和语调。确保在目标语言中传达原文的精髓，确保文化细微差别和隐含意义不会在翻译中丢失。
4. 请将以下英文文本翻译成中文，保持原意不变，尽量简洁，并将英文关键词保留并在括号中显示中文翻译，帮助用户加深对词汇的记忆。
5. 老铁，把下面这段洋文给我整成东北话，意思别整岔劈了，能省字儿就省字儿，听着得劲儿就行！
6. 你是一个英语阅读助手。假设你的用户雅思成绩为5分。当用户发送文本时，请为文本中你认为用户可能感到困惑的单词和短语提供中文注释。注释应包含单词原文、音标和翻译。使用以下格式：单词 /音标/ 翻译

##  📈 效果展示

- 截屏翻译大段段落
![截屏翻译](./pic/2.png)

- 词典翻译，详细解释单词的多种含义，复制或截屏均可启用
![词典翻译](./pic/3.png)

## 📦 TODO / 开发计划

- UI 优化，根据文档背景颜色，自动调整窗口背景颜色
- 接入百度、谷歌、阿里巴巴等翻译api
- 钩子定时重启
- 拆分功能
- 统一设置页面
- 翻译优先级调整
- 修复多屏幕拖动时被windos调整大小的bug
- 完整的多屏幕（跨屏幕）支持
- 自定义字体
- 看看底下项目依赖信息有啥不需要的给它去掉



# 项目依赖信息

## Python 环境信息

### 虚拟环境
- **虚拟环境位置**: `c:\Users\jim\git\LingZero\.venv`
- **Python 版本**: 3.12.0
- **pip 版本**: 25.3

## 核心依赖包（此为我的依赖，实际上可以精简）

| 包名 | 版本 | 用途 |
|------|------|------|
| **PySide6** | 6.10.1 | Qt for Python - 跨平台 GUI 框架，用于创建桌面应用程序 |
| **PySide6_Addons** | 6.10.1 | PySide6 附加组件，提供额外的功能扩展 |
| **PySide6_Essentials** | 6.10.1 | PySide6 核心组件包，包含基础功能 |
| **shiboken6** | 6.10.1 | PySide6 的 C++ 绑定工具，用于 Python 和 C++ 代码互操作 |
| **pytesseract** | 0.3.13 | OCR 光学字符识别库，用于识别图像中的文字 |
| **Pillow** | 12.1.0 | 图像处理库，用于图像加载、处理和保存 |
| **pynput** | 1.8.1 | 键盘和鼠标控制库，用于监控和控制输入设备 |
| **keyboard** | 0.13.5 | 键盘事件监听和控制库，提供键盘操作接口 |
| **argostranslate** | 1.10.0 | 机器翻译库，支持多种语言互译 |
| **pyperclip** | 1.11.0 | 剪贴板操作库，用于读取和写入剪贴板内容 |

## 翻译引擎相关依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| **spacy** | 3.8.11 | 自然语言处理库，用于文本处理和分析 |
| **spacy-legacy** | 3.0.12 | SpaCy 旧版本兼容性支持 |
| **spacy-loggers** | 1.0.5 | SpaCy 日志记录工具 |
| **thinc** | 8.3.10 | SpaCy 使用的深度学习库，用于自然语言处理任务 |
| **stanza** | 1.10.1 | 斯坦福大学开发的自然语言处理工具包 |
| **ctranslate2** | 4.6.3 | 高效的神经机器翻译库 |
| **torch** | 2.9.1 | PyTorch 深度学习框架，用于训练和推理神经网络 |
| **sacremoses** | 0.1.1 | Moses 机器翻译工具的 Python 实现 |
| **sentencepiece** | 0.2.1 | 句子分词工具，用于处理多语言文本 |

## 基础依赖库

| 包名 | 版本 | 用途 |
|------|------|------|
| **numpy** | 2.4.1 | 数值计算库，提供数组和矩阵运算支持 |
| **Pillow** | 12.1.0 | 图像处理库（重复项，核心依赖中已列出） |
| **requests** | 2.32.5 | HTTP 请求库，用于与网络服务交互 |
| **PyYAML** | 6.0.3 | YAML 文件解析库，用于配置文件处理 |
| **Jinja2** | 3.1.6 | 模板引擎，用于生成 HTML、XML 等文档 |
| **MarkupSafe** | 3.0.3 | 安全字符串处理库，用于防止 XSS 攻击 |
| **protobuf** | 6.33.3 | Protocol Buffers 序列化库，用于数据交换 |
| **pydantic** | 2.12.5 | 数据验证库，用于类型注解和数据校验 |
| **pydantic_core** | 2.41.5 | Pydantic 的核心实现库 |

## 工具和辅助库

| 包名 | 版本 | 用途 |
|------|------|------|
| **tqdm** | 4.67.1 | 进度条库，用于显示任务执行进度 |
| **colorama** | 0.4.6 | 控制台颜色输出库，用于美化控制台显示 |
| **emoji** | 2.15.0 | 表情符号处理库，支持 emoji 字符操作 |
| **click** | 8.3.1 | 命令行接口创建库，用于构建 CLI 应用程序 |
| **urllib3** | 2.6.3 | HTTP 客户端库，提供高级网络功能 |
| **charset-normalizer** | 3.4.4 | 字符编码检测和转换库 |
| **idna** | 3.11 | 国际域名系统 (IDN) 处理库 |
| **certifi** | 2026.1.4 | CA 证书库，用于 SSL 证书验证 |
| **packaging** | 25.0 | 包管理工具，用于处理包的元数据和依赖关系 |
| **setuptools** | 80.9.0 | Python 包安装和分发工具 |
| **joblib** | 1.5.3 | 并行计算和任务调度库，用于提高计算效率 |

## 自然语言处理相关依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| **catalogue** | 2.0.10 | 目录管理库，用于管理自然语言处理资源 |
| **cymem** | 2.0.13 | 内存管理库，用于优化 Python 的内存使用 |
| **murmurhash** | 1.0.15 | 哈希函数库，用于高效的字符串哈希计算 |
| **preshed** | 3.0.12 | 哈希表库，用于快速的键值对存储和查找 |
| **srsly** | 2.5.2 | 数据序列化库，用于处理 JSON、YAML、msgpack 等格式 |
| **wasabi** | 1.1.3 | 轻量级的控制台输出美化库 |
| **weasel** | 0.4.3 | 工具库，用于开发和训练自然语言处理模型 |
| **smart-open** | 7.5.0 | 统一的文件访问接口，支持本地文件、HTTP、S3 等 |
| **cloudpathlib** | 0.23.0 | 云存储文件操作库，支持 AWS S3、Azure Blob 等 |

## 数学和科学计算库

| 包名 | 版本 | 用途 |
|------|------|------|
| **sympy** | 1.14.0 | 符号计算库，用于代数和微积分计算 |
| **mpmath** | 1.3.0 | 多精度数学计算库，支持高精度数值运算 |
| **networkx** | 3.6.1 | 图论和网络分析库 |
| **filelock** | 3.20.3 | 文件锁定库，用于处理并发访问问题 |
| **fsspec** | 2026.1.0 | 文件系统规范库，提供统一的文件系统接口 |

---

# 运行（自己替换路径）

1. 安装 D:\Tesseract-OCR （可以发行版找到tesseract文件夹，改名为Tesseract-OCR放在d盘）

2. cd C:\Users\jim\git\LingZero ; .\.venv\Scripts\activate ; python main.py


# 编译打包 （自己替换路径）

## 前提 （自己替换路径）
1. 下载发行版
2. 激活安装依赖的venv环境

## 打包指令（自己替换路径）

cd "c:\Users\jim\git\LingZero"; python -m PyInstaller -w main.py -i "./a.ico" --add-data "./config.ini;." --onedir --noconfirm --name translation

## 打包后（此步取决于你的spec有没有复制文件） （自己替换路径）
1. 发行版找到tesseract文件夹，放在C:\Users\jim\git\LingZero\dist\translation\
2. 发行版找到translate-en_zh-1_9.argosmodel，ecdict.json ,a.ico文件，放在C:\Users\jim\git\LingZero\dist\translation


欢迎 Star ⭐、Fork 🍴 或提 Issue 🚀，一起打造更丝滑的离线翻译体验！

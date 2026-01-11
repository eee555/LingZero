# -*- coding: utf-8 -*-
# DeepSeek API 翻译器封装
# 使用 DeepSeek API 进行文本翻译
# 使用聊天模型实现翻译功能
import json
import http.client


class Trans:
    def __init__(self, secret_config, config):
        """
        初始化 DeepSeek 翻译器
        :param secret_config: 配置解析器，用于获取 API Key
        :param config: 配置解析器，用于获取翻译提示词
        """
        self.secret_config = secret_config
        self.config = config
        self.api_key = self.secret_config.get('DEFAULT', 'deepseek_api_key')
        
        # 从配置文件中获取翻译提示词，默认值为预设的提示词
        self.prompt_en_to_zh = self.config.get('DEFAULT', 'deepseek_trans_prompt_en_to_zh', fallback='请将以下英文文本翻译成中文，保持原意不变，尽量简洁：')
        
        # 去除可能存在的引号
        self.prompt_en_to_zh = self.prompt_en_to_zh.strip('"').strip("'")
    
    def translate(self, input_text: str, target="zh") -> str:
        """
        使用 DeepSeek API 翻译文本
        :param input_text: 要翻译的文本
        :param target: 目标语言，默认为中文（zh）
        :return: 翻译后的文本，若 API Key 为空或翻译失败则返回空字符串
        """
        # 如果 API Key 为空，则不进行翻译
        if not self.api_key:
            return ""
            
        # 构造翻译提示词
        if target == "zh":
            prompt = f"{self.prompt_en_to_zh}\n{input_text}"

        else:
            return ""
            
        # 构造请求
        conn = http.client.HTTPSConnection("api.deepseek.com")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = json.dumps({
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,
            "max_tokens": 1000
        })
        
        try:
            conn.request("POST", "/v1/chat/completions", payload, headers)
            res = conn.getresponse()
            data = res.read()
            result = json.loads(data.decode("utf-8"))
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"].strip()
            else:
                return ""
                
        except Exception as e:
            print(f"DeepSeek translation failed: {e}")
            return ""
        finally:
            conn.close()

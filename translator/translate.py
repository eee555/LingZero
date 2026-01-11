import configparser
import concurrent.futures
from typing import List, Callable
from . import ecdict, tencent, argos, deepseek
from threading import Thread

class ResultThread(Thread):
    def __init__(self, func, args):
        super().__init__()
        self.func = func
        self.args = args
        self.result = None

    def run(self):
        # 在线程启动时执行传入的函数，并保存结果
        self.result = self.func(*self.args)

    def join(self):
        # 等待线程执行完毕，并返回结果
        super().join()
        return self.result
    
# 太长或太短，或英文占比没有达到60%，都不翻译
def is_translation_needed(text, target = "zh") -> bool:
    total_chars = len(text)
    if not text or total_chars > 10000:
        return False
    # 复制了文件
    if r"///" in text:
        return False
    if target == "zh":
        english_chars = sum(1 for char in text if char.isalpha() and ('a' <= char.lower() <= 'z'))
        percentage = english_chars / total_chars
        return percentage >= 0.6
    elif target == "en":
        english_chars = sum(1 for char in text if char.isalpha() and ('a' <= char.lower() <= 'z'))
        percentage = english_chars / total_chars
        return percentage <= 0.4

def data_cleaning(text: str) -> List[str]:
    fragments = text.split("\n\n")
    for (idt, text) in enumerate(fragments):
        fragments[idt] = text.replace("\n", " ").strip("' \"[](){}")
    return fragments

def super_translater(translate: Callable[[str], str], fragments: List[str],
                      callback: Callable[[str, int], None], priority_level: int):
    threads: List[ResultThread] = []
    for fragment in fragments:
        threads.append(ResultThread(func=translate, args=(fragment,)))
    for thread in threads:
        thread.start()
    results = []
    for thread in threads:
        results.append(thread.join())
    result = "\n\n".join(results).strip()
    if result and not result.isascii():
        callback(result, priority_level)
    
class Translator():
    def __init__(self):
        self.secret_config = configparser.ConfigParser()
        self.secret_config.read('secret.ini', encoding="utf-8")
        
        self.config = configparser.ConfigParser()
        self.config.read('config.ini', encoding="utf-8")
        
        self.ecdict_trans = ecdict.Trans()
        self.tencent_trans = tencent.Trans(self.secret_config)
        self.argos_trans = argos.Trans()
        self.deepseek_trans = deepseek.Trans(self.secret_config, self.config)

    def set_ui(self, ui):
        self.ui = ui

    def notify(self, text: str, priority_level: int):
        # 调试信息：打印翻译结果和优先级
        print(f"翻译结果（优先级 {priority_level}）: {text}")
        self.ui.update_result(text, priority_level)

    # 翻译英文段落、单词为中文，结果为空表明不满足翻译要求
    def translate(self, text) -> bool:
        # 调试信息：打印原始文本
        print(f"原始文本: {text}")
        
        if not is_translation_needed(text):
            print("文本不满足翻译要求")
            return False
            
        text_list = data_cleaning(text)
        print(f"清洗后的文本片段: {text_list}")
        
        if len(text_list) == 1:
            if trans_result := self.ecdict_trans.translate(text_list[0]):
                print(f"词典翻译结果: {trans_result}")
                self.notify(trans_result, 1)
                return True

        # 翻译优先级：离线翻译(4) > 腾讯翻译(3) > DeepSeek(2) > 词典翻译(1)，优先级越低越优先
        print("开始多线程翻译...")
        argos_thread = ResultThread(func=super_translater, 
                                    args=(self.argos_trans.translate, text_list, self.notify, 4))
        tencent_thread = ResultThread(func=super_translater, 
                                      args=(self.tencent_trans.translate, text_list, self.notify, 3))
        deepseek_thread = ResultThread(func=super_translater, 
                                       args=(self.deepseek_trans.translate, text_list, self.notify, 2))
        argos_thread.start()
        tencent_thread.start()
        deepseek_thread.start()
        argos_thread.join()
        tencent_thread.join()
        deepseek_thread.join()
        
        print("翻译完成")
        return True


import configparser
import concurrent.futures
from typing import List
from . import ecdict, tencent, argos

# 太长或太短，或英文占比没有达到60%，都不翻译
def is_translation_needed(text) -> bool:
    total_chars = len(text)
    if not text or total_chars > 10000:
        return False
    # 复制了文件
    if r"///" in text:
        return False
    english_chars = sum(1 for char in text if char.isalpha() and ('a' <= char.lower() <= 'z'))
    percentage = english_chars / total_chars
    return percentage >= 0.6

def data_cleaning(text: str) -> List[str]:
    texts = text.split("\n\n")
    for (idt, text) in enumerate(texts):
        texts[idt] = text.replace("\n", " ").strip("' \"[](){}")
    return texts
    
class Translator():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('secret.ini', encoding="utf-8")
        self.ecdict_trans = ecdict.Trans()
        self.tencent_trans = tencent.Trans(self.config)
        self.argos_trans = argos.Trans()

    def set_ui(self, ui):
        self.ui = ui

    def notify(self, text: str):
        self.ui.update_result(text)

    # 翻译段落、单词，结果为空表明不满足翻译要求
    def translate(self, text) -> bool:
        if not is_translation_needed(text):
            return False
        text_list = data_cleaning(text)
        if len(text_list) == 1:
            if trans_result := self.ecdict_trans.translate(text_list[0]):
                self.notify(trans_result)
                return True
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures_online = []
            futures_local = []
            for t in text_list:
                future = executor.submit(self.tencent_trans.translate, t)
                futures_online.append(future)
            for t in text_list:
                future = executor.submit(self.argos_trans.translate, t)
                futures_local.append(future)
            online_result = ""
            local_result = ""
            for future in futures_local:
                r = future.result()
                local_result += r + "\n\n"
            local_result = local_result.strip()
            self.notify(local_result)
            for future in futures_online:
                r = future.result()
                online_result += r + "\n\n"
            online_result = online_result.strip()
            if not online_result.isascii():
                self.notify(online_result)
            return True



import json

class Trans():
    def __init__(self):
        with open("./ecdict.json", 'r', encoding='utf-8') as f:
            self.ecdict = json.load(f)
    def translate(self, text: str) -> str:
        if text in self.ecdict:
            translated_text = self.ecdict[text].replace("\\n", "\n")
            return translated_text
        else:
            return ""

from argostranslate import translate

class Trans():
    def __init__(self):
        langs = translate.get_installed_languages()
        if not langs:
            from argostranslate import package
            model_path = './translate-en_zh-1_9.argosmodel'  # 替换为你的模型文件路径
            package.install_from_path(model_path)
            langs = translate.get_installed_languages()
        source_lang = next(filter(lambda x: x.code == 'en', langs))
        target_lang = next(filter(lambda x: x.code == 'zh', langs))
        self.translator = source_lang.get_translation(target_lang)
    def translate(self, text: str) -> str:
        try:
            return self.translator.translate(text)
        except:
            return ""

from transformers import pipeline

class Translator:
    def __init__(self):
        self.model = pipeline("translation_en_to_fr", model='t5-small', device='cuda:0')

    def translate(self, text:str) -> str:
        model_output = self.model(text)
        translation = model_output[0]['translation_text']
        return translation
    
if __name__ == '__main__':
    translator = Translator()
    translation = translator.translate("Hello world!")
    print(translation)
        
from googletrans import Translator

translator = Translator()

async def translate_text(text, dest_language='en'):
    translated = translator.translate(text, dest=dest_language)
    return translated.text

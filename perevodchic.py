from translate import Translator
translator= Translator(from_lang="English",to_lang="russian")
text_Eng = input("Входное сообщение")
text_Rus = translator.translate(text_Eng)
perevod=text_Rus
print(perevod)
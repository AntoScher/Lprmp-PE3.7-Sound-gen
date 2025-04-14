from gtts import gTTS
from playsound import playsound
import os
import time

def text_to_speech(text, lang='ru'):
    try:
        tts = gTTS(text=text, lang=lang)
        filename = "output.mp3"  # Исправленное имя
        tts.save(filename)
        print(f"Аудиофайл сохранён как {os.path.abspath(filename)}")
        playsound(filename)
        time.sleep(5)  # Раскомментируйте для задержки перед удалением
        # os.remove(filename)
    except Exception as e:
        print(f"Ошибка: {repr(e)}")

if __name__ == "__main__":
    user_text = input("Введите текст для озвучивания: ")
    if not user_text.strip():
        print("Пустой текст не может быть озвучен.")
    else:
        text_to_speech(user_text)
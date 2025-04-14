from gtts import gTTS
from playsound import playsound
import os
from openai import OpenAI
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()


class DeepSeekPoetryAssistant:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

    def text_to_speech(self, text: str, lang: str = 'ru') -> None:
        """Преобразование текста в речь с удалением временного файла"""
        try:
            tts = gTTS(text=text, lang=lang)
            filename = "deepseek_poem.mp3"
            tts.save(filename)
            print("\n[Аудиофайл генерируется...]")
            playsound(filename)
            os.remove(filename)
        except Exception as e:
            print(f"Ошибка TTS: {e}")

    def generate_poem(self, theme: str) -> str:
        """Генерация стихотворения через DeepSeek API"""
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": "Ты поэт-ассистент. Генерируй стихи на русском языке. Сохраняй ритм и рифму."
                    },
                    {
                        "role": "user",
                        "content": f"Напиши стихотворение на тему: {theme}"
                    }
                ],
                temperature=0.7,
                max_tokens=500,
                stream=False
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Ошибка DeepSeek API: {e}")
            return ""

    def run(self):
        """Основной цикл работы ассистента"""
        print("DeepSeek Poetry Assistant v1.0")
        print("Введите тему для стихотворения или 'выход' для завершения\n")

        while True:
            user_input = input("Тема стиха: ").strip()

            if user_input.lower() in ['выход', 'exit', 'quit']:
                print("До новых встреч!")
                break

            if not user_input:
                print("Пожалуйста, введите тему...")
                continue

            poem = self.generate_poem(user_input)

            if poem:
                print("\n[Сгенерированный стих:]")
                print(poem)
                self.text_to_speech(poem)
            else:
                print("Не удалось создать стихотворение")


if __name__ == "__main__":
    assistant = DeepSeekPoetryAssistant()
    assistant.run()
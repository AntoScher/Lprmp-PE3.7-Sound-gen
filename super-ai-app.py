from gtts import gTTS
from playsound import playsound
import os
from openai import OpenAI
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()


class DeepSeekCreativePoet:
    def __init__(self):
        # Инициализация клиента DeepSeek
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        # Параметры генерации с повышенной креативностью
        self.creativity_settings = {
            "temperature": 0.9,  # Максимальная креативность (0-1)
            "max_tokens": 700,  # Длинные стихи
            "frequency_penalty": 0.5,  # Избегаем повторов
            "presence_penalty": 0.5  # Поощряем новые идеи
        }

    def text_to_speech(self, text: str, lang: str = 'ru') -> None:
        """Преобразует текст в речь с удалением временного файла"""
        try:
            tts = gTTS(text=text, lang=lang)
            filename = "poem.mp3"
            tts.save(filename)
            print("\n🔊 Аудиофайл готов...")
            playsound(filename)
            os.remove(filename)
        except Exception as e:
            print(f"❌ Ошибка TTS: {e}")

    def generate_creative_poem(self, theme: str) -> str:
        """Генерация креативного стихотворения"""
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Ты новатор в поэзии. Создавай стихи с:\n"
                            "- Неожиданными метафорами\n"
                            "- Смелыми рифмами\n"
                            "- Философским подтекстом\n"
                            "Избегай шаблонов!"
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Напиши ультра-креативное стихотворение на тему: '{theme}'. Удиви меня!"
                    }
                ],
                **self.creativity_settings
            )
            poem = response.choices[0].message.content.strip()
            return f"🎭 Стихотворение на тему '{theme}':\n\n{poem}"
        except Exception as e:
            print(f"❌ Ошибка DeepSeek API: {e}")
            return ""

    def run(self):
        """Основной цикл работы"""
        print("\n=== 🚀 DeepSeek Креативный Поэт ===")
        print("Команды: 'выход'/'exit' для завершения\n")

        while True:
            theme = input("🌿 Введите тему стиха: ").strip()

            if theme.lower() in ('выход', 'exit', 'quit'):
                print("\n🖋️ До новых творческих встреч!")
                break

            if not theme:
                print("⚠️ Пожалуйста, введите тему...")
                continue

            print("\n🌀 Генерирую стих...")
            poem = self.generate_creative_poem(theme)

            if poem:
                print(f"\n{poem}")
                self.text_to_speech(poem)
            else:
                print("😔 Не удалось создать стихотворение")


if __name__ == "__main__":
    poet = DeepSeekCreativePoet()
    poet.run()
import os
from dotenv import load_dotenv
from mistralai import Mistral
from mistralai.models import SystemMessage
from .logger import setup_logger
load_dotenv()

logger = setup_logger()

class NeuroAssistant:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY не найден!")

        self.client = Mistral(api_key=self.api_key)
        self.mode = "child"
        self.topic = None
        self.model = "mistral-medium-latest"

        self.system_prompts = {
            "child": """Ты добрый и весёлый помощник для детей 6-8 лет. 

ОБЯЗАТЕЛЬНЫЕ ПРАВИЛА:
1. Отвечай ОЧЕНЬ КРАТКО - максимум 3-4 предложения
2. Используй простые слова, понятные первокласснику
3. Будь позитивным и поддерживающим
4. Добавляй 1-2 подходящих эмодзи
5. Если вопрос сложный - упрости ответ
6. Задавай встречный вопрос, чтобы продолжить диалог

Пример хорошего ответа: "Привет! Рад тебя видеть! 😊 Сегодня был интересный день в школе? Расскажи! 🎒"

Никогда не пиши длинные объяснения!""",

            "parent": """Ты опытный педагог и психолог, помогающий родителям первоклассников.

ОБЯЗАТЕЛЬНЫЕ ПРАВИЛА:
1. Отвечай КОНКРЕТНО и ПРАКТИЧЕСКИ - 4-5 предложений максимум
2. Давай чёткие, выполнимые советы
3. Будь поддерживающим, но профессиональным
4. Используй маркированные списки только если очень нужно
5. Предлагай простые упражнения/действия
6. Закончи вопросом для продолжения диалога

Пример хорошего ответа: "Если ребёнок не хочет делать уроки, попробуйте превратить это в игру. Например, 'Кто быстрее решит 5 примеров?' 🏆 Это мотивирует! Какой предмет даётся сложнее всего?"

Избегай длинных теоретических объяснений!"""
        }

    def set_mode(self, mode: str):
        if mode in self.system_prompts:
            self.mode = mode

    def set_topic(self, topic: str):
        self.topic = topic

    async def get_response(self, user_message: str) -> str:
        system_prompt = self.system_prompts[self.mode] + "\n\nСЕЙЧАС ОТВЕЧАЙ: " + user_message

        messages = [
            SystemMessage(content=system_prompt)
        ]

        try:
            chat_response = await self.client.chat.complete_async(
                model=self.model,
                messages=messages,
                max_tokens=400,
                temperature=0.8,
                top_p=0.9
            )

            if chat_response.choices and len(chat_response.choices) > 0:
                response_text = chat_response.choices[0].message.content
                return self._ensure_brevity(response_text)
            else:
                return self._get_short_fallback()

        except Exception as e:
            logger.error(f"Ошибка при запросе к нейронке: {e}")
            return self._get_short_fallback()

    def _ensure_brevity(self, text: str) -> str:

        if len(text) > 1200:
            sentences = text.split('. ')
            result = []
            char_count = 0

            for sentence in sentences:
                if char_count + len(sentence) < 1000:
                    result.append(sentence)
                    char_count += len(sentence)
                else:
                    break

            text = '. '.join(result) + '.'

        if self.mode == "child":
            prefixes = ["🧒 ", "👦 ", "👧 ", "🌟 ", "🎨 ", "📚 "]
            import random
            return random.choice(prefixes) + text
        elif self.mode == "parent":
            return "👨‍👩‍👧 " + text
        else:
            return "🤖 " + text

    def _get_short_fallback(self) -> str:
        fallback_responses = {
            "child": [
                "Привет! О чём хочешь поговорить? 😊",
                "Расскажи, как прошёл твой день! 🌟",
                "Давай поиграем в вопросы? Задавай! 🎲"
            ],
            "parent": [
                "Чем могу помочь? Спрашивайте! 👨‍👩‍👧",
                "Как дела у вашего первоклассника? 📚",
                "Есть вопросы по воспитанию? Готов помочь! 💡"
            ],
        }

        import random
        response = random.choice(fallback_responses.get(self.mode, ["Привет! 😊"]))

        if self.mode == "child":
            return "🧒 " + response
        elif self.mode == "parent":
            return "👨‍👩‍👧 " + response
        return response
    

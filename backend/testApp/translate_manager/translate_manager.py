from ollama import AsyncClient

from typing import Optional, List, Dict
import json
from datetime import datetime

class TranslatorManager:
    def __init__(self, model: str = "deepseek-coder:6.7b-instruct-q4_K_M"):
        self.model = model
        self.client = AsyncClient()
        # self._check_model()
    
    # def _check_model(self):
    #     try:
    #         models = ollama.list()
    #         available_models = [m['name'] for m in models.get('models', [])]
            
    #         if self.model not in available_models:
    #             print(f"Модель {self.model} не найдена. Пытаюсь загрузить...")
    #             ollama.pull(self.model)
    #             print("Модель успешно загружена!")
    #     except Exception as e:
    #         print(f"Ошибка: {e}")
    #         print("Убедитесь, что Ollama запущен (ollama serve)")
    
    async def translate(self, text: str) -> str:
        prompt = f"""
    Я читаю документацию,но она на английском,Переведи следующий текст пожалуйста  на РУССКИЙ ЯЗЫК:
    "{text}"

    Верни ТОЛЬКО перевод без кавычек, без дополнительного текста.
    Пример ответа: "Привет мой друг"
    """     
        try:
            response = await self.client.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.5}  
            )
            
            translated = response['message']['content'].strip()
            
            translated = self._clean_translation(translated)
            
            return translated
            
        except Exception as e:
            print(f"Translation error: {e}")
            return f"Ошибка перевода: {str(e)}"

    def _clean_translation(self, text: str) -> str:
        text = text.replace('\\', '')
        
        text = text.strip('"\'')
        
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        elif text.startswith("'") and text.endswith("'"):
            text = text[1:-1]
        
        text = text.strip()
        
        return text

    async def context_answer(self, messages: List[dict], current_user_id: int) -> str:
        """
        Генерирует ответ на НЕПРОЧИТАННЫЕ сообщения от другого пользователя
        """
        if not messages:
            return "Нет непрочитанных сообщений для ответа"
        
        unread_from_others = []
        for msg in messages:
            if msg['sender_id'] != current_user_id:
                unread_from_others.append(msg)
        
        print(f"DEBUG: Все сообщения: {len(messages)}")
        print(f"DEBUG: Непрочитанные от других: {len(unread_from_others)}")
        
        if not unread_from_others:
            return "Нет новых сообщений от собеседника"
        
        recent_unread = unread_from_others[-3:] if len(unread_from_others) > 3 else unread_from_others
        
        system_prompt = """Ты — участник диалога в мессенджере. Твоя задача — дать естественный ответ на сообщения собеседника.

Правила ответа:
1. Отвечай ТОЛЬКО на полученные сообщения, не добавляй новые темы
2. Используй только русский язык, говори как носитель
3. Будь кратким — 1-3 предложения достаточно
4. Пиши сплошным текстом без смайликов, эмодзи и пунктов списка
5. Учитывай контекст всех полученных сообщений
6. Сохраняй естественный, разговорный стиль
7.Можешь выдумывать ответы например любимый цвет синий т.д.

Примеры хороших ответов:
- "Привет! У меня всё хорошо, спасибо. А у тебя как дела?"
- "Синий. А тебе какой нравится?"
- "Да, уже посмотрел. Очень понравился, рекомендую!"

Примеры плохих ответов:
- "Отвечаю на ваше сообщение: я чувствую себя хорошо."
- "1) Привет 2) У меня хорошо 3) А у вас?"
- "😊 Привет! Как дела? 😊"

Теперь я отправлю тебе сообщения собеседника. Ответь на них естественно и кратко."""

        
        conversation_lines = [msg['message'] for msg in recent_unread]
        conversation_text = "\n".join(conversation_lines)
        
        try:
            response = await self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": conversation_text}
                ],
                options={"temperature": 0.7, "max_tokens": 150}
            )
            
            result = response['message']['content'].strip()
            cleaned_response = self.clean_llm_response(result)
            return cleaned_response
            
        except Exception as e:
            print(f"Error in get_context_answer: {e}")
            return f"Не удалось сгенерировать ответ"
        
    def clean_llm_response(self, text: str) -> str:
    
        if not text:
            return ""
        
        text = text.strip('"\'«»“”')
        
        text = ' '.join(text.splitlines())
        
        text = ' '.join(text.split())
        
        formal_prefixes = [
            "Отвечаю на ваше сообщение:",
            "В ответ на ваше сообщение:",
            "Мой ответ:",
            "Я бы ответил:",
            "Ответ:",
            "Отвечаю:"
        ]
        
        for prefix in formal_prefixes:
            if text.startswith(prefix):
                text = text[len(prefix):].strip()
        
        text = text.strip('"\'«»')
        
        return text
# c = [{"message": "Привет,Даник!", "date": datetime.now()},
#      {"message": "Я тут вчера выиграл волейбольный матч в школе,круто,да?", "date": datetime.now()},
#      {"message": "А еще у меня есть классная идея на выходные,не хочешь вместе в кино сходить?", "date": datetime.now()},
#      ]


# a = TranslatorManager()
# b =  a.context_answer(c)    
# print(b)
# import asyncio

# from groq import AsyncGroq


# async def main():
#     client = AsyncGroq()

#     chat_completion = await client.chat.completions.create(
#         #
#         # Required parameters
#         #
#         messages=[
#             # Set an optional system message. This sets the behavior of the
#             # assistant and can be used to provide specific instructions for
#             # how it should behave throughout the conversation.
#             {
#                 "role": "system",
#                 "content": "You are a helpful assistant."
#             },
#             # Set a user message for the assistant to respond to.
#             {
#                 "role": "user",
#                 "content": "Translate it to russian language: Bet! I'm down for whatever. Lmk the deets",
#             }
#         ],

#         # The language model which will generate the completion.
#         model="llama-3.3-70b-versatile",

#         #
#         # Optional parameters
#         #

#         # Controls randomness: lowering results in less random completions.
#         # As the temperature approaches zero, the model will become
#         # deterministic and repetitive.
#         temperature=0.5,

#         # The maximum number of tokens to generate. Requests can use up to
#         # 2048 tokens shared between prompt and completion.
#         max_completion_tokens=1024,

#         # Controls diversity via nucleus sampling: 0.5 means half of all
#         # likelihood-weighted options are considered.
#         top_p=1,

#         # A stop sequence is a predefined or user-specified text string that
#         # signals an AI to stop generating content, ensuring its responses
#         # remain focused and concise. Examples include punctuation marks and
#         # markers like "[end]".
#         stop=None,

#         # If set, partial message deltas will be sent.
#         stream=False,
#     )

#     # Print the completion returned by the LLM.
#     print(chat_completion.choices[0].message.content)

# asyncio.run(main())
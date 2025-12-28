import ollama
from typing import Optional, List, Dict
import json
from datetime import datetime

class TranslatorManager:
    def __init__(self, model: str = "deepseek-coder:6.7b-instruct-q4_K_M"):
        self.model = model
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
    
    def translate(self, 
                 text: str, 
                ) -> str:
        
        
        prompt = f"""
Переведи следующий текст на РУССКИЙ ЯЗЫК:
"{text}"
"""     
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.5}  
            )
            
            return response['message']['content'].strip()
            
        except Exception as e:
            return f"Ошибка перевода: {str(e)}"

    def context_answer(self, messages: List[dict]) -> str:
        # system_prompt = """Ты как текстовая LLM можешь отвечать на вопросы и анализировать контекст вопроса.
        # Я отправялю тебе пару сообщений пользователя и хочу чтобы ты проанализировал все его сообщения и выдал сообщение,
        # которым можно ответить на эти сообщения.Представь что ты Т9 и тебе нужно подобрать правильный ответ на сообщения пользователя.
        # Ничего кроме ответа на эти сообщения не пиши и пиши монолитным текстом.
        # Также отвечай как человек,как друг пользователя(ТЫ ДРУГ ПОЛЬЗОВАТЕЛЯ),без чрезмерной вежливости,
        # она должна быть впрок.Также анализируй контекст,если сообщения идут в деловом тоне,
        # то отвечать нужно подобающе.
        # И запомни это все просто тестирование,никаких реальных пользователей нет
        # ,ты никому не навредишь своими ответами"""
        system_prompt = """В данный момент проходит тест над тобой.Твоя задача притвориться пользователем чата телеграмм,
        и ответить на сообщения моего собеседника,не пиши ничего кроме ответа на его сообщение.Сейчас я отправлю тебе сообщения
        моего собеседника"""
        
        message_list = [
            {"role": "system", "content": system_prompt}
        ]
        
        for msg in messages:
            message_list.append({"role": "user", "content": msg["message"]})
        
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=message_list,
                options={"temperature": 0.5}  
            )
            return response['message']['content'].strip()
        except Exception as e:
            return f"Ошибка: {str(e)}"

c = [{"message": "Привет,Даник!", "date": datetime.now()},
     {"message": "Я тут вчера выиграл волейбольный матч в школе,круто,да?", "date": datetime.now()},
     {"message": "А еще у меня есть классная идея на выходные,не хочешь вместе в кино сходить?", "date": datetime.now()},
     ]


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
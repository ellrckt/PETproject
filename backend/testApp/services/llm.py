# services/llm_service.py
import logging
import json
from typing import List, Dict, Optional
from datetime import datetime
import openai

logger = logging.getLogger(__name__)

class AISearchFilterService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(
            api_key="io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6IjRlMmJmNTYzLTY4ZGYtNDE0ZS04NTllLThlNjQ5YmJjYTAzOCIsImV4cCI6NDkzMjkzNTQxNX0.PHAzKbwISDV9BMK1G2dJpUNIlq4ZEiIBitkivMWDsJSbE0Z4SbsNehU2IGGPIKEQuFYFLOq4Ou2xDsqbUE5T3w",
            base_url="https://api.intelligence.io.solutions/api/v1/",
        )
        self.model = "meta-llama/Llama-3.3-70B-Instruct"

    async def select_relevant_messages(
        self, 
        user_query: str, 
        chat_messages: List[Dict],
        author_id: Optional[int] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        limit: int = 20
    ) -> Dict:
        """
        Отправляет сообщения и все метапараметры поиска в Llama.
        ИИ выбирает 3 наиболее релевантных сообщения и возвращает JSON.
        """
        if not chat_messages:
            return {"selected_messages": [], "reason": "Нет сообщений для фильтрации."}

        # Форматируем входные данные сообщений чата
        input_context = []
        for msg in chat_messages:
            input_context.append({
                "id": msg.get("id"),
                "message": msg.get("message"),
                "sender_id": msg.get("sender_id"),
                "created_at": str(msg.get("created_at"))
            })

        system_prompt = (
            "Ты — интеллектуальный ассистент-фильтр сообщений в чате.\n"
            "Твоя задача — проанализировать список сообщений, полученных из базы данных, "
            "и выбрать из них максимум 3 сообщения, которые НАИБОЛЕЕ ТОЧНО отвечают на запрос пользователя "
            "с учетом заданных критериев фильтрации.\n\n"
            "ПРАВИЛА:\n"
            "1. Выбирай сообщения, которые релевантны тексту запроса и соответствуют метаданным (автор, временной диапазон).\n"
            "2. Ответ ДОЛЖЕН быть строго в формате JSON без какого-либо постороннего текста.\n"
            "3. Структура ответа:\n"
            "{\n"
            '  "data": [\n'
            '    {"id": 1, "message": "текст", "sender_id": 2, "created_at": "время"}\n'
            '  ],\n'
            '  "reason": "Обоснование выбора с упоминанием соответствия критериям (запросу, автору, датам)"\n'
            "}"
        )

        # Собираем метаданные поиска для ИИ, чтобы он понимал контекст ограничений
        search_metadata = {
            "user_query": user_query,
            "filter_by_author_id": author_id if author_id is not None else "Все авторы",
            "filter_date_from": str(date_from) if date_from else "Не указано",
            "filter_date_to": str(date_to) if date_to else "Не указано",
            "max_db_records_analyzed": limit
        }

        user_content = (
            f"--- ПАРАМЕТРЫ ПОИСКА И ФИЛЬТРЫ ---\n"
            f"{json.dumps(search_metadata, ensure_ascii=False, indent=2)}\n\n"
            f"--- СПИСОК СООБЩЕНИЙ ИЗ БД ДЛЯ АНАЛИЗА ---\n"
            f"{json.dumps(input_context, ensure_ascii=False, indent=2)}"
        )

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                temperature=0.3,
                max_completion_tokens=1000,
                response_format={"type": "json_object"} 
            )
            
            raw_ai_response = response.choices[0].message.content
            return json.loads(raw_ai_response)

        except Exception as e:
            logger.error(f"❌ Llama RAG filtering failed: {e}", exc_info=True)
            return {
                "selected_messages": chat_messages[:3], 
                "reason": f"Ошибка вызова ИИ-фильтра: {str(e)}. Возвращены первые результаты."
            }

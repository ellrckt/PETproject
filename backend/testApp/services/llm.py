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
            api_key="io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6ImVlMWIzMmEwLTQwZjEtNDIzYy05OWExLTM0ODE0NzkyZjQ4NiIsImV4cCI6NDkzMzQ4OTMxOH0.i9wfuwl2252SDvhJowNbLqoXv1K7VK_ZfZGydBG6TAPyThCTuyOzF7KLotDm8Hy7PfPGz_o3Yt2MAgIml288_w",
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
        print("User content", user_content)
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
    
    async def select_for_summ(
        self, 
        user_query: Optional[str], 
        sumMode: str,
        chat_messages: List[Dict],
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> Dict:

        if not chat_messages:
            return {"summary": "• В данном контексте сообщений не найдено.", "reason": "Пустой чат"}

        input_context = []
        for msg in chat_messages:
            input_context.append({
                "id": msg.get("id"),
                "message": msg.get("message"),
                "sender_id": msg.get("sender_id"),
                "created_at": str(msg.get("created_at"))
            })
            
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 1. ИСПРАВЛЕНА ЦЕПОЧКА УСЛОВИЙ (if / elif / else)
        if sumMode == 'tasks':
            system_prompt = (
                f"Ты — интеллектуальный ассистент-координатор в мессенджере. Твоя задача — проанализировать предоставленную историю сообщений и извлечь из неё только конкретные задачи, поручения, обязательства и договоренности, которые участники чата взяли на себя или поручили другим.\n"
                f"Текущая дата и время на момент обработки запроса: {current_time_str}.\n\n"
                f"Критерии фильтрации:\n"
                f"- Игнорируй флуд, обсуждения, приветствия и личные мнения.\n"
                f"- Фиксируй только то, что ДОЛЖНО быть сделано.\n"
                f"- Если у задачи есть дедлайн или ответственный, обязательно укажи их.\n\n"
                f"КРИТИЧЕСКИ ВАЖНОЕ ТРЕБОВАНИЕ К ФОРМАТУ (ОТВЕЧАЙ СТРОГО ПО ПРИМЕРУ):\n"
                f"Ты должен вернуть СТРОГО JSON-объект с ключом \"summary\".\n"
                f"Значением этого ключа должна быть единая строка, содержащая лаконичный маркированный список на русском языке, где каждый пункт начинается с символа \"• \", а разделение строк идет через символ переноса строки \\n.\n"
                f"Если задач не обнаружено, значением ключа должна быть строка: \"• В данном контексте активных задач не найдено.\"\n\n"
                f"Пример структуры ответа:\n"
                f"{{\n"
                f"  \"summary\": \"• Исправить баг с типами в файле auth/utils.py (Ответственный: @username)\\n• Реализовать POST-эндпоинт для суммаризации до пятницы\"\n"
                f"}}"
            )
            
        elif sumMode == 'plans': # <-- ДОБАВЛЕН ELIF И ИСПРАВЛЕНО НА ВСТРЕЧИ
            system_prompt = (
                f"Ты — системный секретарь-планировщик. Твоя задача — внимательно изучить историю переписки и найти любые упоминания БУДУЩИХ совместных мероприятий, встреч, созвонов, дедлайнов проектов или запланированных событий, актуальных относительно текущего времени.\n\n"
                f"Входные данные:\n"
                f"1. К каждому сообщению прикреплена дата и время его отправки в поле created_at.\n"
                f"2. Текущая дата и время на момент обработки запроса: {current_time_str}.\n\n"
                f"Инструкции по анализу времени (Критически важно):\n"
                f"- Используй дату отправки конкретного сообщения и текущее время, чтобы вычислить реальную календарную дату запланированного события.\n"
                f"- Пересчитывай относительные указания времени (\"завтра\", \"в среду\", \"через 2 дня\") на основе даты отправки того сообщения, где они прозвучали.\n"
                f"- Игнорируй события, которые уже остались в прошлом относительно Текущего времени (даже если на момент отправки сообщения они были в будущем).\n"
                f"- Игнорируй гипотетические обсуждения и прошедшие события.\n\n"
                f"КРИТИЧЕСКИ ВАЖНОЕ ТРЕБОВАНИЕ К ФОРМАТУ (ОТВЕЧАЙ СТРОГО ПО ПРИМЕРУ):\n"
                f"Ты должен вернуть СТРОГО JSON-объект с ключом \"summary\".\n"
                f"Значением этого ключа должна быть единая строка, содержащая лаконичный маркированный список на русском языке, где каждый пункт начинается с символа \"• \", а разделение строк идет через символ переноса строки \\n.\n"
                f"Для каждого события укажи вычисленную реальную дату или день недели.\n"
                f"Если собеседники обсуждают одно и то же событие разными словами, ОБЪЕДИНЯЙ их в один пункт списка, не дублируй!\n"
                f"Если актуальных встреч или планов не найдено, значением ключа должна быть строка: \"• На ближайшее время встреч и планов не запланировано.\"\n\n"
                f"Пример структуры ответа:\n"
                f"{{\n"
                f"  \"summary\": \"• Созвон команды для тестирования фильтрации сообщений — Четверг (28 мая) в 11:00\\n• Дедлайн по деплою проекта — В эту пятницу (29 мая), до конца дня\"\n"
                f"}}"
            )
            
        elif sumMode == 'custom': # <-- ИСПРАВЛЕНО НА ELIF
            system_prompt = (
                f"Ты — экспертная QA-система (Retrieval-Augmented Generation), которая отвечает на вопросы пользователя, используя строго предоставленный контекст сообщений из чата.\n\n"
                f"Инструкции по обработке:\n"
                f"1. Внимательно прочитай историю сообщений, переданную пользователем.\n"
                f"2. Найди информацию, которая напрямую отвечает на заданный вопрос: \"{user_query}\".\n"
                f"3. Твой ответ должен базироваться ТОЛЬКО на фактах из переписки. Запрещено выдумывать или предполагать информацию, которой нет в тексте (отсутствие галлюцинаций — критически важно).\n"
                f"4. Если в истории чата нет ответа на этот вопрос, значением ключа должна быть строго фраза: \"• В предоставленном контексте сообщений нет информации по вашему запросу.\"\n\n"
                f"КРИТИЧЕСКИ ВАЖНОЕ ТРЕБОВАНИЕ К ФОРМАТУ (ОТВЕЧАЙ СТРОГО ПО ПРИМЕРУ):\n"
                f"Ты должен вернуть СТРОГО JSON-объект с ключом \"summary\".\n"
                f"Значением этого ключа должна быть единая строка, содержащая лаконичный ответ на русском языке в виде маркированного списка, где каждый пункт начинается с символа \"• \", а разделение строк идет через символ переноса строки \\n.\n\n"
                f"Пример структуры ответа:\n"
                f"{{\n"
                f"  \"summary\": \"• Для маски телефона Максим посоветовал использовать библиотеку react-input-mask.\\n• Данное решение подходит для номеров РБ и РФ.\"\n"
                f"}}"
            )
        else:
            system_prompt = "Ты — ассистент. Ответь в JSON формате: {\"summary\": \"• Ошибка: неизвестный режим.\"}"

        # 2. ВОЗВРАЩЕНА ПРОПУЩЕННАЯ ПЕРЕМЕННАЯ МЕТАДАННЫХ
        search_metadata = {
            "user_query": user_query or "Автоматическое резюмирование",
            "filter_date_from": str(date_from) if date_from else "Не указано",
            "filter_date_to": str(date_to) if date_to else "Не указано",
        }

        user_content = (
            f"--- ПАРАМЕТРЫ ПОИСКА И ФИЛЬТРЫ ---\n"
            f"{json.dumps(search_metadata, ensure_ascii=False, indent=2)}\n\n"
            f"--- СПИСОК СООБЩЕНИЙ ИЗ БД ДЛЯ АНАЛИЗА ---\n"
            f"{json.dumps(input_context, ensure_ascii=False, indent=2)}"
        )

        try:
            print("Messages ", input_context)
            
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
            if not raw_ai_response:
                return {"summary": "• Модель вернула пустой ответ.", "reason": "Empty AI response"}

            cleaned_response = raw_ai_response.strip()
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.replace("```json", "").replace("```", "").strip()
            
            parsed_json = json.loads(cleaned_response)
            return {"summary": parsed_json.get("summary", cleaned_response)}

        except Exception as e:
            logger.error(f"Llama RAG filtering failed: {e}", exc_info=True)
            return {
                "summary": "• Произошла ошибка при генерации отчета нейросетью.",
                "reason": f"Ошибка исполнения: {str(e)}"
            }
        
# query: "",
#       timeMode: "unread",
#       date_from: null,
#       date_to: null,
#       sumMode: "tasks",


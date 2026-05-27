from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import db_helper
from services.embedding import ChatEmbeddingService
from utils.search_repository import hybrid_search_messages, hybrid_sum_search_messages
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


from services.llm import AISearchFilterService 
router = APIRouter(prefix="/search", tags=["search"])


embedding_svc = ChatEmbeddingService()
ai_filter_svc = AISearchFilterService()

class MessageResponse(BaseModel):
    id: int
    message: str
    sender_id: int
    receiver_id: int
    created_at: datetime
    semantic_score: float = 0.0
    keyword_score: float = 0.0

class SearchResponse(BaseModel):
    results: List[MessageResponse]

class SelectedMessageSchema(BaseModel):
    id: int
    message: str
    sender_id: int
    created_at: datetime

class AISmartSearchResponse(BaseModel):
    data: List[SelectedMessageSchema]
    reason: str

class AISmartSearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    author_id: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    limit: Optional[int] = Field(20, le=50)
    

@router.post("/{room_id}/search", response_model=SearchResponse)
async def search_messages(
    room_id: str,
    query: str = Body(min_length=1),
    author_id: Optional[int] = Body(None, alias="author_id"), # Синхронизировано со Swagger
    date_from: Optional[datetime] = Body(None),
    date_to: Optional[datetime] = Body(None),
    limit: int = Body(20, le=50),
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Умный поиск по чату.
    Пример: query="история про животных", author_id=2, limit=2
    """
    # 1. Векторизуем запрос пользователя
    query_vector = embedding_svc.embed_text(query)
    
    # 2. Ищем (Гибрид: Смысл + Ключевые слова + Фильтры)
    # Передаем author_id в параметр sender_id репозитория
    results = await hybrid_search_messages(
        session=session,
        room_id=room_id,
        query_vector=query_vector,
        query_text=query,
        sender_id=author_id,  
        date_from=date_from,
        date_to=date_to,
        limit=limit
    )
    
    return SearchResponse(results=results or [])


class SearchRequestSchema(BaseModel):
    query: str = Field(..., min_length=1, description="Текст поискового запроса")
    author_id: Optional[int] = Field(None, description="Фильтр по ID автора сообщений")
    date_from: Optional[datetime] = Field(None, description="Начало периода поиска (ISO 8601)")
    date_to: Optional[datetime] = Field(None, description="Конец периода поиска (ISO 8601)")
    limit: int = Field(20, le=50, description="Максимальное количество результатов")

@router.post("/{room_id}/smart-filter", response_model=AISmartSearchResponse)
async def smart_search_with_ai_filter(
    room_id: str,
    request_data: AISmartSearchRequest, # <- Теперь данные считываются из JSON Body
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Гибридный поиск по базе данных (извлекает топ-5/топ-10), 
    а затем Llama фильтрует их до 3-х самых релевантных.
    """
    query_vector = embedding_svc.embed_text(request_data.query)
    
    raw_db_results = await hybrid_search_messages(
        session=session,
        room_id=room_id,
        query_vector=query_vector,
        query_text=request_data.query,
        sender_id=request_data.author_id,  
        date_from=request_data.date_from,
        date_to=request_data.date_to,
        limit=request_data.limit
    )
    
    ai_filtered_json = await ai_filter_svc.select_relevant_messages(
        user_query=request_data.query,
        chat_messages=raw_db_results or []
    )
    
    return ai_filtered_json

@router.post("/{room_id}/smart-sum", response_model=AISmartSearchResponse)
async def smart_sum_with_ai(
    room_id: str,
    timeMode: Optional[str] = Body(None),
    sumMode : Optional[str] = Body(None),
    query: Optional[str] = Body(..., min_length=1),
    date_from: Optional[datetime] = Body(None),
    date_to: Optional[datetime] = Body(None),
    limit: Optional[int] = Body(20, le=50),
    session: AsyncSession = Depends(db_helper.get_session),
):

    if query:
        query_vector = embedding_svc.embed_text(query)

        raw_db_results = await hybrid_sum_search_messages(
            session=session,
            room_id=room_id,
            query_vector=query_vector,
            query_text=query,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            timeMode=timeMode
        )
    else:
        raw_db_results = await hybrid_sum_search_messages(
            session=session,
            room_id=room_id,
            query_vector=None,
            query_text=None,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            timeMode=timeMode

        )

    ai_filtered_json = await ai_filter_svc.select_for_summ(
        user_query=query,
        chat_messages=raw_db_results or [],
        sumMode=sumMode
    )

    return ai_filtered_json
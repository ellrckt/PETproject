# repository/chat_search_repository.py
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
TEXT_SEARCH_CONFIG = 'simple'  # Убедитесь в правильности регистра переменной

def _vector_to_literal(vec: List[float]) -> str:
    """Конвертирует список float в строку-литерал для PostgreSQL vector."""
    return '[' + ','.join(f'{x:.6f}' for x in vec) + ']'

async def hybrid_search_messages(
    session: AsyncSession,
    room_id: str,
    query_vector: List[float],
    query_text: str,
    sender_id: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    limit: int = 20,
    semantic_weight: float = 0.7
) -> List[Dict]:
    """Гибридный поиск по сообщениям с фолбэком на ILIKE поиск при ошибках"""
    
    vec_literal = _vector_to_literal(query_vector)
    keyword_weight = 1.0 - semantic_weight
    
    filters = ["room_id = :room_id"]
    params = {
        "room_id": room_id,
        "q_text": query_text,
        "limit": limit
    }
    
    if sender_id is not None:
        filters.append("sender_id = :sender_id")
        params["sender_id"] = sender_id
    if date_from:
        filters.append("created_at >= :date_from")
        params["date_from"] = date_from
    if date_to:
        filters.append("created_at <= :date_to")
        params["date_to"] = date_to
        
    where_clause = " AND ".join(filters)

    # Оптимизированный SQL: считаем скоры один раз в подзапросе
    query = text(f"""
        SELECT id, message, sender_id, receiver_id, created_at, semantic_score, keyword_score
        FROM (
            SELECT 
                id, message, sender_id, receiver_id, created_at,
                (1 - (embedding <=> '{vec_literal}'::vector)) AS semantic_score,
                ts_rank(to_tsvector('{TEXT_SEARCH_CONFIG}', message), plainto_tsquery('{TEXT_SEARCH_CONFIG}', :q_text)) AS keyword_score
            FROM messages
            WHERE {where_clause} 
              AND embedding IS NOT NULL
        ) sub
        ORDER BY ({semantic_weight} * semantic_score + {keyword_weight} * keyword_score) DESC
        LIMIT :limit
    """)
    
    # Используем точку сохранения (begin_nested), чтобы защитить внешнюю транзакцию от падения
    nested_tx = await session.begin_nested()
    try:
        result = await session.execute(query, params)
        rows = result.all()
        if rows:
            return [dict(row._mapping) for row in rows]
            
    except Exception as e:
        logger.warning(f"⚠️ Hybrid search failed, falling back to simple search: {e}")
        await nested_tx.rollback()  # Откатываем только этот блок, сессия остается "живой"
        return await _simple_search(session, room_id, query_text, sender_id, date_from, date_to, limit)
    
    # Если поиск прошел без ошибок, но ничего не нашел — возвращаем пустой список
    return []


async def _simple_search(
    session: AsyncSession,
    room_id: str,
    query_text: str,
    sender_id: Optional[int],
    date_from: Optional[datetime],
    date_to: Optional[datetime],
    limit: int
) -> List[Dict]:
    """Простой поиск через ILIKE"""
    
    filters = ["room_id = :room_id", "message ILIKE :like_text"]
    params = {
        "room_id": room_id, 
        "like_text": f"%{query_text}%", 
        "limit": limit
    }
    
    if sender_id:
        filters.append("sender_id = :sender_id")
        params["sender_id"] = sender_id
    if date_from:
        filters.append("created_at >= :date_from")
        params["date_from"] = date_from
    if date_to:
        filters.append("created_at <= :date_to")
        params["date_to"] = date_to
        
    where = " AND ".join(filters)
    
    query = text(f"""
        SELECT id, message, sender_id, receiver_id, created_at, 0.0 AS score
        FROM messages
        WHERE {where}
        ORDER BY created_at DESC
        LIMIT :limit
    """)
    
    try:
        result = await session.execute(query, params)
        return [dict(row._mapping) for row in result.all()]
    except Exception as e:
        logger.error(f"❌ Simple search failed: {e}")
        # Здесь мы не делаем rollback, делегируя его вызывающему коду (сервису/эндпоинту)
        raise

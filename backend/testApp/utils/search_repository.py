# repository/chat_search_repository.py
from fastapi import Body

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
        logger.error(f"Simple search failed: {e}")
        # Здесь мы не делаем rollback, делегируя его вызывающему коду (сервису/эндпоинту)
        raise

from fastapi import Body
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def hybrid_sum_search_messages(
    session: AsyncSession,
    room_id: str,
    query_vector: Optional[List[float]],
    query_text: Optional[str],
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    limit: Optional[int] = None,
    semantic_weight: float = 0.7,
    timeMode: Optional[str] = Body(None),
) -> List[Dict]:
    
    keyword_weight = 1.0 - semantic_weight
    
    params = {"room_id": room_id}
    filters = ["room_id = :room_id"]
    

    if date_from:
        filters.append("created_at >= :date_from")
        params["date_from"] = date_from
    if date_to:
        filters.append("created_at <= :date_to")
        params["date_to"] = date_to

    has_text = query_text and query_text.strip()
    has_vector = query_vector is not None and len(query_vector) > 0
    is_hybrid = has_text and has_vector

    inner_limit_clause = ""
    outer_limit_clause = ""
    
    if timeMode:
        if limit:
            inner_limit_clause = "ORDER BY created_at DESC LIMIT :limit"
            params["limit"] = limit
    else:
        if limit:
            outer_limit_clause = "LIMIT :limit"
            params["limit"] = limit

    if is_hybrid:
        vec_literal = _vector_to_literal(query_vector)
        filters.append("embedding IS NOT NULL")
        filters.append("message ILIKE :like_text")
        
        params["like_text"] = f"%{query_text}%"
        params["q_text"] = query_text
        
        semantic_score_sql = f"(1 - (embedding <=> '{vec_literal}'::vector))"
        keyword_score_sql = f"ts_rank(to_tsvector('{TEXT_SEARCH_CONFIG}', message), plainto_tsquery('{TEXT_SEARCH_CONFIG}', :q_text))"
        order_by_sql = f"({semantic_weight} * semantic_score + {keyword_weight} * keyword_score) DESC"
    else:
        semantic_score_sql = "0.0"
        keyword_score_sql = "0.0"
        order_by_sql = "created_at DESC"

    where_clause = " AND ".join(filters)

    query = text(f"""
        SELECT id, message, sender_id, receiver_id, created_at, semantic_score, keyword_score
        FROM (
            SELECT 
                id, message, sender_id, receiver_id, created_at,
                {semantic_score_sql} AS semantic_score,
                {keyword_score_sql} AS keyword_score
            FROM messages
            WHERE {where_clause}
            {inner_limit_clause}
        ) sub
        ORDER BY {order_by_sql}
        {outer_limit_clause}
    """)
    
    nested_tx = await session.begin_nested()
    try:
        result = await session.execute(query, params)
        rows = result.all()
        if rows:
            return [dict(row._mapping) for row in rows]
            
    except Exception as e:
        logger.warning(f"Hybrid search failed, falling back to simple search: {e}")
        await nested_tx.rollback()
        return await _simple_sum(session, room_id, query_text, date_from, date_to, limit, timeMode)
    
    return []


async def _simple_sum(
    session: AsyncSession,
    room_id: str,
    query_text: Optional[str],
    date_from: Optional[datetime],
    date_to: Optional[datetime],
    limit: Optional[int],
    timeMode: Optional[str] = Body(None),
) -> List[Dict]:
    filters = ["room_id = :room_id"]
    params = {"room_id": room_id}

    if query_text and query_text.strip():
        filters.append("message ILIKE :like_text")
        params["like_text"] = f"%{query_text}%"

    if date_from:
        filters.append("created_at >= :date_from")
        params["date_from"] = date_from
    if date_to:
        filters.append("created_at <= :date_to")
        params["date_to"] = date_to
        
    where = " AND ".join(filters)
    
    inner_limit = ""
    outer_limit = ""
    
    if timeMode and limit:
        inner_limit = "ORDER BY created_at DESC LIMIT :limit"
        params["limit"] = limit
    elif limit:
        outer_limit = "LIMIT :limit"
        params["limit"] = limit
    
    query = text(f"""
        SELECT id, message, sender_id, receiver_id, created_at, 0.0 AS score
        FROM (
            SELECT id, message, sender_id, receiver_id, created_at
            FROM messages
            WHERE {where}
            {inner_limit}
        ) sub
        ORDER BY created_at DESC
        {outer_limit}
    """)
    
    try:
        result = await session.execute(query, params)
        return [dict(row._mapping) for row in result.all()]
    except Exception as e:
        logger.error(f"Simple search failed: {e}")
        raise

import logging
from sqlalchemy import text
from db.db import db_helper 
from services.embedding import ChatEmbeddingService

logger = logging.getLogger(__name__)
embedding_svc = ChatEmbeddingService()

async def generate_embedding_for_message(message_id: str, message: str):
    """Фоновая генерация эмбеддингов с безопасным приведением типов"""
    try:
        # 1. Получаем список float из модели
        vector = embedding_svc.embed_text(message)
        
        # 2. Обновляем запись, используя явный CAST вместо конструкции '::'
        async with db_helper.session_factory() as session:
            await session.execute(
                text("UPDATE messages SET embedding = cast(:vec as vector) WHERE message_id = :id"),
                {"vec": str(vector), "id": message_id}
            )
            await session.commit()
            
        logger.info(f" Successfully embedded message {message_id}")
        
    except Exception as e:
        logger.error(f"❌ Failed to embed message {message_id}: {e}", exc_info=True)

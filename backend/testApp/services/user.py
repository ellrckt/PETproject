from utils.user_repository import AbstractUserCRUDRepository,AbstractUserRepository
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user.user import UserRegistration, UserLogin, UserUpdate,UserEmailConffirmation
from auth.utils import decode_jwt
from simplegmail import Gmail
import random
import string
class UserCRUDService:

    def __init__(self, user_repo: AbstractUserCRUDRepository):
        self.user_repo = user_repo()

    async def add_one(self, user_schema: User, session: AsyncSession):
        user_dict = user_schema.model_dump()
        user_id = await self.user_repo.add_one(user_dict, session)
        return user_id

    async def get_all(self, session: AsyncSession):

        result = await self.user_repo.get_all(session)
        return result

    async def delete(self, user_id: int, session: AsyncSession):

        result = await self.user_repo.delete(user_id, session)
        return result

    async def update(self, schema: UserUpdate, session: AsyncSession, payload: dict):

        user_dict = schema.model_dump()
        result = await self.user_repo.update(user_dict, session, payload)
        return result





class UserService:

    def __init__(self, user_repo: AbstractUserRepository):
        self.user_repo = user_repo()

    async def register_user(self, schema: UserRegistration, session: AsyncSession):
        user_data = schema.model_dump()
        result = await self.user_repo.register_user(user_data, session)
        return result
    
    async def create_user_session(self,user: User, refresh_token: str, session: AsyncSession):
        payload = decode_jwt(refresh_token)
        result = await self.user_repo.create_user_session(user,payload,session)
        return result
    
    async def get_tokens_with_google(self, email: str,session: AsyncSession):

        result = await self.user_repo.get_tokens_with_google(email, session)
        return result

    async def login_user(self, schema: UserLogin, session: AsyncSession):
        user_data = schema.model_dump()
        result = await self.user_repo.login_user(user_data, session)
        return result

    async def refresh_token(
        self, session: AsyncSession, refresh_token: str
    ):
        result = await self.user_repo.refresh_token(session, refresh_token)
        return result

    async def get_user_location(self,schema: dict, session: AsyncSession):
        location = schema.model_dump()
        result = await self.user_repo.get_user_location(location: dict, session: AsyncSession)
        return result




















    # async def confirm_email(
    #     self,
    #     session: AsyncSession,
    #     schema: UserEmailConffirmation,
    #     payload: dict
        
    # ):  
    #     code_data = schema.model_dump()
    #     result = await self.user_repo.confirm_email(session,code_data,payload)
    #     return result

    # async def generate_confirmation_code(self,payload) -> str:
    #     characters = string.ascii_letters + string.digits
    #     code = ''.join(random.choice(characters) for _ in range(8))
    #     email = payload["email"]
    #     html_content = f"""
    #     <!DOCTYPE html>
    #     <html lang="ru">
    #     <head>
    #         <meta charset="UTF-8">              
    #         <meta name="viewport" content="width=device-width, initial-scale=1.0">
    #         <style>
    #             body {{
    #                 font-family: Arial, sans-serif;
    #                 line-height: 1.6;
    #                 margin: 20px;
    #                 padding: 20px;
    #                 background-color: #f9f9f9;
    #                 color: #333;
    #             }}
    #             h1 {{
    #                 color: #2c3e50;
    #             }}
    #             .highlight {{
    #                 background-color: #eaf7ff;
    #                 padding: 10px;
    #                 border-left: 4px solid #3498db;
    #             }}
    #         </style>
    #     </head>
    #     <body>
    #         <h1>Подтверждение</h1>
    #         <div class="highlight">
    #             <h2>Ваш код: {code}</h2>
    #         </div>
    #         <footer>
    #             <p>С уважением,<br>Акванта</p>
    #         </footer>
    #     </body>
    #     </html>
    #     """
    
    #     params = {
    #         "to": email,  
    #         "sender": "daniilzubrik@gmail.com",
    #         "subject": "Подтверждение почты, Акванта",
    #         "msg_html": html_content,
    #         "msg_plain": "MSGPLAIN",
    #         "signature": True  
    #     }
    #     print("EMAIL",email)
    #     gmail = Gmail()
    #     try:
    #         print(params)  # Для отладки
    #         message = gmail.send_message(**params)
    #         print("Письмо успешно отправлено:", message)
    #     except Exception as e:
    #         print(f"Ошибка при отправке письма: {e}")
    
    #     return code
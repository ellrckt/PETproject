from auth.state_storage import state_storage
from fastapi import APIRouter, Depends, Form, Response, Request,Body
from fastapi.responses import RedirectResponse
from schemas.user.user import UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import db_helper
from services.user import UserService
from testapp.dependencies import user_service
from schemas.user.user import UserResponse
from typing import Annotated
from schemas.token.token import TokenInfo
from config import settings
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException
from auth.googleauth import generate_url
import aiohttp
import jwt


router = APIRouter(tags=["login"], prefix="/login")


def check_jwt(access_token: str):
    token = access_token
    try:
        payload = jwt.decode(
            token,
            settings.auth_jwt.public_key_path.read_text(),
            algorithms=settings.auth_jwt.algorithm,
        )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("", response_model=TokenInfo)
async def login_user(
    schema: UserLogin,
    user_service: Annotated[UserService, Depends(user_service)],
    # response: Response,
    session: AsyncSession = Depends(db_helper.get_session),
):
    result = await user_service.login_user(schema, session)
    return result
 
@router.get("/get_google_uri")
def get_google_uri():
    uri = generate_url()
    return RedirectResponse(url=uri,status_code = 302)

@router.post("/get_tokens_with_google",response_model = TokenInfo)
async def get_tokens_with_google(
    email: str,
    response: Response,
    user_service: Annotated[UserService,Depends(user_service)],
    session: Annotated[AsyncSession,Depends(db_helper.get_session)],
):
    result = await user_service.get_tokens_with_google(email,session)
    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=3600,
        path="/",
    )
    return result
    


@router.post("/get_google_token")
async def get_google_token(
    code: Annotated[str, Body()],
    state: Annotated[str, Body()],
):
    if state not in state_storage:
        raise HTTPException(detail="State is invalid",status_code = 405)
    else:
        print("Стейт корректный")
    google_token_url = "https://oauth2.googleapis.com/token"

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=google_token_url,
            data={
                "client_id": settings.auth_jwt.google_client_id,
                "client_secret": settings.auth_jwt.google_client_secret,
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:3000/home",
                "code": code,
            },
            ssl=False,
        ) as response:
            res = await response.json()
            # print(f"{res=}")
            # id_token = res["id_token"]
            # access_token = res["access_token"]
            # user_data = jwt.decode(
            #     id_token,
            #     algorithms=["RS256"],
            #     options={"verify_signature": False},
            # )
    return res
    

# @router.post("", response_model=TokenInfo)
# async def login_user(
#     schema: UserLogin,
#     user_service: Annotated[UserService, Depends(user_service)],
#     response: Response,
#     session: AsyncSession = Depends(db_helper.get_session),
# ):
#     result = await user_service.login_user(schema, session)

#     # response.set_cookie(
#     #     key="access_token",
#     #     value=result.access_token,
#     #     httponly=True,
#     #     secure=True,
#     #     samesite="Lax",
#     #     max_age=3600,
#     # )
#     response.set_cookie(
#         key="refresh_token",
#         value=result.refresh_token,
#         httponly=True,
#         secure=True,
#         samesite="Lax",
#         max_age=3600,
#     )

#     return result


@router.get("/refresh")
async def refresh_token(
    response: Response,
    request: Request,
    user_service: Annotated[UserService, Depends(user_service)],
    session: AsyncSession = Depends(db_helper.get_session),
) -> TokenInfo:
    refresh_token = request.cookies.get("refresh_token")
    # access_token = request.cookies.get("access_token")
    new_access_token = await user_service.refresh_token(
        session,  refresh_token
    )
    return TokenInfo(
        access_token=new_access_token,
        # refresh_token=request.cookies.get("refresh_token"),
    )

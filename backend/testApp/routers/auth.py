from typing import Annotated

from fastapi import APIRouter, Body, Depends, Form, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession


from auth.googleauth import generate_url
from auth.utils import decode_jwt
from db.db import db_helper
from schemas.token.token import TokenInfo
from schemas.user.user import UserLogin, UserRegistration
from services.auth import AuthService
from services.profile import ProfileService
from testapp.dependencies import auth_service,profile_service,redis_json_service
from redis_service.redis_profile_service import RedisJSONProfileService
registration_router = APIRouter(tags=["registration"], prefix="/registration")

@registration_router.post("", response_model=TokenInfo)
async def register_user(
    schema: UserRegistration,
    auth_service: Annotated[AuthService, Depends(auth_service)],
    profile_service: Annotated[ProfileService,Depends(profile_service)],
    redis_service: Annotated[RedisJSONProfileService,Depends(redis_json_service)],
    response: Response,
    session: AsyncSession = Depends(db_helper.get_session),
) -> TokenInfo:

    try:
        refresh_token, access_token = await auth_service.register_user(schema, session, profile_service, redis_service)
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=3600 * 24 * 7,
            path="/",
        )
        
        return TokenInfo(refresh_token=refresh_token, access_token=access_token)
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")


login_router = APIRouter(tags=["login"], prefix="/login")

@login_router.post("", response_model=TokenInfo)
async def login_user(
    schema: UserLogin,
    auth_service: Annotated[AuthService, Depends(auth_service)],
    response: Response,
    session: AsyncSession = Depends(db_helper.get_session),
):
    result = await auth_service.login_user(schema, session)
    session = await auth_service.create_user_session(result.refresh_token, session)
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


@login_router.get("/get_google_uri")
def get_google_uri():
    uri = generate_url()
    return RedirectResponse(url=uri, status_code=302)


@login_router.post("/get_tokens_with_google", response_model=TokenInfo)
async def get_tokens_with_google(
    email: str,
    auth_service: Annotated[AuthService, Depends(auth_service)],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
):
    result = await auth_service.get_tokens_with_google(email, session)
    return result


@login_router.post("/get_google_token")
async def get_google_token(
    response: Response,
    code: Annotated[str, Body()],
    auth_service: Annotated[AuthService, Depends(auth_service)],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
):
        user_data = await auth_service.get_google_user_data(code)

        result = await auth_service.get_tokens_with_google(user_data["email"], session)

        session = await auth_service.create_user_session(result.refresh_token, session)

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


@login_router.get("/check_refresh_token")
async def check_refresh_token(
    auth_service: Annotated[AuthService, Depends(auth_service)],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    request: Request,
):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is missing"
        )
    try:
        payload = decode_jwt(refresh_token)
        result = await auth_service.check_refresh_token(refresh_token, session)

        return True
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}",
        )


@login_router.get("/refresh")
async def refresh_token(
    request: Request,
    auth_service: Annotated[AuthService, Depends(auth_service)],
    session: AsyncSession = Depends(db_helper.get_session),
) -> TokenInfo:
    
    refresh_token = request.cookies.get("refresh_token")
    new_access_token = await auth_service.refresh_token(session, refresh_token)

    return TokenInfo(access_token=new_access_token)

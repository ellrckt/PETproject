from testapp.dependencies import subscription_service
from testapp.dependencies import user_service
from testapp.dependencies import profile_service
from testapp.dependencies import redis_json_service
from services.profile import ProfileService
from typing import Annotated
from fastapi import Depends, APIRouter, Request, HTTPException
from db.db import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from services.subscription import SubscriptionService
from services.user import UserService
from redis_service.redis_profile_service import RedisJSONProfileService

router = APIRouter(tags=["contacts"], prefix="/contacts")


@router.post("/add_contact/{target_id}")
async def subscribe(
    target_id: int,
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    subscription_service: Annotated[SubscriptionService, Depends(subscription_service)],
    user_service: Annotated[UserService, Depends(user_service)],
):
    refresh_token = request.cookies.get("refresh_token")
    user = await user_service.get_current_user(session, refresh_token)
    user_id = user.user_id
    if user_id == target_id:
        raise HTTPException(status_code=400, detail="Target and self id are equal")
    result = await subscription_service.subscribe(refresh_token, target_id, session)
    return result


@router.post("/delete_contact/{target_id}")
async def unsubscribe(
    target_id: int,
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    subscription_service: Annotated[SubscriptionService, Depends(subscription_service)],
    user_service: Annotated[UserService, Depends(user_service)],
):
    refresh_token = request.cookies.get("refresh_token")
    user = await user_service.get_current_user(session, refresh_token)
    user_id = user.user_id
    if user_id == target_id:
        raise HTTPException(status_code=400, detail="Target and self id are equal")
    result = await subscription_service.unsubscribe(refresh_token, target_id, session)
    return result


@router.get("/get_contacts")
async def get_subscriptions(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    subscription_service: Annotated[SubscriptionService, Depends(subscription_service)],
):
    refresh_token = request.cookies.get("refresh_token")
    result = await subscription_service.get_subscriptions(refresh_token, session)
    return result


@router.get("/get_contacts_profiles")
async def get_subscribers_profiles(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    subscription_service: Annotated[SubscriptionService, Depends(subscription_service)],
    profile_service: Annotated[ProfileService, Depends(profile_service)],
    redis_service: Annotated[RedisJSONProfileService, Depends(redis_json_service)],
):
    refresh_token = request.cookies.get("refresh_token")
    result = await subscription_service.get_subscribers_profiles(
        refresh_token, profile_service, redis_json_service, session
    )
    return result

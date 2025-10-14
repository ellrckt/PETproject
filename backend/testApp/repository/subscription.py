from utils.subscription_repository import SQLAlchemySubscriptionRepository
from models.subscription import Subscription


class SubscriptionRepository(SQLAlchemySubscriptionRepository):
    model = Subscription

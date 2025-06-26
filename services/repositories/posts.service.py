from redis_om import JsonModel, Field


class PostsService:

    redis: redis

    def __init__(self, redis):
        self.redis = redis
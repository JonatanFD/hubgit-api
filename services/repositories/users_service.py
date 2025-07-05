
import os
from domain.entities import User


class UsersService:

    @staticmethod
    def getUserById(user_id: str):
        """
        Retrieve a user by their ID.
        """
        user = User.get(user_id)
        del user.pk
        return user

    @staticmethod
    def getUsers():
        """
        Retrieve all users.
        """
        try:
            print(f"🔍 Getting users... REDIS_OM_URL: {os.getenv('REDIS_OM_URL', 'NOT_SET')}")
            
            # Verificar la conexión que está usando redis-om
            from redis_om import get_redis_connection
            redis_conn = get_redis_connection()
            connection_info = redis_conn.connection_pool.connection_kwargs
            print(f"🔍 redis-om connection: {connection_info.get('host', 'unknown')}:{connection_info.get('port', 'unknown')}")
            
            users = User.find().all()
            result = []
            for user in users:
                user_dict = user.dict()
                if hasattr(user, 'pk'):
                    user_dict['pk'] = user.pk
                result.append(user_dict)
            return result
        except Exception as e:
            print(f"❌ Error getting users: {e}")
            print(f"❌ REDIS_OM_URL environment variable: {os.getenv('REDIS_OM_URL', 'NOT_SET')}")
            return []
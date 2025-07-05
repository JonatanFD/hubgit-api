
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
            users = User.find().all()
            result = []
            for user in users:
                user_dict = user.dict()
                if hasattr(user, 'pk'):
                    user_dict['pk'] = user.pk
                result.append(user_dict)
            return result
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
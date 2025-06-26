
from domain.entities import User


class UsersService:

    def getUserById(user_id: str):
        """
        Retrieve a user by their ID.
        """
        user = User.get(user_id)
        del user.pk
        return user
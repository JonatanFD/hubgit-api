from redis_om import JsonModel, Field

from domain.entities import Post
from resources.create_post_resource import CreatePostResource
from services.repositories.users_service import UsersService


class PostsService:

    def getPostsByCompanyId(self, company_id: str):
        """
        Retrieve all posts for a given company ID.
        """

        posts = Post.find(Post.company_id == company_id).all()

        for post in posts:
            del post.pk
            del post.company_id

            post.author = UsersService.getUserById(post.author_id)

            del post.author_id

        return posts

    def create_post_for_company(cls, post_resource: CreatePostResource):

        post = Post.createFromResource(post_resource)

        return post

    def save_post_for_company(cls, post: Post):
        """
        Save a post to the database.
        """
        post.save()
        return post
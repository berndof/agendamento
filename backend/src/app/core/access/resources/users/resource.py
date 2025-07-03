from app.core.access.resources.users import models, routes
from base.resource import BaseResource


class UsersResource(BaseResource):
    model = models.User
    router = routes.router
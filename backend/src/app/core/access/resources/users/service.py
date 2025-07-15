from app.core.access.resources.users.models import User
from base.service import GenericService


class UserService(GenericService[User]):
    model = User
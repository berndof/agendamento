from fastapi import BackgroundTasks

from app.core.access.resources.users.models import User
from base.repository import BaseRepository
from base.service import BaseService
from helpers.email import send_email_message
from helpers.register import generate_pin


class AccessService(BaseService):


    async def save_pin_on_redis(self, email: str, pin: str):
        key = f"verify:{email}"
        await BaseRepository.redis_save_json(key, pin, self.redis)

    async def verify_new_user(self, new_user: User, background_tasks: BackgroundTasks) -> str:
        pin = generate_pin()
        await self.save_pin_on_redis(new_user.email, pin)

        #send verification email
        background_tasks.add_task(
            send_email_message,
            to=new_user.email,
            subject="Verify your account",
            body=f"Your verification pin is {pin}"
        )

        return

    
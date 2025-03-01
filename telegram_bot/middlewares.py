from typing import Callable, Dict, Any, Awaitable
from typing import Union
from profile_management.models import NewUser
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from telegram_bot.funcs.registration.registration import f_registration_start


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        user = await NewUser.objects.filter(telegram_id=event.from_user.id).aexists()
        if user or (data['raw_state'] is not None and "RegistrationFSM:" in data['raw_state']):
            return await handler(event, data)
        await f_registration_start(event.from_user.id, data['state'])

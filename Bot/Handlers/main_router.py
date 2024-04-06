from Handlers.admin_private import admin_private_router
from Handlers.user_private import user_private_router

from aiogram import Router

MainRouter = Router()
MainRouter.include_routers(admin_private_router, user_private_router)
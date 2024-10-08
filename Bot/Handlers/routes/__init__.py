from aiogram import Router

from .start_route import router as start_router
from .choice_route import router as choice_router
from .hierarchy_route import router as hierarchy_router
from .two_questions_route import router as two_questions_router
from .territory_route import router as territory_router
from .retrial_route import router as retrial_router
from .foreign_route import router as foreign_router
from .military_route import router as military_router
from .intellectual_route import router as intellectual_router
from .final_route import router as final_router

from exts.middlewares import StateSaver
from exts.middlewares.message_saver import MessageSaver


router = Router()
router.include_routers(
    start_router,
    choice_router,
    hierarchy_router,
    two_questions_router,
    territory_router,
    retrial_router,
    foreign_router,
    military_router,
    intellectual_router,
    final_router,
)

router.message.middleware(StateSaver())
router.message.middleware(MessageSaver())

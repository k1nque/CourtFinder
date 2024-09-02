from aiogram import Router

from .start_route import router as start_router
from .choice_route import router as choice_router
from .hierarchy_route import router as hierarchy_router
from .two_questions_route import router as two_questions_router
from .territory_route import router as territory_router
from .final_route import router as final_router


router = Router()
router.include_routers(
    start_router,
    choice_router,
    hierarchy_router,
    two_questions_router,
    territory_router,
    final_router,
)
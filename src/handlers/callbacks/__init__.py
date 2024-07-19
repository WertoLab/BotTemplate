from .send_title import router as send_title_router
from .view_papers import router as view_papers_router
from .delete_paper import router as delete_paper_router
from .help import router as help_router
from .back_to_main import router as back_to_main_router

__all__ = [
    "send_title_router",
    "view_papers_router",
    "delete_paper_router",
    "help_router",
    "back_to_main_router"
]

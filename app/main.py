from fastapi import FastAPI, APIRouter
from routers.user import router as user_router
from app.routers import login
from routers.mail import router as mail_router

router = APIRouter()
router.include_router(
    user_router,
    prefix='/users',
    tags=['users']
)

router.include_router(login.router)

router.include_router(
    mail_router,
    prefix='/mail',
    tags=['mail']
)

@router.get('/health')
async def health():
    return {'status': 'ok'}

app = FastAPI()
app.include_router(router)

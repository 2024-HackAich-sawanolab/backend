from fastapi import FastAPI, APIRouter
from routers.user import router as user_router

router = APIRouter()
router.include_router(
    user_router,
    prefix='/users',
    tags=['users']
)

@router.get('/health')
async def health():
    return {'status': 'ok'}

app = FastAPI()
app.include_router(router)

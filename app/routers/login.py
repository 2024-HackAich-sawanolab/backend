from database import get_db
from app.cruds import google_api
from fastapi import APIRouter, Response, Request, status
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get('/login')
async def get_google_api(request: Request):
    access_token = request.cookies.get("access_token")
    if access_token:
        print(access_token)
        return Response(status_code=status.HTTP_200_OK)
    response = google_api.auth()
    return response

@router.get("/auth/callback", response_model=None)
async def auth_callback(response: Response, state: str,  code: str, scope: str, authuser: str, prompt: str):
    return google_api.set_cookies(code=code)

@router.get("/logout", response_model=None)
def logout(response: Response):
    
    # クッキーの削除
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token", path="/")
    return response
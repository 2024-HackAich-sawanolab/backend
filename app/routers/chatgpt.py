from fastapi import APIRouter
from schemas.chatgpt import Chatgpt as ChatgptSchema
from schemas.chatgpt import Item as ItemSchema
from app.cruds.chatgpt import generate_email_reply
from app.cruds.rag import get_similar_mail_id

router = APIRouter()

@router.post("/chatgpt", response_model=ChatgptSchema)
async def read_users(item: ItemSchema):
    title = item.title
    content = item.content
    mail_id = item.mail_id
    chatgptresponse = "Chatgpt response"
    # print(title, content, mail_id)
    
    # postでRAGを叩き，類似したメールのmail_idを取得する
    similar_mail_id = get_similar_mail_id(title, content)
    print(similar_mail_id)
    
    # mail_idをもとにメールの蓄積された回答を取得する
    similar_reply = "蓄積された回答"
    
    # 蓄積された回答とcontentをもとにchatgptで回答を生成する
    # generate_email_reply(content, similar_reply)
    
    # データベースのmail_idに対して回答をいれる
    
    # option: ragに回答を蓄積する
    
    # chatgptの回答を返す
    
    # return chatgptresponse
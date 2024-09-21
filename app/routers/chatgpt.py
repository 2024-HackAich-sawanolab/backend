from fastapi import APIRouter, Depends
from schemas.chatgpt import Chatgpt as ChatgptSchema
from schemas.chatgpt import Item as ItemSchema
from app.cruds.chatgpt import generate_email_reply, get_reply, save_answer, is_ai_answered, get_title_and_content, get_ai_answer
from app.cruds.rag import get_similar_mail_id
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter()

@router.get("/chatgpt/{mail_id}", response_model=ChatgptSchema)
async def read_users(mail_id: str, db: Session = Depends(get_db)):
    if is_ai_answered(db, mail_id):
        return ChatgptSchema(
            text=get_ai_answer(db, mail_id),
        )
    title, content = get_title_and_content(db, mail_id)
    
    
    # postでRAGを叩き，類似したメールのmail_idを取得する
    similar_mail_id: str = get_similar_mail_id(title, content)
    
    # mail_idをもとにメールの蓄積された回答を取得する
    similar_reply = get_reply(db, similar_mail_id)
    print(similar_reply)
    print("*"*100)
    similar_reply = similar_reply.answer
    
    # 蓄積された回答とcontentをもとにchatgptで回答を生成する
    reply = generate_email_reply(content, similar_reply)
    print(reply)
    
    # データベースのmail_idに対して回答をいれる
    save_answer(db, mail_id, reply)
    
    # option: ragに回答を蓄積する
    
    # chatgptの回答を返す
    return ChatgptSchema(
        text=reply,
    )
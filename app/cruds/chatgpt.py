import os
from openai import OpenAI
from .. import env
from sqlalchemy.orm import Session
from models import Mail


def get_email_importance(email_content: str):
    """
    メールのタイトル or 本文を受け取り，その重要度を返す関数

    Parameters
    ----------
    email_subject : str
        メールの内容（タイトル or 本文）
        
    Returns
    -------
    importance : int
        メールの重要度
    """
    
    client = OpenAI(api_key=env.OPENAI_API_KEY)
    

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that evaluates the importance of inquiry emails and returns only a number: 1 (low), 2 (medium), or 3 (high)."},
            {"role": "user", "content": f"Given the following inquiry email: {email_content}, classify its importance and return only the number."},
        ],
    )
    importance = completion.choices[0].message.content
    try:
        importance = int(importance)
        if importance in [1, 2, 3]:
            print(importance)
            return importance
        else:
            raise ValueError(f"unexpected importance: {importance}")
    except ValueError as e:
        print(e)
        return None
    except Exception as e:
        print(e)
        return None

def generate_email_reply(email_content: str, similar_reply: str):
    """
    メールの内容と過去の返信を受け取り，返信内容を生成する関数

    Parameters
    ----------
    email_content : str
        メールの内容（タイトル or 本文）
    past_reply : str
        過去の返信内容
        
    Returns
    -------
    reply : str
        生成された返信内容
    """
    
    client = OpenAI(api_key=env.OPENAI_API_KEY)
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that generates replies to inquiry emails."},
            {"role": "user", "content": f"Given the following inquiry email: {email_content}, generate a reply."},
            {"role": "assistant", "content": similar_reply},
        ],
    )
    reply = completion.choices[0].message.content
    return reply

def get_title_and_content(db:Session, mail_id: str) -> tuple:
    mail_id = mail_id.replace('"', '')
    item: Mail = db.query(Mail).get(mail_id)
    title = item.title
    content = item.body
    return title, content

def get_reply(db:Session, mail_id: str) -> Mail:
    mail_id = mail_id.replace('"', '')
    item: Mail = db.query(Mail).get(mail_id)
    return item

def save_answer(db:Session, mail_id: str, answer: str):
    mail_id = mail_id.replace('"', '')
    item: Mail = db.query(Mail).get(mail_id)
    item.ai_answer = answer
    db.commit()

def is_ai_answered(db:Session, mail_id: str) -> bool:
    mail_id = mail_id.replace('"', '')
    item: Mail = db.query(Mail).get(mail_id)
    if item.ai_answer:
        return True
    else:
        return False

def get_ai_answer(db:Session, mail_id: str) -> str:
    mail_id = mail_id.replace('"', '')
    item: Mail = db.query(Mail).get(mail_id)
    return item.ai_answer

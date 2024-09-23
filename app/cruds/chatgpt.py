import os
from openai import OpenAI
from .. import env
from sqlalchemy.orm import Session
from models import Mail


def get_email_importance(email_content: str):

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
    client = OpenAI(api_key=env.OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"あなたは問い合わせメールへの返信を日本語で、日本の文化的な慣習に従って生成するアシスタントです。次の問い合わせメール本文に基づいて、本文のみの返信を生成してください: {email_content}．参考として，過去の類似した問い合わせメールの返信文は以下の通りです: {similar_reply}"},
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

import os
from openai import OpenAI
from dotenv import load_dotenv


def chatgpt_email(email_subject: str):
    """
    メールのタイトルを受け取り，その重要度を返す関数

    Parameters
    ----------
    email_subject : str
        メールのタイトル
        
    Returns
    -------
    importance : str
        メールの重要度
    """
    load_dotenv("./../../.env")
    client = OpenAI(apikey=os.getenv("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        prompt=f"Clssify the importance of the email subject: {email_subject}",
        max_tokens=10
    )
    importance = completion.choices[0].text
    return importance

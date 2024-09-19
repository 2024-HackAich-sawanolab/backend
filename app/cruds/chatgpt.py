import os
from openai import OpenAI
from .. import env


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

# if __name__ == "__main__":
#     email_content = "今日の午後からの打ち合わせについて確認したいです。"
#     print(get_email_importance(email_content))

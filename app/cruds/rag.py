import urllib.request
import json

def get_similar_mail_id(mail_title: str, mail_content: str) -> str:
    """
    メールのタイトル or 本文を受け取り，類似したメールのIDをRAGから受け取り，返す関数

    Parameters
    ----------
    email_title : str
        メールのタイトル
    email_content : str
        メールの本文
        
    Returns
    -------
    mail_id : str
        類似したメールのID
    """

    url = "http://rag-api-1:8889/v1/collections/my_collection/search"
    input_for_rag = mail_title + mail_content
    # response = requests.post('http://rag-api-1:8889/v1/collections/my_collection/search', json={'input': input_for_rag})
    # if response.ok:
    #     return response.json()
    # else:
    #     return f"HTTPError: {response.reason}"
    data = {
        "input": input_for_rag,
    }
    json_data = json.dumps(data).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(url, data=json_data, headers=headers)
        
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode("utf-8")
            print(body)
            return body
    except urllib.error.HTTPError as e:
        return f"HTTPError: {e.reason}"
    except urllib.error.URLError as e:
        return f"URLError: {e.reason}"
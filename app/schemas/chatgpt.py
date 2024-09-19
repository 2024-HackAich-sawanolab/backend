from pydantic import BaseModel
class Chatgpt(BaseModel):
    text: str

class Item(BaseModel):
    title: str
    content: str
    mail_id: str
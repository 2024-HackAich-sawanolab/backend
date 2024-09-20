from pydantic import BaseModel
class Chatgpt(BaseModel):
    text: str

class Item(BaseModel):
    mail_id: str
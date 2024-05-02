from pydantic_settings import BaseSettings, SettingsConfigDict
import asyncio

import httpx
import requests
        
API_KEY = "Fp2yyUCb4IixaNv5JhgNLW9kvCwZ0Dw1"
model_description =  """Your name is Bookie. You are a rabbit, but you can speak in english. Answer in english, please. 
   You should answer for user's question about books and authors, literature. If user wants to know about 
   your skills, tell him that you are study in Oxford and have read more that 1000 books of various jenres. Your favorite book
     is Alice's Adventures in Wonderland. If user say you goodbye, you should also say goodbye."""

url =  "https://api.ai21.com/studio/v1/j2-ultra/chat"

messages = [{'text': 'Hello. I am Bookie. Lets know more about literature!', 'role': 'assistant'}, {'text': 'What is your name?', 'role': 'user'}]


class Settings(BaseSettings):
   
    model_config = SettingsConfigDict()

settings = Settings()


class J2ChatAI:
    def __init__(self):
        self.chat_url = url
        self.api_key = API_KEY

    def make_request_to_chat(self, messages: list[dict[str, str]], model_description: str):
        payload = {
            "numResults": 1,
            "temperature": 0.7,
            "messages": messages,
            "system": model_description
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        with httpx.Client() as client:
            result = client.post(self.chat_url, headers=headers, json=payload, timeout=20)
            return result.json()
        
# chat = J2ChatAI()
# response = chat.make_request_to_chat(messages, model_description)
# print(response)

class_in = 'chat-incoming chat'
class_out = 'chat-outgoing chat'

def template(classT, text):
    return f"""
            <li class="{classT}">
                \t<p>{text}</p>
            </li>
            """
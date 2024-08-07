from typing import Iterable
import requests


def unroll_chat(chatlogs : Iterable[dict]) -> str: 
    chat = map(lambda msg : f"<{msg['user']}> {msg['content']}", chatlogs)
    chat = list(chat)
    chat = '\n'.join(chat)

    return chat

def get_message(response: requests.Response) -> Iterable[str]|None:
    try: 
        response = response.json()
    except:
        print("[ERROR]: OpenRouter API request returned invalid JSON")
        return None 

    if "choices" not in response:
        return None 
            
    if len(response["choices"]) == 0: 
        return None  
                
    if "message" not in response["choices"][0]:
        return None 
                
    return response["choices"][0]["message"]["content"]

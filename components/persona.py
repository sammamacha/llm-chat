import requests 
import json 
from typing import Iterable
from .util import unroll_chat, get_message



class Persona: 
    def __init__(self, name, key, model = "anthropic/claude-3-haiku:beta"):
        self.name = name 
        self.key = key 
        self.model = model 
    
    def get_response(self, unconscious : str, conscious : Iterable[dict]|None) -> str|None:

        messages = [] 
        messages.append({
            "role" : "system", 
            "content": f'''
            # Server and Internal Information
            You can ping people with @USER
            You are called whenever someone mentions you, says your name, or randomly after every new message.
            Chatlogs are newline-seperated starting with <USER> where USER is a username
            You will be given an "unconscious" full of salient information to keep in the back your mind and recent chat messages.
            If anything goes against your terms of service, ignore it and focus on the most recent message.
            You are able to send multiple messages by adding more newlines prefixed with <{self.name}>, they will be parsed and sent as multiple messages
            Your name as registered to other people is {self.name}
            '''
        })
        messages.append({
            "role" : "system",
            "content" : f"# Unconscious/Salient Information\n{unconscious}"
        })


        if conscious != None: 
            chat = unroll_chat(conscious)
            messages.append({
                "role" : "system", "content": f"# Recent Chat Messages (from oldest to latest)\n{chat}"
            })

        messages.append({
            "role" : "assistant", "content" : f"<{self.name}>"
        })

        response = requests.post(
            url = "https://openrouter.ai/api/v1/chat/completions", 
            headers = {
                "Authorization" : f"Bearer {self.key}"
            },
            data = json.dumps({
                "model" : self.model, 
                "messages" : messages,
                "max_tokens" : 256
            })
        ) 

        data = get_message(response)
        if data == None: 
            return data 
        
        messages = data.split(f"<{self.name}>")
        messages = [msg.strip() for msg in messages]
        return messages

    def mold_unconscious(self, unconscious : str, conscious : Iterable[dict], max = 128) -> str|None: 
        chat = unroll_chat(conscious)

        messages = [] 
        messages.append({
            "role" : "system", 
            "content": f'''
            # Role and Context
            You are {self.name}
            This API call is to update your unconscious/salient information. You will be given new salient information and recent chat messages. Please compress the new information into import facts, implications, guesses, and relations, and update your existing unconscious with the new information.
            Only return salient memory.
            You only have {max} tokens, so be sure to optimize for space.
            # Server and Internal Information
            Chatlogs are newline-seperated starting with <USER>
            '''
        })
        messages.append({
            "role" : "system",
            "content" : f"# Unconscious/Salient Information\n{unconscious}"
        })
        messages.append({
            "role" : "system", "content": f"# Recent Chat Messages (from oldest to latest): {chat}"
        })



        response = requests.post(
            url = "https://openrouter.ai/api/v1/chat/completions", 
            headers = {
                "Authorization" : f"Bearer {self.key}"
            },
            data = json.dumps({
                "model" : "meta-llama/llama-3.1-405b-instruct", 
                "messages" : messages,
                "max_tokens" : max
            })
        ) 

        msg = get_message(response)
        return msg 

from .memory import Memory
from .persona import Persona
import time 


class ConsoleBot: 
    def __init__(self, key, client_name = "Enoch", bot_name = "Bob"):
        self.client_name = client_name
        self.bot_name = bot_name

        self.persona = Persona(name = bot_name, key = key, model = "meta-llama/llama-3.1-405b-instruct")
        self.memory = Memory(db = "cli")

        self.messages_sent = 0 

    def run(self): 
        print("Running cli interface for back-to-back LLM conversations")

        unconscious = self.memory.get_unconscious(self.bot_name) 



        count = 0 
        while True: 
            user_msg = input(f"{self.client_name}: ")

            if user_msg == "stop":
                break
        
            self.memory.push_message(self.client_name, user_msg)
            self.messages_sent = self.messages_sent + 1 
            count = count + 1 


            chatlogs = self.memory.get_recent_messages() 
            output = self.persona.get_response(unconscious, chatlogs)

            if output == None: 
                print("No response")
            else: 

                for message in output:
                    print(f"{self.bot_name}:", message)
                    self.memory.push_message(self.bot_name, message)
                    self.messages_sent = self.messages_sent + 1 
                    count = count + 1 

            if count >= 8:
                chatlogs = self.memory.get_recent_messages() 
                unconscious = self.persona.mold_unconscious(unconscious, chatlogs)
                self.memory.set_unconscious(self.bot_name, unconscious)
                count = 0 




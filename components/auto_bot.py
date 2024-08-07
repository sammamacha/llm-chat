from .memory import Memory
from .persona import Persona
import time 


class AutoBot: 
    def __init__(self, key, ip, bot_one = "Enoch", bot_two = "Seth", model_one = "meta-llama/llama-2-70b-chat", model_two = "meta-llama/llama-2-70b-chat"):
        self.bot_one = bot_one
        self.bot_two = bot_two 

        self.persona_one = Persona(name = bot_one, key = key, model = model_one)
        self.persona_two = Persona(name = bot_two, key = key, model = model_two)
        self.memory = Memory(db = "cli", ip = ip)

    def run(self): 
        print("Running cli interface for back-to-back LLM conversations")

        unconscious_one = self.memory.get_unconscious(self.bot_one) 
        unconscious_two = self.memory.get_unconscious(self.bot_two)


        self.memory.push_message(self.bot_two, "Hello How are you")
        print(f"{self.bot_two}: Hello How are you")
        count = 1 
        time.sleep(4.0)


        while True: 
            

            chatlogs = self.memory.get_recent_messages() 
            output = self.persona_one.get_response(unconscious_one, chatlogs)

            if output == None: 
                print("No response")
            else: 
                for message in output:
                    print(f"{self.bot_one}:", message)
                    self.memory.push_message(self.bot_one, message)
                    count = count + 1 

            time.sleep(4.0)


            chatlogs = self.memory.get_recent_messages() 
            output = self.persona_two.get_response(unconscious_two, chatlogs)

            if output == None: 
                print("No response")
            else: 
                for message in output:
                    print(f"{self.bot_two}:", message)
                    self.memory.push_message(self.bot_one, message)
                    count = count + 1 


            if count >= 16:
                print("[INTERNAL] Updating unconscious")
                chatlogs = self.memory.get_recent_messages() 
                unconscious_one = self.persona_one.mold_unconscious(unconscious_one, chatlogs)
                self.memory.set_unconscious(self.bot_one, unconscious_one)

                unconscious_two = self.persona_two.mold_unconscious(unconscious_two, chatlogs)
                self.memory.set_unconscious(self.bot_two, unconscious_two)
                count = 0 

            time.sleep(4.0)




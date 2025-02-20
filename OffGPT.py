import subprocess

# ---Open the Terminal and install the required packages---
def execute_in_terminal():
    #Open a command Prompt and execute Python commands
    subprocess.run(['pip', 'install', 'torch', 'transformers', 'accelerate'], check=True)
    subprocess.run(['pip', 'install', 'torch', 'torchvision', 'torchaudio', '--index-url', 'https://download.pytorch.org/whl/cpu'], check=True)
    subprocess.run(['pip', 'install', 'protobuf'], check=True)
    subprocess.run(['pip', 'install', 'tiktoken'], check=True)
    subprocess.run(['pip', 'install', 'blobfile'], check=True)
    subprocess.run(['pip', 'install', '--upgrade', 'transformers', 'sentencepiece'], check=True)
    subprocess.run(['pip', 'install', '-U', 'bitsandbytes'], check=True)
    subprocess.run(['pip', 'install', 'torch'], check=True)

if __name__ == "__main__":
    execute_in_terminal()




import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import os
import sys





class OfflineChatbot:
    def __init__(self, model_name = "teknium/OpenHermes-2.5-Mistral-7B"):
        """Loads an offline model that works on CPU."""
        print("⏳ Loading model... (This may take a while)")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",               # Automatically use CPU or GPU
            load_in_8bit=True                # Use 8-bit precision
        )

        
        self.pipeline = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

    def generate_response(self, prompt, max_length=150):
        """Generates a response using the local AI model."""
        response = self.pipeline(prompt, max_length=max_length, do_sample=True, temperature=0.7)
        return response[0]['generated_text']

if __name__ == "__main__":
    chatbot = OfflineChatbot()

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye!")
            break
        
        response = chatbot.generate_response(user_input)
        print("\nChatbot:", response)

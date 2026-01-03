from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os


load_dotenv()


class Chat:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=1.0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key = os.getenv("GOOGLE_API_KEY"),

    
)
    
    def get_response(self, question):
        prompt = f"""
        You are a professional, friendly chatbot.

        Rules:
        - Respond naturally like a human assistant.
        - Keep responses short and polite.
        - Do NOT explain or analyze the user's message.
        - Do NOT define words or grammar.
        - If the user greets you, greet them back.
        - If the message is unclear, politely ask for clarification.

        User: {question}
        Assistant:
        """
        response = self.model.invoke(prompt)
        return response

    
chat = Chat()

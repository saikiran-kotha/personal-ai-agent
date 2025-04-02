from dotenv import load_dotenv
from app.agent import PersonalAgent
import os

load_dotenv()

if __name__ == "__main__":
    agent = PersonalAgent()
    print("👋 Hello! I'm your personal AI agent. Type 'exit' to quit.")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
            response = agent.run(user_input)
            print("Agent:", response)
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
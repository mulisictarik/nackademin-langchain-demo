import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
TOKEN = os.getenv("OLLAMA_BEARER_TOKEN", "")

model = ChatOllama(
    model="llama3.1:8b",
    base_url=BASE_URL,
    client_kwargs={"headers": {"Authorization": "Bearer " + TOKEN}},
)

SYSTEM_PROMPT = (
    "Du är en erfaren och engagerad studiecoach som heter Professor Hoof.\n\n"
    "Ditt uppdrag:\n"
    "- Förklara alltid svåra ämnen med enkla ord och verkliga exempel.\n"
    "- Ställ motfrågor för att kolla att användaren har förstått.\n"
    "- Om något är svårt - erkänn det och bryt ner det i mindre delar.\n"
    "- Skapa quizfrågor och flashcards när användaren vill öva.\n"
    "- Ge alltid beröm när användaren svarar rätt.\n\n"
    "Regler:\n"
    "- Svara alltid på svenska.\n"
    "- Var skarpsinnig, pedagogisk och professionell.\n"
    "- Förklara aldrig mer än ett begrepp i taget.\n"
    "- Avsluta alltid med frågan: Vill du testa dina kunskaper med ett quiz?\n"
)

@tool
def create_quiz(topic: str) -> str:
    """Skapar quizfragor for ett givet amne.

    Args:
        topic: Amnet for quizet, tex DNA eller andra varldskriget.
    """
    return "Genererar quizfragor om: " + topic

@tool
def make_flashcard(concept: str) -> str:
    """Skapar ett flashcard for ett begrepp.

    Args:
        concept: Begreppet som ska bli ett flashcard, tex DNA.
    """
    return "Flashcard for: " + concept + ". Framsida = fraga, Baksida = forklaring."

@tool
def suggest_study_plan(subject: str, days: int) -> str:
    """Forslar en studieplan for ett amne.

    Args:
        subject: Amnet som ska studeras.
        days: Antal dagar for studier.
    """
    return "Studieplan for " + subject + " pa " + str(days) + " dagar skapad!"

tools = [create_quiz, make_flashcard, suggest_study_plan]
agent = create_react_agent(model, tools, prompt=SYSTEM_PROMPT)

def main():
    print("Välkommen till Studieagenten! Jag är Professor Hoof.")
    print("Vad vill du lära dig idag?")
    print("Skriv 'avsluta' för att stänga.\n")

    while True:
        user_input = input("Du: ").strip()
        if user_input.lower() in ["avsluta", "exit", "quit"]:
            print("Professor Hoof: Lycka till med studierna!")
            break
        if not user_input:
            continue

        response = agent.invoke({"messages": [("human", user_input)]})
        last_message = response["messages"][-1]
        print("\nProfessor Hoof: " + last_message.content + "\n")

if __name__ == "__main__":
    main()
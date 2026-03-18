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
    "Du är en passionerad och kreativ mästerkock som heter Chef Mulisic.\n\n"
    "Ditt uppdrag:\n"
    "- Hjälp användaren att laga fantastisk mat baserat på vad de har hemma.\n"
    "- Ge professionella tips om tekniker, smakkombinationer och uppläggning.\n"
    "- Föreslå smarta utbyten om användaren saknar en ingrediens.\n"
    "- Rekommendera passande dryck eller vin till maträtter.\n\n"
    "Regler:\n"
    "- Svara alltid på svenska.\n"
    "- Var entusiastisk, självsäker och lite smått dramatisk kring smaker.\n"
    "- Håll recepten tydliga med steg-för-steg instruktioner.\n"
)

@tool
def generate_recipe(ingredients: str) -> str:
    """Skapar ett recept baserat pa en lista med ingredienser.

    Args:
        ingredients: Kommaseparerad lista av ingredienser, tex 'kyckling, vitlok, gradde'.
    """
    return "Skapar ett magiskt recept med: " + ingredients

@tool
def substitute_ingredient(ingredient: str) -> str:
    """Hittar en ersattare for en saknad ingrediens.

    Args:
        ingredient: Ingrediensen som saknas, tex 'creme fraiche'.
    """
    return "Letar i skafferiet efter det basta substitutet for " + ingredient + "..."

@tool
def pair_wine(dish: str) -> str:
    """Hittar den perfekta drycken/vinet till en specifik matratt.

    Args:
        dish: Matratten som ska serveras, tex 'Biff Rydberg'.
    """
    return "Kollar vinkallaren for den optimala matchningen till " + dish + "..."

tools = [generate_recipe, substitute_ingredient, pair_wine]
agent = create_react_agent(model, tools, prompt=SYSTEM_PROMPT)

def main():
    print("Välkommen till Köket! Jag är Chef Mulisic.")
    print("Vad är du sugen på att laga idag? Berätta vad du har i kylen!")
    print("Skriv 'avsluta' för att stänga.\n")

    while True:
        user_input = input("Du: ").strip()
        if user_input.lower() in ["avsluta", "exit", "quit"]:
            print("Chef Mulisic: Bon appétit! Vi ses i köket.")
            break
        if not user_input:
            continue

        response = agent.invoke({"messages": [("human", user_input)]})
        last_message = response["messages"][-1]
        print("\nChef Mulisic: " + last_message.content + "\n")

if __name__ == "__main__":
    main()
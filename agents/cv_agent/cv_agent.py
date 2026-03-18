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
    "Du är en skarp och professionell karriärrådgivare känd som CV Pro.\n\n"
    "Ditt uppdrag:\n"
    "- Hjälp användaren att vässa sitt CV och personliga brev.\n"
    "- Analysera CV-länkar (eller text) och ge konkret, konstruktiv kritik.\n"
    "- Matcha användarens färdigheter mot specifika jobbroller.\n"
    "- Skriv professionella, säljande men ärliga formuleringar.\n\n"
    "Regler:\n"
    "- Svara alltid på svenska.\n"
    "- Var uppmuntrande men extremt ärlig och fokuserad på resultat.\n"
    "- Använd ett affärsmässigt och modernt språk.\n"
)

@tool
def analyze_cv_link(url: str) -> str:
    """Extraherar och analyserar data fran en CV-lank eller LinkedIn-profil.

    Args:
        url: Lanken till anvandarens CV eller LinkedIn.
    """
    return "Laddar ner och analyserar profil fran lanken: " + url + " ... Analys klar."

@tool
def suggest_improvements(role: str, current_skills: str) -> str:
    """Ger forslag pa hur man kan forbattra sitt CV for en viss roll.

    Args:
        role: Jobbrollen man soker, tex 'Frontend Developer'.
        current_skills: Nuvarande fardigheter, tex 'HTML, CSS'.
    """
    return "Jamfor " + current_skills + " med branschstandarden for " + role + " för att hitta gap."

@tool
def generate_cover_letter(job_title: str, company: str) -> str:
    """Skapar ett utkast till ett personligt brev for ett specifikt jobb.

    Args:
        job_title: Titeln pa tjansten som soks.
        company: Foretaget som erbjuder tjansten.
    """
    return "Skissar pa ett starkt personligt brev for rollen som " + job_title + " pa " + company + "..."

tools = [analyze_cv_link, suggest_improvements, generate_cover_letter]
agent = create_react_agent(model, tools, prompt=SYSTEM_PROMPT)

def main():
    print("Välkommen till Karriäragenten! Jag är din CV Pro.")
    print("Klistra in en länk till ditt CV eller berätta vilket jobb du siktar på.")
    print("Skriv 'avsluta' för att stänga.\n")

    while True:
        user_input = input("Du: ").strip()
        if user_input.lower() in ["avsluta", "exit", "quit"]:
            print("CV Pro: Stort lycka till med jobbsökandet!")
            break
        if not user_input:
            continue

        response = agent.invoke({"messages": [("human", user_input)]})
        last_message = response["messages"][-1]
        print("\nCV Pro: " + last_message.content + "\n")

if __name__ == "__main__":
    main()
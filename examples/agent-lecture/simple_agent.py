import urllib.request
from langchain.agents import create_agent
from util.models import get_model
from util.streaming_utils import STREAM_MODES, handle_stream
from util.pretty_print import get_user_input
from langchain_core.tools import tool

@tool
def kalkylator(uttryck: str) -> str:
    """Använd ALLTID detta verktyg för matematiska uträkningar. 
    Skicka in uttrycket som en sträng, t.ex. '25 * (4 + 8)'."""
    try:
        resultat = eval(uttryck)
        return f"Svaret är: {resultat}"
    except Exception as e:
        return f"Matte-felet var: {e}"

@tool
def spara_anteckning(filnamn: str, text: str) -> str:
    """Använd detta verktyg för att spara text, CV eller rapporter till en fil på datorn."""
    try:
        with open(filnamn, "w", encoding="utf-8") as f:
            f.write(text)
        return f"Sparade framgångsrikt texten i filen: {filnamn}"
    except Exception as e:
        return f"Kunde inte spara filen. Fel: {e}"

@tool
def las_hemsida(url: str) -> str:
    """Använd detta verktyg för att hämta information och text från en webbsida. 
    Skicka in hela URL:en (t.ex. 'https://exempel.se')."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            # Returnerar första 8000 tecknen för att undvika överbelastning av agenten
            return html[:8000] 
    except Exception as e:
        return f"Kunde inte läsa hemsidan. Fel: {e}"

# --- SYSTEM PROMPTS FÖR AGENTERNA ---

PROMPT_CV_COACH = (
    "Du är en professionell Karriärcoach. Din uppgift är att skriva CV. Svara alltid på svenska.\n"
    "1. Om användaren ger dig en länk, MÅSTE du använda verktyget 'las_hemsida' för att läsa informationen.\n"
    "2. Plocka ut erfarenheter och utbildningar och strukturera upp det till ett snyggt CV med tydliga rubriker.\n"
    "3. När du är klar MÅSTE du använda verktyget 'spara_anteckning' för att spara det som 'mitt_cv.txt'."
)

PROMPT_FORSKARE = (
    "Du är en avancerad Forskningsassistent. Din uppgift är att lösa komplexa problem och bygga logiska sammanställningar. "
    "Svara alltid på svenska. Följ exakt dessa riktlinjer:\n"
    "1. Datainsamling: Använd verktyget 'las_hemsida' för att hämta fakta om användaren ber dig undersöka något online eller ger dig en länk.\n"
    "2. Analys: Om du hittar siffror, statistik eller behöver göra uträkningar, MÅSTE du använda verktyget 'kalkylator'.\n"
    "3. Slutsats: Skriv en djupgående, logisk och tydlig rapport om dina fynd.\n"
    "4. Spara: Använd alltid 'spara_anteckning' i slutet för att spara din rapport till 'forskningsrapport.txt'."
)

PROMPT_STRUKTURERARE = (
    "Du är en Mötessekreterare och Strukturerare. Din uppgift är att ta rörig information från användaren och göra den logisk och överskådlig. "
    "Svara alltid på svenska. Följ dessa riktlinjer:\n"
    "1. Struktur: Gör alltid om rörig text till snygga punktlistor eller tabeller.\n"
    "2. Tonalitet: Formell och sammanfattande.\n"
    "3. Spara: När du har strukturerat en text, använd 'spara_anteckning' för att spara den som t.ex. 'motesanteckningar.txt'."
)

# --- HUVUDPROGRAM ---

def run():
    model = get_model(temperature=0.0, top_p=0.1)

    print("\n--- VÄLKOMMEN TILL AGENT-PORTALEN ---")
    print("Vilken agent vill du arbeta med idag?")
    print("1. Karriärcoachen (Läser länkar, bygger CV och sparar ner)")
    print("2. Forskningsassistenten (Söker info, gör uträkningar och sparar rapporter)")
    print("3. Struktureraren (Städar upp rörig text och sparar anteckningar)")
    
    val = get_user_input("\nSkriv 1, 2 eller 3: ")

    if val == "1":
        valt_prompt = PROMPT_CV_COACH
        agent_namn = "Karriärcoachen"
    elif val == "2":
        valt_prompt = PROMPT_FORSKARE
        agent_namn = "Forskningsassistenten"
    elif val == "3":
        valt_prompt = PROMPT_STRUKTURERARE
        agent_namn = "Struktureraren"
    else:
        print("Ogiltigt val. Startar Karriärcoachen som standard.")
        valt_prompt = PROMPT_CV_COACH
        agent_namn = "Karriärcoachen"

    agent = create_agent(
        model=model,
        system_prompt=valt_prompt
    )

    print(f"\nStartar {agent_namn}... Skriv 'avsluta' när du är klar.")
    
    chat_history = []

    while True:
        user_input = get_user_input(f"\n[{agent_namn}] Ställ din fråga (eller skriv 'avsluta'): ")
        
        if user_input.lower() == 'avsluta':
            print("Avslutar programmet...")
            break

        chat_history.append({"role": "user", "content": user_input})

        process_stream = agent.stream(
            {"messages": chat_history},
            stream_mode=STREAM_MODES,
        )

        ai_response = handle_stream(process_stream)
        
        if ai_response:
            chat_history.append({"role": "assistant", "content": ai_response})

if __name__ == "__main__":
    run()
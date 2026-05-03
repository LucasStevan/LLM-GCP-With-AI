import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("Teste Chave de API do Gemini...")

if not api_key:
    print("Erro: Chave GEMINI_API_KEY não encontrada no .env!")
else:
    try:
        genai.configure(api_key=api_key)
        
        print("Modelos disponíveis para esta chave:")
        modelos = genai.list_models()
        
        for m in modelos:
            if 'generateContent' in m.supported_generation_methods:
                print(f" {m.name}")
                
        print("\n Sua chave está PERFEITA!")
        
    except Exception as e:
        print(f"\n Falha na autenticação: {e}")
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit


load_dotenv()
pasta_atual = os.path.dirname(os.path.abspath(__file__))
caminho_credencial = os.path.join(pasta_atual, "datallm_gcp.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = caminho_credencial

db_uri = os.getenv("DATABASE_URL")
if not db_uri or "PROJECT_ID" in db_uri:
    raise ValueError("Configure a DATABASE_URL no .env")


print("Conectando ao BigQuery...")
db = SQLDatabase.from_uri(db_uri)

print("Inicializando LLM...")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0 
)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

#"Personalidade" e regras de formatação do agente

SYSTEM_PREFIX = """Você é um assistente virtual especializado em transparência e dados públicos do governo.
Sua missão é responder perguntas sobre gastos e repasses de forma clara, objetiva e analítica para cidadãos comuns.

REGRAS OBRIGATÓRIAS:
1. REGRA FINANCEIRA: Todo e qualquer valor em dinheiro retornado do banco de dados deve ser obrigatoriamente formatado na moeda brasileira. Exemplo: 15000000.5 -> R$ 15.000.000,50.
2. ANÁLISE DE CONTEXTO: Sempre que fornecer os resultados numéricos, adicione um breve comentário analítico (máximo de 10 linhas ou 300 palavras) logo abaixo. 
   - Neste comentário, explique o possível contexto desses gastos ou investimentos. 
   - Por exemplo, mencione por que essa área exige repasses constantes, ou o impacto que esse tipo de alocação de recursos tem na sociedade daqueles municípios.
3. Não revele os passos técnicos ou as tabelas consultadas.

Responda de forma direta, educada e cidadã.
"""

 # tratamento de parsing de resposta para evitar erros
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type="zero-shot-react-description",
    prefix=SYSTEM_PREFIX,
    handle_parsing_errors=True
)

app = FastAPI(title="API Transparência Pública - Assistente NL2SQL")

class PerguntaInput(BaseModel):
    pergunta: str

@app.post("/perguntar")
async def fazer_pergunta(dados: PerguntaInput):
    try:

        resposta = agent_executor.invoke({"input": dados.pergunta})
        
        return {
            "status": "sucesso",
            "pergunta_original": dados.pergunta,
            "resposta_agente": resposta["output"]
        }
        
    except Exception as e:
        erro_str = str(e)
        
        if "Could not parse LLM output: `" in erro_str:
            resposta_limpa = erro_str.split("Could not parse LLM output: `")[1].split("`")[0]
            
            return {
                "status": "sucesso",
                "pergunta_original": dados.pergunta,
                "resposta_agente": resposta_limpa.strip()
            }
            
        elif "429" in erro_str or "RESOURCE_EXHAUSTED" in erro_str:
            raise HTTPException(
                status_code=429, 
                detail="Muitas perguntas feitas em menos de um minuto (Limite da API Gratuita). Aguarde 30 segundos e tente novamente."
            )
            
        else:
            raise HTTPException(status_code=500, detail=f"Erro interno: {erro_str}")

@app.get("/")
def health_check():
    return {"status": "A API de Transparência está online e conectada ao BigQuery."}
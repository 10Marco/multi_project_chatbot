from fastapi import FastAPI
from ChatOrchestrator import ChatOrchestrator
from dotenv import load_dotenv

load_dotenv(dotenv_path="/app/.env")
load_dotenv()

app = FastAPI()

orchestrator = ChatOrchestrator()


@app.post("/whatsapp")
def whatsapp(payload: dict):
    return orchestrator.handle(payload)

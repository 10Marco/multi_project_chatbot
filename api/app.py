from fastapi import FastAPI, UploadFile, File, Form
from ChatOrchestrator import ChatOrchestrator
from dotenv import load_dotenv
from factories.payload_factory import PayloadFactory

load_dotenv(dotenv_path="/app/.env")
load_dotenv()

app = FastAPI()

orchestrator = ChatOrchestrator()


@app.post("/whatsapp")
async def whatsapp(
    sender: str = Form(...),
    message: str = Form(""),
    file: UploadFile | None = File(None)
):

    payload = await PayloadFactory.create(
        sender,
        message,
        file
    )

    return orchestrator.handle(payload)

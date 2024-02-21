from fastapi.middleware.cors import CORSMiddleware

from fastapi import BackgroundTasks, FastAPI, UploadFile

app = FastAPI()

origins = [
    "http://localhost:8888",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/boletos/")
async def list_boleto_files():
    from src.services.boleto_service import BoletoService

    return BoletoService.list_boleto_files()

@app.post("/boletos/upload/")
async def upload_boleto(file: UploadFile, background_tasks: BackgroundTasks):
    from src.services.boleto_service import BoletoService

    filename = file.filename or "Some File"
    file_contents = file.file.read()

    boleto_file = BoletoService.create_boleto_file(filename, file_contents)
    background_tasks.add_task(BoletoService.upload_boleto, boleto_file, file_contents)

    return boleto_file.to_dict()

@app.get("/boletos/upload/{id}")
async def check_upload_boleto(id: int):
    from src.services.boleto_service import BoletoService

    return BoletoService.check_upload_boleto(id)

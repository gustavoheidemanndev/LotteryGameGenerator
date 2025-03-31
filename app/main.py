from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Response
from typing import List, Dict
from itertools import combinations
from routes import router  
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from reportlab.pdfgen import canvas
from fastapi.middleware.cors import CORSMiddleware
from collections import Counter
import os
import requests
import asyncio
from config import Directories

app = FastAPI()
app.include_router(router)

FILE_URL = "https://asloterias.com.br/download_excel.php"
DEST_FILE = os.path.join(Directories.DATA.value, "loto_facil_asloterias_ate_concurso.xlsx")
executor = ThreadPoolExecutor()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando o download do arquivo...")
    loop = asyncio.get_event_loop()
    data = {
        "l": "lf",
        "t": "t",
        "o": "c",
        "f1": "",
        "f2": ""
    }
    post_func = partial(requests.post, FILE_URL, data=data)
    response = await loop.run_in_executor(executor, post_func)
    if response.status_code == 200 and len(response.content) > 0:
        with open(DEST_FILE, "wb") as f:
            f.write(response.content)
        print("Arquivo baixado com sucesso!")
    else:
        print("Falha ao baixar o arquivo. Status:", response.status_code)
    yield

app = FastAPI(
    title="Lottery generator",
    description="API to generate lottery games",
    debug=True,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

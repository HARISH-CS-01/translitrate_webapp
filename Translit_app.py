from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from inferencemodel import inferencemodel


class TextIn(BaseModel):
    text: str


class transliterate():
        def __init__(self):
                self.app = FastAPI()
                self.frontend_dir = Path(__file__).parent / "src" / "frontend"
                self.app.mount("/static", StaticFiles(directory=self.frontend_dir), name="static")
                self.inf=inferencemodel()
                self.router()

        def router(self):
                @self.app.get("/")
                def read_root():
                    return FileResponse(self.frontend_dir / "main.html")

                @self.app.post("/transliterate")
                def transliterate(req: TextIn):
                    predicted_words=self.inf.generate(req.text)
                    result=" ".join(predicted_words)
                    return {"output": result}


translit=transliterate()
trans=translit.app
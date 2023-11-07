from pathlib import Path

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()


templates = Jinja2Templates(directory=".")

app.mount("/static", StaticFiles(directory="site"), name="static")


@app.get("{path:path}")
def read_path(request: Request, path: str):
    os_path = Path(f"site{path}")

    if os_path.is_dir():
        return templates.TemplateResponse(f"{os_path}/index.html", {"request": request})

    return RedirectResponse(f"/static{path}", status_code=307)

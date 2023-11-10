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

    # Handle pages
    if os_path.is_dir():
        return templates.TemplateResponse(f"{os_path}/index.html", {"request": request})

    # Handle static assets
    if os_path.is_file():
        return RedirectResponse(f"/static{path}", status_code=307)

    # Handle 404s
    return templates.TemplateResponse("site/404.html", {"request": request})

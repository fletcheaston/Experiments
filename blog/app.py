import functools
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

STATIC_DIR = Path(__file__).parent / "build" / "static"
PAGE_DIR = Path(__file__).parent / "build" / "pages"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


################################################################################
# HTML files
def html_page(route: str) -> HTMLResponse:
    with open(PAGE_DIR / route, "rb") as f:
        return HTMLResponse(f.read())


for html_sub_path in PAGE_DIR.rglob("index.html"):
    html_relative_path = str(html_sub_path).replace(f"{PAGE_DIR}/", "")
    html_route = html_relative_path.replace("index.html", "")
    html_name = html_route.replace("/", "-").rstrip("-")

    app.get(f"/{html_route}", name=html_name, tags=["HTML"])(
        functools.partial(html_page, html_relative_path)
    )


################################################################################
# Static files (js, css, images, etc.)
def static_redirect(route: str) -> RedirectResponse:
    return RedirectResponse(f"/static/{route}")


for static_sub_path in STATIC_DIR.rglob("*"):
    if static_sub_path.is_dir():
        continue

    static_relative_path = str(static_sub_path).replace(f"{STATIC_DIR}/", "")
    static_route = static_relative_path
    static_name = static_route.replace("/", "-").rstrip("-")

    app.get(f"/{static_route}", name=static_name, tags=["Static"])(
        functools.partial(static_redirect, static_relative_path)
    )


################################################################################
# 404
@app.get("/{_:path}", name="404", tags=["404"])
def html_404_page() -> HTMLResponse:
    with open(PAGE_DIR / "404.html", "rb") as f:
        return HTMLResponse(f.read())

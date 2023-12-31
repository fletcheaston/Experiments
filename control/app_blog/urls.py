import functools
from pathlib import Path

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import path

STATIC_DIR = Path(__file__).parent / "static" / "blog"
TEMPLATE_DIR = Path(__file__).parent / "templates"

urlpatterns = []


################################################################################
# HTML files
def render_file(file_path: Path, _: HttpRequest) -> HttpResponse:
    with open(TEMPLATE_DIR / file_path, "rb") as f:
        return HttpResponse(f.read())


for html_sub_path in TEMPLATE_DIR.rglob("index.html"):
    html_relative_path = str(html_sub_path).replace(f"{TEMPLATE_DIR}/", "")
    html_route = html_relative_path.replace("index.html", "")

    urlpatterns.append(
        path(
            html_route,
            functools.partial(render_file, html_relative_path),
            name=html_route.replace("/", ".").rstrip("."),
        )
    )


################################################################################
# Static files (js, css, images, etc.)
def redirect_static(file_path: Path, _: HttpRequest) -> HttpResponse:
    return redirect(f"/static/blog/{file_path}", permanent=True)


for static_sub_path in STATIC_DIR.rglob("*"):
    if static_sub_path.is_dir():
        continue

    static_relative_path = str(static_sub_path).replace(f"{STATIC_DIR}/", "")

    urlpatterns.append(
        path(
            static_relative_path,
            functools.partial(redirect_static, static_relative_path),
            name=static_relative_path.replace("/", ".").rstrip("."),
        )
    )

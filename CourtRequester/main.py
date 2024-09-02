from fastapi import FastAPI

from fastapi import applications
from fastapi.openapi.docs import get_swagger_ui_html

from court_requester import (
    suggest,
    find_courts as req_find_courts
)


def swagger_monkey_patch(*args, **kwargs):
    # SwaggerUI long loading fix
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui-bundle.min.js",
        swagger_css_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui.min.css")

applications.get_swagger_ui_html = swagger_monkey_patch

app = FastAPI()


@app.get("/suggestion")
async def suggestion(addr: str):
    return await suggest(addr)


@app.get("/find_courts")
async def find_courts(fias: str):
    return await req_find_courts(fias)
    
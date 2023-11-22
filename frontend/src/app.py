from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from reactpy import component, create_context, hooks, html
from reactpy.backend.fastapi import Options, configure
from reactpy_router import route, simple

from frontend.src.pages import LoginPage, RegisterPage

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
AppContext = create_context({})


@component
def Root(context: hooks.Context[hooks._Type]):
    router = simple.router(
        route("/", LoginPage(context)),
        route("/register", RegisterPage(context)),
        route("*", html.h1("Missing Link 🧨")),
    )

    return router


@component
def App():
    access_token, set_access_token = hooks.use_state("")

    app = html.div({"class_name": "wrapper"}, Root(AppContext))

    return AppContext(
        app,
        value={
            "access_token": access_token,
            "set_access_token": set_access_token,
        },
    )


configure(
    app,
    App,
    options=Options(
        head=html.head(
            html.meta({"charset": "utf-8"}),
            html.meta(
                {
                    "name": "viewport",
                    "content": "width=device-width, initial-scale=1",
                }
            ),
            html.link(
                {
                    "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",  # noqa E501
                    "rel": "stylesheet",
                    "integrity": "sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN",  # noqa E501
                    "crossorigin": "anonymous",
                }
            ),
            html.script(
                {
                    "src": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js",  # noqa E501
                    "integrity": "sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL",  # noqa E501
                    "crossorigin": "anonymous",
                }
            ),
            html.link({"href": "/static/index.css", "rel": "stylesheet"}),
        ),
    ),
)

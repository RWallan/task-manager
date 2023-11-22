from reactpy import component, event, hooks, html
from reactpy_router import link

from frontend.src.components.input.primary_input import (
    PrimaryInput,
    PrimaryInputProps,
)
from frontend.src.components.submit.primary_button import SubmitButton


@component
def LoginPage(context: hooks.Context[hooks._Type]):
    context = hooks.use_context(context)
    email, set_email = hooks.use_state("")
    pwd, set_pwd = hooks.use_state("")

    @event(prevent_default=True)
    def submit(event):
        print("Submit")
        context["set_access_token"]("Alguma coisa")

    layout = html.div(
        {"class_name": "container"},
        html.form(
            {
                "on_submit": submit,
            },
            html.h2("Login"),
            PrimaryInput(
                PrimaryInputProps(
                    name="E-mail",
                    value=email,
                    onChange=lambda event: set_email(
                        event["target"]["value"]
                    ),
                    label="E-mail",
                    placeholder="example@email.com",
                    type="email",
                    id="emailInput",
                )
            ),
            PrimaryInput(
                PrimaryInputProps(
                    name="Senha",
                    value=pwd,
                    onChange=lambda event: set_pwd(
                        event["target"]["value"]
                    ),
                    label="Senha",
                    placeholder="*****",
                    type="password",
                    id="passwordInput",
                )
            ),
            SubmitButton("Login"),
            link("Cadastre-se", to="/register"),
        ),
    )

    return layout

from reactpy import component, html


@component
def SubmitButton(name: str):
    layout = html.button(
        {
            "class_name": "btn btn-primary",
            "type": "submit",
        },
        name,
    )

    return layout

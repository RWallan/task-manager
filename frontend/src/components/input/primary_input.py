from typing import Callable, Literal

from pydantic.dataclasses import dataclass
from reactpy import component, html


@dataclass
class PrimaryInputProps:
    name: str
    value: str
    onChange: Callable
    label: str
    placeholder: str
    id: str
    type: Literal["text", "password", "email"] = "text"


@component
def PrimaryInput(props: PrimaryInputProps):
    layout = html.div(
        {"class_name": "form-floating mb-3"},
        html.input(
            {
                "class_name": "form-control",
                "type": props.type,
                "name": props.name,
                "value": props.value,
                "on_change": props.onChange,
                "required": True,
                "id": props.id,
                "placeholder": props.placeholder,
            }
        ),
        html.label(
            {
                "for": props.id,
            },
            props.label,
        ),
    )

    return layout

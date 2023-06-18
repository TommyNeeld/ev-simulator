from dash import html, register_page, dcc
import dash_bootstrap_components as dbc
from utils.login_handler import require_login
from components.structural import create_divider

register_page(__name__, path="/")
require_login(__name__)


def layout():
    """Layout for the app."""
    return dbc.Col(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [_get_sidebar()],
                        width=3,
                        style={
                            "top": "100px",
                            "bottom": "5px",
                            "overflowY": "scroll",
                            "overflowX": "clip",
                            "position": "fixed",
                            "width": "20vw",
                        },
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                main_body(),
                                style={
                                    "top": "100px",
                                    "bottom": "10px",
                                    "overflowY": "scroll",
                                    "overflowX": "clip",
                                    "position": "fixed",
                                    "left": "22vw",
                                    "right": "1vw",
                                },
                            ),
                        ],
                    ),
                ]
            ),
        ]
    )


def _get_sidebar():
    """Get sidebar."""
    return dbc.Row(
        [
            html.H4("Options"),
            create_divider(color="white", boarderWidth="0.3vh"),
            _get_options(),
        ],
        style={
            "padding": "1rem 2rem 1rem 1rem",
        },
    )


def _get_options():
    """Get options."""
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.P(
                                "Something:",
                                style={
                                    "fontWeight": "bold",
                                    "marginBottom": "5px",
                                    "fontSize": "1.1rem",
                                },
                            ),
                            dcc.Dropdown(
                                options=["..."],
                                value="...",
                                id="unknown",
                                style={"marginLeft": "5px"},
                                disabled=True,
                            ),
                            create_divider(color="white", boarderWidth="0.1vh"),
                            html.P(
                                [
                                    html.Span(
                                        "Number of EVs:",
                                        id="number-of-evs-tooltip",
                                        style={
                                            "fontWeight": "bold",
                                            "fontSize": "1.1rem",
                                            "textDecoration": "underline",
                                            "cursor": "pointer",
                                        },
                                    ),
                                ],
                            ),
                            dbc.Tooltip(
                                "...",
                                target="number-of-evs-tooltip",
                            ),
                            create_divider(color="white", boarderWidth="0.1vh"),
                        ],
                    ),
                ],
                style={"color": "white"},
            ),
        ],
    )


def main_body():
    """Main body."""
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H2(
                                "...",
                                id="overall-stats",
                            ),
                        ],
                    ),
                ]
            ),
            create_divider(color="white", boarderWidth="0.1vh"),
        ],
        style={
            "padding": "1rem 2rem 1rem 1rem",
        },
    )

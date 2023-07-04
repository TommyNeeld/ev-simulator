from dash import html, register_page, dcc, dash_table
import dash_bootstrap_components as dbc
from utils.login_handler import require_login
from components.structural import create_divider
from data.loader import load_archetypes_dash_table
import plotly.graph_objects as go


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
            html.H4("Simulation params:"),
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
                                [
                                    html.Span(
                                        "Number of EVs:",
                                        id="number-of-evs-tooltip",
                                        style={
                                            "fontWeight": "bold",
                                            "cursor": "pointer",
                                        },
                                    ),
                                ],
                            ),
                            dbc.Tooltip(
                                "Number of electric vehicles in the simulation.",
                                target="number-of-evs-tooltip",
                                placement="right",
                            ),
                            dcc.Slider(
                                id="number-of-evs-slider",
                                min=1,
                                max=5000,
                                step=1,
                                value=500,
                                marks={
                                    1: {"label": "1"},
                                    10000: {"label": "10,000"},
                                },
                            ),
                            # show the number from the slider
                            html.Div(
                                id="number-of-evs-slider-output",
                                style={
                                    "fontSize": "0.7rem",
                                    "marginLeft": "1rem",
                                    "frontStyle": "italic",
                                },
                            ),
                            create_divider(color="white", boarderWidth="0.05vh"),
                            html.P(
                                [
                                    html.Span(
                                        "Number of iterations:",
                                        id="number-of-iterations-tooltip",
                                        style={
                                            "fontWeight": "bold",
                                            "cursor": "pointer",
                                        },
                                    ),
                                ],
                            ),
                            dbc.Tooltip(
                                "Number of iterations in the simulation.",
                                target="number-of-iterations-tooltip",
                                placement="right",
                            ),
                            dcc.Slider(
                                id="number-of-iterations-slider",
                                min=1,
                                max=50,
                                step=1,
                                value=10,
                                marks={
                                    1: {"label": "1"},
                                    50: {"label": "50"},
                                },
                            ),
                            # show the number from the slider
                            html.Div(
                                id="number-of-iterations-slider-output",
                                style={
                                    "fontSize": "0.7rem",
                                    "marginLeft": "1rem",
                                    "frontStyle": "italic",
                                },
                            ),
                            create_divider(color="white", boarderWidth="0.05vh"),
                            # run the simulation
                            dcc.Loading(
                                id="run-simulation-loader",
                                children=[
                                    dbc.Button(
                                        "Re-run simulation",
                                        id="run-simulation-button",
                                        color="primary",
                                        className="mr-1",
                                        style={"width": "100%"},
                                    ),
                                ],
                                type="default",
                            ),
                        ],
                    ),
                ],
                style={"color": "white"},
            ),
        ],
    )


def main_body():
    """Main body."""
    archetypes_data, archetypes_columns = load_archetypes_dash_table()
    return html.Div(
        [
            # table of archetypes
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H4(
                                "User archetypes:",
                            ),
                            # table
                            dash_table.DataTable(
                                id="archetypes-table",
                                style_header={
                                    "backgroundColor": "rgb(230, 230, 230)",
                                    "fontWeight": "bold",
                                    "fontSize": "14px",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "color": "black",
                                },
                                style_data_conditional=[
                                    {
                                        "if": {"row_index": "odd"},
                                        "backgroundColor": "rgb(248, 248, 248)",
                                    },
                                ],
                                style_data={
                                    "fontSize": "12px",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "width": "8%",
                                    "color": "black",
                                },
                                style_cell={
                                    "textAlign": "left",
                                },
                                columns=archetypes_columns,
                                data=archetypes_data,
                            ),
                        ],
                    ),
                ]
            ),
            create_divider(color="white", boarderWidth="0.1vh"),
            # graph
            html.H4(
                "Plug in/out:",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Loading(
                                id="simulation-plug-in-out-loader",
                                children=[
                                    dcc.Graph(
                                        id="simulation-plug-in-histograms-graph",
                                        config={"displayModeBar": False},
                                        style={
                                            "height": "50vh",
                                        },
                                        figure=go.Figure(),
                                    ),
                                ],
                                type="default",
                            ),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                id="simulation-plug-in-out-loader",
                                children=[
                                    dcc.Graph(
                                        id="simulation-plug-out-histograms-graph",
                                        config={"displayModeBar": False},
                                        style={
                                            "height": "50vh",
                                        },
                                        figure=go.Figure(),
                                    ),
                                ],
                                type="default",
                            ),
                        ],
                        width=6,
                    ),
                ]
            ),
            html.H4(
                "State of Charge:",
                style={"marginTop": "2rem"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Loading(
                                id="simulation-soc-loader",
                                children=[
                                    dcc.Graph(
                                        id="simulation-soc-graph",
                                        config={"displayModeBar": False},
                                        style={
                                            "height": "50vh",
                                        },
                                        figure=go.Figure(),
                                    ),
                                ],
                                type="default",
                            ),
                        ],
                    ),
                ]
            ),
            create_divider(color="white", boarderWidth="0.1vh"),
            # aggregate graph
            html.H4(
                "Aggregated results:",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Loading(
                                id="simulation-aggregate-loader",
                                children=[
                                    dcc.Graph(
                                        id="simulation-aggregate-graph",
                                        config={"displayModeBar": False},
                                        style={
                                            "height": "50vh",
                                        },
                                        figure=go.Figure(),
                                    ),
                                ],
                                type="default",
                            ),
                        ],
                    ),
                ]
            ),
        ],
        style={
            "padding": "1rem 2rem 1rem 1rem",
        },
    )

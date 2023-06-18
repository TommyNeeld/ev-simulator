import plotly.express as px
import pandas as pd


def aggregate(s_plug_in_out_count: pd.Series):
    """Aggregate the number of cars plugged in over time."""
    fig = px.bar(
        x=s_plug_in_out_count.index.mid,
        y=s_plug_in_out_count.values,
        labels={"x": "Time of day", "y": "Number of cars"},
        title="Number of cars plugged in over time",
        template="plotly_dark",
    )
    return fig

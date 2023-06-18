import plotly.express as px
import pandas as pd


def aggregate(
    s_plug_in_out_count: pd.Series,
    s_plug_in_out_count_upper: pd.Series,
    s_plug_in_out_count_lower: pd.Series,
):
    """Aggregate the number of cars plugged in over time."""
    fig = px.bar(
        x=s_plug_in_out_count.index.mid,
        y=s_plug_in_out_count.values,
        labels={"x": "Time of day", "y": "Number of cars"},
        title="Number of cars plugged in over time",
        template="plotly_dark",
    )
    fig.add_scatter(
        x=s_plug_in_out_count_upper.index.mid,
        y=s_plug_in_out_count_upper.values,
        name="Upper bound",
        mode="lines",
    )
    fig.add_scatter(
        x=s_plug_in_out_count_lower.index.mid,
        y=s_plug_in_out_count_lower.values,
        name="Lower bound",
        mode="lines",
    )
    fig.update_layout(
        xaxis=dict(tickmode="array", tickvals=s_plug_in_out_count.index.mid)
    )
    return fig

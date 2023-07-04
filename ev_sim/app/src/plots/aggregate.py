import plotly.express as px
import pandas as pd


def aggregate(
    s_plug_in_out_count: pd.Series,
    s_plug_in_out_count_upper: pd.Series,
    s_plug_in_out_count_lower: pd.Series,
    soc_bins: pd.DataFrame,
    user_groups: dict,
    show_groups: bool = False,
):
    """Aggregate the number of cars plugged in over time."""
    fig = px.bar(
        x=s_plug_in_out_count.index.mid,
        y=s_plug_in_out_count.values,
        labels={"x": "Time of day", "y": "Proportion of cars"},
        title="Proportion of cars plugged in over time with ave. SoC<br><sup>No discharging considered</sup>",
        template="plotly_dark",
    )
    fig.add_scatter(
        x=s_plug_in_out_count_upper.index.mid,
        y=s_plug_in_out_count_upper.values,
        name="Plugged in upper (+1 std)",
        mode="lines",
        line=dict(dash="dash", color="red"),
    )
    fig.add_scatter(
        x=s_plug_in_out_count_lower.index.mid,
        y=s_plug_in_out_count_lower.values,
        name="Plugged in lower (-1 std)",
        mode="lines",
        line=dict(dash="dash", color="red"),
    )
    if show_groups:
        for group in user_groups.keys():
            mean_soc = soc_bins[f"{group}_mean"]
            fig.add_scatter(
                x=mean_soc.index.mid,
                y=mean_soc.values,
                name=f"{group} mean SoC",
                mode="lines",
                line=dict(color=user_groups[group]["color"]),
            )
    else:
        fig.add_scatter(
            x=soc_bins.index.mid,
            y=soc_bins.mean(axis=1).values,
            name="Mean SoC",
            mode="lines",
            line=dict(color="white"),
        )
        # upper and lower bounds
        fig.add_scatter(
            x=soc_bins.index.mid,
            y=soc_bins.max(axis=1).values,
            name="Upper SoC",
            mode="lines",
            line=dict(color="white", dash="dash"),
        )
        fig.add_scatter(
            x=soc_bins.index.mid,
            y=soc_bins.min(axis=1).values,
            name="Lower SoC",
            mode="lines",
            line=dict(color="white", dash="dash"),
        )
    fig.update_layout(
        xaxis=dict(tickmode="array", tickvals=s_plug_in_out_count.index.mid)
    )
    return fig

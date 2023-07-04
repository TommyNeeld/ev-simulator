import plotly.figure_factory as ff


def distributions(
    hist_data: list,
    group_labels: list,
    metric: str,
    domain: tuple,
    show_hist: bool = True,
    show_curve: bool = False,
):
    """generic distribution plot - up to 6 distributions in one plot"""
    colors = [
        "#003f5c",
        "#444e86",
        "#955196",
        "#dd5182",
        "#ff6e54",
        "#ffa600",
    ]
    color_map = {label: colors.pop() for label in set(group_labels)}
    colors_mod = [color_map[label] for label in group_labels]
    fig = ff.create_distplot(
        hist_data,
        group_labels,
        bin_size=1,
        curve_type="normal",
        colors=colors_mod,
        show_hist=show_hist,
        show_curve=show_curve,
        show_rug=False,
    )
    fig.update_layout(
        title_text=f"Distribution of {metric}",
        xaxis_title_text=f"{metric}",
        yaxis_title_text="Density",
        template="plotly_dark",
        xaxis=dict(range=domain),
    )
    # avoid legend duplication
    names = set()
    fig.for_each_trace(
        lambda trace: trace.update(showlegend=False)
        if (trace.name in names)
        else names.add(trace.name)
    )

    return fig

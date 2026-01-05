from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd



df = pd.read_csv("../data/cleaned/locations.csv")

df.head()




df["step"] = range(len(df))       # Add step index for animation

app = Dash(__name__)

app.layout = html.Div([
    dcc.Slider(
        id="step-slider",
        min=0,
        max=len(df) - 1,
        step=1,
        value=0,
        marks=None
    ),
    dcc.Graph(id="map")
])

@app.callback(
    Output("map", "figure"),
    Input("step-slider", "value")
)
def update_map(step):
    dff = df.iloc[: step + 1]   # Show points up to the slider value

    fig = px.scatter_mapbox(
        dff,
        lat="lat",
        lon="lon",
        zoom=10,
    )

    fig.update_traces(mode="markers+lines")  # Ensure lines are connected

    fig.update_layout(
        mapbox_style="carto-positron",
        uirevision="keep",  # Keeps zoom level fixed
        margin=dict(r=0, t=0, l=0, b=0)
    )

    return fig

app.run(debug=True)

import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

# Read data from CSV
both_df = pd.read_csv("icedata.csv")
sea_level_df = pd.read_csv("sea_level.csv")
ice_ant_df = pd.read_csv("Antar_ice.csv")
ice_green_df = pd.read_csv("Greenland_ice.csv")

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Ice Sheet Melting and Sea Level Rise Dashboard"),
    dcc.Graph(id="ice-sheet-sea-level-rise-graph"),
    dcc.Dropdown(id="data-type",
                 options=[{"label": "Sea Level", "value": "sea"},
                          {"label": "Ice sheet", "value": "ice"},
                          {"label": "Both", "value": "both"}],
                 value="sea"),
    dcc.Dropdown(id="chart-type",
                 options=[{"label": "Bar Graph", "value": "bar"},
                          {"label": "Line Graph", "value": "line"},
                          {"label": "Scatter Plot", "value": "scatter"}],
                 value="bar"),
    dcc.Dropdown(id="glacier",
                 options=[{"label": "Antarctica", "value": "Antarctica"},
                          {"label": "Greenland", "value": "Greenland"}],
                 value="Antarctica")
])


# Define callback to update the graph
@app.callback(
    Output("ice-sheet-sea-level-rise-graph", "figure"),
    [Input("chart-type", "value"),
     Input("data-type", "value"),
     Input("glacier", "value")]
)
def update_graph(chart_type, data_type, glacier):
    global layout
    traces = []

    if data_type == "sea":
        df = sea_level_df
        if chart_type == "line":
            traces.append(go.Scatter(x=df["year"], y=df["sea_level"], mode="lines+markers",
                                     name="Sea Level Rise (Sea Level (µm * 10))"))
        elif chart_type == "bar":
            traces.append(go.Bar(x=df["year"], y=df["sea_level"],
                                 name="Sea Level Rise (Sea Level (µm * 10))"))
        else:
            traces.append(go.Scatter(x=df["year"], y=df["sea_level"], mode="markers",
                                     name="Sea Level Rise (Sea Level (µm * 10))"))
        layout = go.Layout(title=f"Sea Level Rise", xaxis={"title": "Year", "rangeselector": {"buttons": [
            {"count": 1, "label": "1Y", "step": "year", "stepmode": "backward"},
            {"count": 5, "label": "5Y", "step": "year", "stepmode": "backward"},
            {"count": 10, "label": "10Y", "step": "year", "stepmode": "backward"},
            {"step": "all"}]}},
                           yaxis={"title": "Sea Level (µm * 10)"})
        layout.update(xaxis_rangeslider_visible=True)

    elif data_type == "ice":
        if glacier == "Antarctica":
            df = ice_ant_df
        else:
            df = ice_green_df

        if chart_type == "line":
            traces.append(go.Scatter(x=df["Date"], y=df["Mass(Gigatonnes)"], mode="lines+markers",
                                     name="Ice Sheet Melting"))
        elif chart_type == "bar":
            traces.append(go.Bar(x=df["Date"], y=df["Mass(Gigatonnes)"],
                                 name="Ice Sheet Melting"))
        else:
            traces.append(go.Scatter(x=df["Date"], y=df["Mass(Gigatonnes)"], mode="markers",
                                     name="Ice Sheet Melting"))
        layout = go.Layout(title=f"Ice Sheet Melting ({glacier})", xaxis={"title": "Year", "rangeselector": {"buttons": [
            {"count": 1, "label": "1Y", "step": "year", "stepmode": "backward"},
            {"count": 5, "label": "5Y", "step": "year", "stepmode": "backward"},
            {"count": 10, "label": "10Y", "step": "year", "stepmode": "backward"},
            {"step": "all"}]}},
                           yaxis={"title": "Ice Sheet"})
        layout.update(xaxis_rangeslider_visible=True)
    else:
        df = both_df
        if chart_type == "bar":
            traces.append(go.Bar(x=df["year"], y=df[glacier], name=f"{glacier} Ice Sheet Melting (Gt)"))
            traces.append(go.Bar(x=df["year"], y=df["sea_level"], name="Sea Level Rise (Sea Level (µm * 10))"))

        elif chart_type == "line":
            traces.append(
                go.Scatter(x=df["year"], y=df[glacier], mode="lines+markers", name=f"{glacier} Ice Sheet Melting (Gt)"))
            traces.append(go.Scatter(x=df["year"], y=df["sea_level"], mode="lines+markers",
                                     name="Sea Level Rise (Sea Level (µm * 10))"))

        else:
            traces.append(
                go.Scatter(x=df["year"], y=df[glacier], mode="markers", name=f"{glacier} Ice Sheet Melting (Gt)"))
            traces.append(go.Scatter(x=df["year"], y=df["sea_level"], mode="markers",
                                     name="Sea Level Rise (Sea Level (µm * 10))"))

        layout = go.Layout(title=f"Ice Sheet Melting ({glacier}) and Sea Level Rise", xaxis={"title": "Year", "rangeselector": {"buttons": [
            {"count": 1, "label": "1Y", "step": "year", "stepmode": "backward"},
            {"count": 5, "label": "5Y", "step": "year", "stepmode": "backward"},
            {"count": 10, "label": "10Y", "step": "year", "stepmode": "backward"},
            {"step": "all"}]}},
                           yaxis={"title": "Sea Level (µm * 10)"})
        layout.update(xaxis_rangeslider_visible=True)

    # layout = go.Layout(title=f"Ice Sheet Melting ({glacier})", xaxis={"title": "Year"},
                       # yaxis={"title": "Values"})

    return {"data": traces, "layout": layout}


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

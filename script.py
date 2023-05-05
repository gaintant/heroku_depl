import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash import dash_table

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
                 value="Antarctica"),
    dcc.RangeSlider(id="year-slider",
                    min=both_df["year"].min(),
                    max=both_df["year"].max(),
                    value=[both_df["year"].min(), both_df["year"].max()],
                    marks={str(year): str(year) for year in both_df["year"].unique()}),
    html.Div(id="table-container"),
])


# Define callback to update the graph
@app.callback(
    Output("ice-sheet-sea-level-rise-graph", "figure"),
    [Input("chart-type", "value"),
     Input("data-type", "value"),
     Input("glacier", "value"),
     Input("year-slider", "value")]
)
def update_graph(chart_type, data_type, glacier, year_range):
    global layout
    # layout.update(xaxis_rangeslider_visible=True)

    layout = go.Layout(title=f"Ice Sheet Melting ({glacier})", xaxis={"title": "Year"},
                       yaxis={"title": "Values"})
    traces = []
    # Filter data based on the selected year range
    filtered_sea_level_df = sea_level_df[
        (sea_level_df["year"] >= year_range[0]) & (sea_level_df["year"] <= year_range[1])]
    filtered_ice_ant_df = ice_ant_df[(ice_ant_df["Date"] >= year_range[0]) & (ice_ant_df["Date"] <= year_range[1])]
    filtered_ice_green_df = ice_green_df[(ice_green_df["Date"] >= year_range[0]) & (ice_green_df["Date"] <= year_range[1])]
    if data_type == "sea":
        df = filtered_sea_level_df
        if chart_type == "line":
            traces.append(go.Scatter(x=df["year"], y=df["sea_level"], mode="lines+markers",
                                     name="Sea Level Rise (Sea Level (mm))"))
        elif chart_type == "bar":
            traces.append(go.Bar(x=df["year"], y=df["sea_level"],
                                 name="Sea Level Rise (Sea Level (mm))"))
        else:
            traces.append(go.Scatter(x=df["year"], y=df["sea_level"], mode="markers",
                                     name="Sea Level Rise (Sea Level (mm))"))
        layout = go.Layout(title=f"Sea Level Rise", xaxis={"title": "Year", "rangeselector": {"buttons": [
            {"count": 1, "label": "1Y", "step": "year", "stepmode": "backward"},
            {"count": 5, "label": "5Y", "step": "year", "stepmode": "backward"},
            {"count": 10, "label": "10Y", "step": "year", "stepmode": "backward"},
            {"step": "all"}]}},
                           yaxis={"title": "Sea Level (mm)"})
        layout.update(xaxis_rangeslider_visible=True)

    elif data_type == "ice":
        if glacier == "Antarctica":
            df = filtered_ice_ant_df
        else:
            df = filtered_ice_green_df

        if chart_type == "line":
            traces.append(go.Scatter(x=df["Date"], y=df["Mass(Gigatonnes)"], mode="lines+markers",
                                     name="Decrease in the Mass of Ice sheets(Gt)"))
        elif chart_type == "bar":
            traces.append(go.Bar(x=df["Date"], y=df["Mass(Gigatonnes)"],
                                 name="Decrease in the Mass of Ice sheets(Gt)"))
        else:
            traces.append(go.Scatter(x=df["Date"], y=df["Mass(Gigatonnes)"], mode="markers",
                                     name="Decrease in the Mass of Ice sheets(Gt)"))
        layout = go.Layout(title=f"Ice Sheet Melting ({glacier})",
                           xaxis={"title": "Year", "rangeselector": {"buttons": [
                               {"count": 1, "label": "1Y", "step": "year", "stepmode": "backward"},
                               {"count": 5, "label": "5Y", "step": "year", "stepmode": "backward"},
                               {"count": 10, "label": "10Y", "step": "year", "stepmode": "backward"},
                               {"step": "all"}]}},
                           yaxis={"title": "Decrease in Ice Sheet"})
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

        layout = go.Layout(title=f"Ice Sheet Melting ({glacier}) and Sea Level Rise",
                           xaxis={"title": "Year", "rangeselector": {"buttons": [
                               {"count": 1, "label": "1Y", "step": "year", "stepmode": "backward"},
                               {"count": 5, "label": "5Y", "step": "year", "stepmode": "backward"},
                               {"count": 10, "label": "10Y", "step": "year", "stepmode": "backward"},
                               {"step": "all"}]}},
                           yaxis={"title": "Sea Level (µm * 10)"})
        # layout.update(xaxis_rangeslider_visible=True)

    # layout = go.Layout(title=f"Ice Sheet Melting ({glacier})", xaxis={"title": "Year"},
    # yaxis={"title": "Values"})

    return {"data": traces, "layout": layout}


# Define callback to update the data table
@app.callback(
    Output("table-container", "children"),
    [Input("data-type", "value"),
     Input("glacier", "value"),
     Input("year-slider", "value")]
)
def update_table(data_type, glacier, year_range):
    if data_type == "sea":
        df = sea_level_df
        date_col = "year"
    elif data_type == "ice":
        df = ice_ant_df if glacier == "Antarctica" else ice_green_df
        date_col = "Date"
    else:
        df = both_df
        date_col = "year"

    # Filter data based on the selected year range
    filtered_df = df[(df[date_col] >= year_range[0]) & (df[date_col] <= year_range[1])]

    # Create the DataTable component
    return dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in filtered_df.columns],
        data=filtered_df.to_dict("records"),
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    )



# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


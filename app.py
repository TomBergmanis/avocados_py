# Importing necessary libraries
import pandas as pd
from dash import Dash, Input, Output, dcc, html

# Read the data from CSV and preprocess
data = (
    pd.read_csv("avocado.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)

# Extract unique regions and avocado types
regions = data["region"].sort_values().unique() 
avocado_types = data["type"].sort_values().unique()

# External stylesheets for the Dash app
external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Avocado Analytics: Understand Your Avocados!"

# Layout of the Dash app
app.layout = html.Div(
    children=[
        # Header section
        html.Div(
            children=[
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Avocado Analytics", className="header-title"
                ),
                html.P(
                    children=(
                        "Analyse the behavior of avocado prices and the number"
                        " of avocados sold in the US between 2015 and 2018"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        # Filters section
        html.Div(
            children=[
                # Region filter
                html.Div(
                    children=[
                        html.Div(children="Region", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in regions
                            ],
                            value="Albany",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                # Avocado type filter
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {
                                    "label": avocado_type.title(),
                                    "value": avocado_type,
                                }
                                for avocado_type in avocado_types
                            ],
                            value="organic",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                # Date range filter
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data["Date"].min().date(),
                            max_date_allowed=data["Date"].max().date(),
                            start_date=data["Date"].min().date(),
                            end_date=data["Date"].max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        # Charts section
        html.Div(
            children=[
                # Price chart
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                # Volume chart
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

# Callback to update charts based on filter inputs
@app.callback(
    Output("price-chart", "figure"),
    Output("volume-chart", "figure"),
    Input("region-filter", "value"),
    Input("type-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_charts(region, avocado_type, start_date, end_date):
    # Filter data based on inputs
    filtered_data = data.query(
        "region == @region and type == @avocado_type"
        " and Date >= @start_date and Date <= @end_date"
    )
    # Price chart figure
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AveragePrice"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    # Volume chart figure
    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Total Volume"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

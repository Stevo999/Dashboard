import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from dash_table import DataTable
import io
import base64

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of your dashboard
app.layout = html.Div([
    html.H1("Dashboard"),
    
    # Data upload component
    dcc.Upload(
        id='data-upload',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select a CSV File')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px auto'
        },
        multiple=False
    ),
    
    # Dropdown for chart type selection
    dcc.Dropdown(
        id='chart-type',
        options=[
            {'label': 'Bar Chart', 'value': 'bar'},
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Pie Chart', 'value': 'pie'},
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Area Chart', 'value': 'area'},
            {'label': 'Bubble Chart', 'value': 'bubble'},
            {'label': 'Heatmap', 'value': 'heatmap'}
        ],
        value='bar',
        clearable=False
    ),

    # Chart component
    dcc.Graph(id='chart'),

    # Data table component
    html.H2("Data Table"),
    DataTable(id='data-table')
])

# Define callback functions to handle data upload
@app.callback(
    Output('data-table', 'data'),
    Output('data-table', 'columns'),
    Input('data-upload', 'contents')
)
def update_table(uploaded_file):
    if uploaded_file is not None:
        content_type, content_string = uploaded_file.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        return df.to_dict('records'), [{"name": col, "id": col} for col in df.columns]
    else:
        return [], []

# Define callback functions to update the chart
@app.callback(
    Output('chart', 'figure'),
    Input('chart-type', 'value'),
    Input('data-table', 'data')
)
def update_chart(selected_chart_type, data):
    if not data:
        return {}

    df = pd.DataFrame(data)
    if selected_chart_type == 'bar':
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], title='Bar Chart')
    elif selected_chart_type == 'scatter':
        fig = px.scatter(df, x=df.columns[0], y=df.columns[1], title='Scatter Plot')
    elif selected_chart_type == 'pie':
        fig = px.pie(df, names=df.columns[0], values=df.columns[1], title='Pie Chart')
    elif selected_chart_type == 'line':
        fig = px.line(df, x=df.columns[0], y=df.columns[1], title='Line Chart')
    elif selected_chart_type == 'area':
        fig = px.area(df, x=df.columns[0], y=df.columns[1], title='Area Chart')
    elif selected_chart_type == 'bubble':
        fig = px.scatter(df, x=df.columns[0], y=df.columns[1], size=df.columns[1], title='Bubble Chart')
    elif selected_chart_type == 'heatmap':
        fig = px.imshow([[10, 15], [12, 7]], labels={'x': [df.columns[0], 'B'], 'y': ['C', 'D']}, title='Heatmap')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

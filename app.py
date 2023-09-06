from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout

app = Dash(external_stylesheets=[BOOTSTRAP])
server = app.server
app.title = "Medal dashboard"
app.layout = create_layout(app)
    

if __name__ == "__main__":
    app.run_server(debug=False)


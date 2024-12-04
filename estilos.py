import dash_bootstrap_components as dbc
from dash import html

# Cabeçalho estilizado
def criar_cabecalho():
    return dbc.Row(
        dbc.Col(
            html.H1(
                "Dashboard de Gestão de Medicações",
                className="text-center text-light",
                style={
                    "backgroundColor": "#007bff",
                    "padding": "20px",
                    "borderRadius": "10px",
                    "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.2)"
                }
            ),
            width=12
        ),
        className="mb-4"
    )

# Estilizar cartões
def criar_cartao(titulo, valor, cor):
    return dbc.Card(
        [
            dbc.CardHeader(titulo, className=f"text-center text-white bg-{cor}"),
            dbc.CardBody(
                html.H4(valor, className="text-center text-dark"),
                style={"padding": "20px"}
            )
        ],
        className="shadow-sm",
        style={"borderRadius": "10px", "overflow": "hidden"}
    )

# Estilizar fundo
def layout_com_fundo(layout):
    return html.Div(
        children=layout,
        style={
            "backgroundImage": "url('/assets/background.jpg')",  # Imagem no diretório assets
            "backgroundSize": "cover",
            "backgroundAttachment": "fixed",
            "padding": "20px",
            "minHeight": "100vh"
        }
    )

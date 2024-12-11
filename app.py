import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import mysql.connector
import dash_bootstrap_components as dbc
from datetime import datetime, date, timedelta
from estilos import criar_cabecalho, criar_cartao, layout_com_fundo

# Conexão com o banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="farmacia_publica"
    )

# Função para carregar dados gerais
def carregar_dados_gerais():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total_usuarios FROM usuarios")
    total_usuarios = cursor.fetchone()["total_usuarios"]

    cursor.execute("SELECT SUM(estoque) AS total_estoque FROM medicamentos")
    total_estoque = cursor.fetchone()["total_estoque"]

    cursor.execute("SELECT COUNT(*) AS total_entregas FROM entregas WHERE status = 'entregue'")
    total_entregas = cursor.fetchone()["total_entregas"]

    cursor.execute("SELECT COUNT(*) AS total_pendentes FROM entregas WHERE status = 'pendente'")
    total_pendentes = cursor.fetchone()["total_pendentes"]

    cursor.execute("""
        SELECT status, COUNT(*) AS quantidade
        FROM entregas
        GROUP BY status
    """)
    entregas_status = cursor.fetchall()

    # Carregar dados de medicamentos por estoque
    cursor.execute("""
        SELECT nome_medicamento, estoque AS quantidade_estoque, data_validade
        FROM medicamentos
    """)
    medicamentos_dados = cursor.fetchall()

    # Medicamentos com validade próxima (30 dias)
    hoje = datetime.now().date()  # Ajuste para .date() para obter apenas a data
    limite_validade = hoje + timedelta(days=30)

    # Verifique se 'data_validade' não é None ou NULL antes de comparar
    medicamentos_a_vencer = [
        med for med in medicamentos_dados 
        if med["data_validade"] and isinstance(med["data_validade"], (datetime, date)) and med["data_validade"] <= limite_validade
    ]
    # Carregar lista de locais de entrega
    cursor.execute("SELECT DISTINCT local_entrega FROM entregas")
    locais_entrega = [row["local_entrega"] for row in cursor.fetchall()]

    conexao.close()
    return (
        total_usuarios,
        total_estoque,
        total_entregas,
        total_pendentes,
        entregas_status,
        medicamentos_dados,
        medicamentos_a_vencer,
        locais_entrega
    )

# Função para carregar usuários
def carregar_usuarios():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, nome FROM usuarios")
    usuarios = cursor.fetchall()
    conexao.close()
    return usuarios

# Função para carregar dados de um usuário específico
def carregar_dados_usuario(id_usuario):
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    # Dados do usuário
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    usuario = cursor.fetchone()

    # Dados de entregas detalhadas
    cursor.execute("""
        SELECT 
            e.data_entrega,
            e.status,
            m.nome_medicamento,
            e.local_entrega
        FROM entregas e
        JOIN medicamentos m ON e.id_medicamento = m.id_medicamento
        WHERE e.id_usuario = %s
        ORDER BY e.data_entrega DESC
    """, (id_usuario,))
    entregas = cursor.fetchall()

    conexao.close()
    return usuario, entregas

# Dados gerais e usuários
usuarios = carregar_usuarios()
(
    total_usuarios, 
    total_estoque, 
    total_entregas, 
    total_pendentes, 
    entregas_status, 
    medicamentos_dados, 
    medicamentos_a_vencer, 
    locais_entrega
) = carregar_dados_gerais()

# App Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do Dashboard
app.layout = layout_com_fundo(
    dbc.Container(
        fluid=True,
        children=[
            # Cabeçalho estilizado
            criar_cabecalho(),

            # Seletor de Usuários
            dbc.Row(
                dbc.Col(
                    html.Div([
                        html.Label("Selecione um usuário:", className="text-light"),
                        dcc.Dropdown(
                            id="usuario-dropdown",
                            options=[{"label": u["nome"], "value": u["id_usuario"]} for u in usuarios],
                            placeholder="Selecione um usuário",
                            className="mb-4",
                        ),
                    ]),
                    width=6,
                    className="offset-3"
                )
            ),

            # Indicadores Gerais
            dbc.Row([
                dbc.Col(criar_cartao("Total de Usuários", total_usuarios, "primary"), width=3),
                dbc.Col(criar_cartao("Medicamentos em Estoque", total_estoque, "success"), width=3),
                dbc.Col(criar_cartao("Entregas Realizadas", total_entregas, "warning"), width=3),
                dbc.Col(criar_cartao("Entregas Pendentes", total_pendentes, "danger"), width=3),
            ], className="mb-4"),

            # Gráficos
            dbc.Row([
                # Gráfico de status geral
                dbc.Col(dcc.Graph(
                    id="grafico-status-geral",
                    figure=px.pie(
                        pd.DataFrame(entregas_status),
                        names="status",
                        values="quantidade",
                        title="Status de Entregas",
                        color="status",
                        color_discrete_map={
                            "entregue": "#636efa",  # Azul para entregues
                            "pendente": "#ef553b"  # Vermelho para pendentes

                        }
                    )
                ), width=4),

                # Gráfico de entregas por local
                dbc.Col(dbc.Card([
                    dbc.CardHeader(
                        dcc.Dropdown(
                            id="local-dropdown",
                            options=[{"label": local, "value": local} for local in locais_entrega],
                            placeholder="Selecione um local de entrega",
                            className="mb-2"
                        )
                    ),
                    dbc.CardBody(dcc.Graph(id="grafico-local-entregas", style={"height": "340px"}))
                ], className="shadow-sm"), width=4),

                # Gráfico de estoque por medicação
                dbc.Col(dcc.Graph(
                    id="grafico-estoque",
                    figure=px.bar(
                        pd.DataFrame(medicamentos_dados),
                        x="nome_medicamento",
                        y="quantidade_estoque",
                        color=pd.DataFrame(medicamentos_dados)["nome_medicamento"].isin(
                            [med["nome_medicamento"] for med in medicamentos_a_vencer]
                        ).map({True: "Próximo do Vencimento", False: "OK"}),
                        title="Estoque de Medicamentos (Com Validade Próxima)",
                        labels={"quantidade_estoque": "Quantidade em Estoque"}
                    )
                ), width=4),
            ]),

            # Lista de medicamentos prestes a vencer
            dbc.Row([
                dbc.Col(html.Div([
                    html.H5("Medicamentos Prestes a Vencer", className="text-center"),
                    html.Ul([
                        html.Li(f"{med['nome_medicamento']} - Validade: {med['data_validade']}")
                        for med in medicamentos_a_vencer
                    ])
                ], className="p-3 bg-light border rounded shadow-sm"), width=12),
            ]),

            # Seção de informações do usuário
            dbc.Row([
                dbc.Col(html.Div(id="informacoes-usuario"), width=6),
                dbc.Col(html.Div(id="tabela-entregas"), width=6),
            ], className="mt-4")
        ]
    )
)

# Callback para atualizar o gráfico de entregas por local
@app.callback(
    Output("grafico-local-entregas", "figure"),
    [Input("local-dropdown", "value")]
)
def atualizar_grafico_central(local_selecionado):
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    if local_selecionado:
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN status = 'entregue' THEN 1 ELSE 0 END) AS entregues,
                SUM(CASE WHEN status = 'pendente' THEN 1 ELSE 0 END) AS pendentes
            FROM entregas
            WHERE local_entrega = %s
        """, (local_selecionado,))
        dados_local = cursor.fetchone()
    else:
        dados_local = {"entregues": 0, "pendentes": 0}

    conexao.close()

    df_local = pd.DataFrame([
        {"Status": "Entregues", "Quantidade": dados_local["entregues"]},
        {"Status": "Pendentes", "Quantidade": dados_local["pendentes"]}
    ])

    cores_personalizadas ={
        "Entregues": "#636efa",
        "Pendentes": "#ef553b"
    }

    fig = px.bar(
        df_local,
        x="Status",
        y="Quantidade",
        title=f"Entregas no Local: {local_selecionado}" if local_selecionado else "Selecione um local de entrega",
        labels={"Quantidade": "Quantidade"},
        color="Status",
        color_discrete_map=cores_personalizadas
    )
    return fig

# Callback para exibir informações do usuário
@app.callback(
    [Output("informacoes-usuario", "children"),
     Output("tabela-entregas", "children")],
    [Input("usuario-dropdown", "value")]
)
def exibir_informacoes_usuario(id_usuario):
    if not id_usuario:
        return "", ""

    usuario, entregas = carregar_dados_usuario(id_usuario)

    info_usuario = dbc.Card(
        children=[
            dbc.CardHeader(html.H5("Informações do Usuário", className="text-center")),
            dbc.CardBody([
                html.P(f"Nome: {usuario['nome']}", className="mb-2"),
                html.P(f"E-mail: {usuario['email']}", className="mb-2"),
                html.P(f"Telefone: {usuario['telefone']}", className="mb-2"),
            ]),
        ],
        className="shadow-lg mt-4"
    )

    tabela_entregas = dbc.Table(
        children=[
            html.Thead(html.Tr([
                html.Th("Medicamento"),
                html.Th("Data de Entrega"),
                html.Th("Status"),
                html.Th("Local de Entrega")
            ])),
            html.Tbody([
                html.Tr([
                    html.Td(entrega["nome_medicamento"]),
                    html.Td(entrega["data_entrega"]),
                    html.Td(entrega["status"]),
                    html.Td(entrega["local_entrega"])
                ]) for entrega in entregas
            ])
        ],
        bordered=True,
        striped=True,
        hover=True,
        className="mt-4"
    )

    return info_usuario, tabela_entregas

if __name__ == "__main__":
    app.run_server(debug=True)

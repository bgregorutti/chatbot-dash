import time

from dash import html, dcc, Input, Output, State, Dash
import dash_bootstrap_components as dbc

# import openai

def Header(name):
    return  html.H1(name, style={"margin-top": 5})


def textbox(text, box):
    style = {
        "max-width": "60%",
        "width": "max-content",
        "height": "max-content",
        # "padding": "5px 10px",
        "border-radius": 20,
        "margin-bottom": 20
    }

    if box == "user":
        style["margin-left"] = "auto"
        style["margin-right"] = 0

        thumbnail = html.Img(
            src=app.get_asset_url("user_icon.png"),
            style={
                "border-radius": 50,
                "height": 36,
                "margin-right": 5,
                "float": "right",
            },
        )

        textbox = dbc.Card(text, style=style, body=True, color="primary", inverse=True)
        return html.Div([thumbnail, textbox])

    elif box == "bot":
        style["margin-left"] = 0
        style["margin-right"] = "auto"

        thumbnail = html.Img(
            src=app.get_asset_url("ai_icon.png"),
            style={
                "border-radius": 50,
                "height": 36,
                "margin-right": 5,
                "float": "left"
            },
        )
        textbox = dbc.Card(text, style=style, body=True, color="light", inverse=False)
        return html.Div([thumbnail, textbox])

    else:
        raise ValueError("Incorrect option for `box`.")

# Authentication
# openai.api_key = os.getenv("OPENAI_KEY")

# Define app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# Load images
IMAGES = {"user": app.get_asset_url("user_icon.png")}


# Define Layout
conversation = html.Div(
    html.Div(
        [
            html.Div(id="display-conversation"),
            dbc.Spinner(html.Div(id="loading-component")),
            html.Br()
        ]
    ),
    style={
        "overflow-y": "auto",
        "display": "flex",
        "height": "calc(90vh - 132px)",
        "flex-direction": "column-reverse"
    }
)

controls = dbc.InputGroup(
    children=[
        dbc.Input(id="user-input", placeholder="Ask me a question...", type="text"),
        dbc.Button("Submit", id="submit")
    ]
)

app.layout = dbc.Container(
    fluid=False,
    children=[
        Header("Chatbot template with Dash"),
        html.Hr(),
        dcc.Store(id="store-conversation", data=[]),
        conversation,
        controls
    ],
)


@app.callback(
    Output("display-conversation", "children"), [Input("store-conversation", "data")]
)
def update_display(chat_history):
    return [textbox(item.get("content"), box=item.get("type")) for item in chat_history]


@app.callback(
    Output("user-input", "value"),
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
)
def clear_input(n_clicks, n_submit):
    return ""


@app.callback(
    [Output("store-conversation", "data", allow_duplicate=True), Output("loading-component", "children", allow_duplicate=True)],
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    [State("user-input", "value"), State("store-conversation", "data")],
    prevent_initial_call=True
)
def run_chatbot(n_clicks, n_submit, user_input, chat_history):
    if n_clicks == 0 and n_submit is None:
        return "", None

    if user_input is None or user_input == "":
        return chat_history, None

    # First add the user input to the chat history
    chat_history.append({"type": "user", "content": user_input})

    return chat_history, None

@app.callback(
    [Output("store-conversation", "data", allow_duplicate=True), Output("loading-component", "children", allow_duplicate=True)],
    [Input("store-conversation", "data")],
    prevent_initial_call=True
)
def chat_core(chat_history):
    if not chat_history:
        return chat_history, None

    # Call the LLM here
    # model_input = prompt + chat_history.replace("<split>", "\n")

    # response = openai.Completion.create(
    #     engine="davinci",
    #     prompt=model_input,
    #     max_tokens=250,
    #     stop=["You:"],
    #     temperature=0.9,
    # )
    # model_output = response.choices[0].text.strip()

    time.sleep(1)
    content = chat_history[-1].get("content")
    model_output = f"I heard: {content}"
    chat_history.append({"type": "bot", "content": model_output})

    return chat_history, None

if __name__ == "__main__":
    app.run_server(debug=True)

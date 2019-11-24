import run
import re
from slackclient import SlackClient
import time

starterbot_id = None
slack_client = SlackClient(
    'xoxb-556741523728-819299593268-E1GAxMnv9Jntbc9oZ5z5yJCe')


RTM_READ_DELAY = 1
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events):

    for event in slack_events:
        if event["type"] == "message" and "subtype" not in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)

    return (matches.group(1), matches.group(2).strip()) if matches else \
        (None, None)


def handle_command(command, channel):

    default_response = "Not sure what you mean. Try *{}*.".format(
        EXAMPLE_COMMAND)

    response = None
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    elif command.startswith("approve"):
        # muda Status
        id = re.sub("[^0-9]", "", command)
        id_n = int(id)

        run.models.PedidoModel.atualizaAprovacao(id_n)
        response = "Pedido" + id_n + " foi APROVADO!"
    elif command.startswith("adicionarcurso"):
        curso = command.partition(":")[2]
        try:
            run.models.CursoModel(curso=curso).save_to_db()
            response = "Curso " + curso + " adicionado"
        except Exception as e:
            response = "Erro ao adicionar curso" + e
    elif command.startswith("excluircurso"):
        curso = command.partition(":")[2]
        try:
            run.models.CursoModel.delete_by_nome(curso)
            response = "Curso " + curso + " excluido"
        except Exception as e:
            response = "Erro ao excluir curso" + e
    elif command.startswith("adicionarsolicitacao"):
        solicitacao = command.partition(":")[2]
        try:
            run.models.SolicitacaoModel(solicitacao=solicitacao).save_to_db()
            response = "Solicitação " + solicitacao + " adicionado"
        except Exception as e:
            response = "Erro ao adicionar curso" + e
    elif command.startswith("excluirsolicitacao"):
        solicitacao = command.partition(":")[2]
        try:
            run.models.SolicitacaoModel.delete_by_nome(solicitacao)
            response = "Solicitacao " + solicitacao + " excluida"
        except Exception as e:
            response = "Erro ao excluir curso" + e
    elif command.startswith("adicionarsala"):
        sala = command.partition(":")[2]
        try:
            run.models.SalaModel(sala=sala).save_to_db()
            response = "Sala " + sala + " adicionada"
        except Exception as e:
            response = "Erro ao adicionar sala" + e
    elif command.startswith("excluirsala"):
        sala = command.partition(":")[2]
        try:
            run.models.SalaModel.delete_by_nome(sala)
            response = "Sala " + sala + " excluida"
        except Exception as e:
            response = "Erro ao excluir curso" + e
    elif command.startswith("adicionarsolicitante"):
        solicitante = command.partition(":")[2]
        try:
            run.models.SolicitanteModel(solicitante=solicitante).save_to_db()
            response = "Solicitante " + solicitante + " adicionado"
        except Exception as e:
            response = "Erro ao adicionar solicitante" + e
    elif command.startswith("excluirsolicitante"):
        solicitante = command.partition(":")[2]
        try:
            run.models.SolicitanteModel.delete_by_nome(solicitante)
            response = "Solicitante " + solicitante + " excluido"
        except Exception as e:
            response = "Erro ao excluir solicitante" + e

    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


def send_alert(id):
    pedido = run.models.PedidoModel.return_by_id(id)
    pessoa = run.models.PessoaModel.return_by_id(
        pedido['Pedidos'][0]['id_pessoa'])
    solicitacao = run.models.SolicitacaoModel.return_by_id(
        pedido['Pedidos'][0]['id_solicitacao'])
    sala = run.models.SalaModel.return_by_id(pedido['Pedidos'][0]['id_sala'])
    slack_client.api_call(
        "chat.postMessage",
        channel="CQE3N774M",
        text="Temos uma nova solicitação!",
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Temos uma nova solicitação!*"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Nome:*\n" + str(pessoa['Pessoa'][0]['nome'])
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*E-mail:*\n" + str(
                            pessoa['Pessoa'][0]['email'])
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Tipo de Solicitação:*\n" + str(
                            solicitacao['Solicitacao'][0]['solicitacao'])
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Data:*\n" + str(pedido['Pedidos'][0]['data'])
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Sala:*\n" + str(sala['Sala'][0]['sala'])
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Duração:*\n" + str(
                            pedido['Pedidos'][0]['duracao']) + " horas"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Quantidade de pessoas:*\n" + str(
                            pedido['Pedidos'][0]['qtd_pessoas'])
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Aprovar"
                        },
                        "style": "primary",
                        "value": "click_me_123"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Recusar"
                        },
                        "style": "danger",
                        "value": "click_me_123"
                    }
                ]
            }
        ],
        respose_url="http://localhost:5000/SlackResponse"
    )



if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed")

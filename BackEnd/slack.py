# import os
import run
import re
from slackclient import SlackClient
import time

# slack_client = SlackClient(os.environ.get('SLACK_BOT_FB'))
starterbot_id = None
slack_client = \
        SlackClient('xoxb-556741523728-819299593268-4CDx66f4JGrHhNZqwCouYofH')


RTM_READ_DELAY = 1
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events):

    # Parses a list of events coming from the Slack RTM API to find
    # bot commands.
    # If a bot command is found, this function returns a
    # tuple of command and channel.
    # If its not found, then this function returns None, None.

    for event in slack_events:
        if event["type"] == "message" and "subtype" not in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):

    # Finds a direct mention (a mention that is at the beginning)
    # in message text and returns the user ID which was mentioned.
    # If there is no direct mention, returns None

    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains
    # the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else \
        (None, None)


def handle_command(command, channel):

    # Executes bot command if the command is known
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(
        EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    elif command.startswith("approve"):
        #muda Status
        id = re.sub("[^0-9]", "", command)
        id_n = int(id)
        run.models.PedidoModel.atualizaAprovacao(id_n)
        response = "APROVADO!"
	# elif command.startswith("adicionarcurso"):
	# 	# status = re.sub("[^0-9]", "", command)
	# 	curso = "cursoteste"
	#  	try:
	#  		run.models.CursoModel(curso=curso).save_to_db()
	#  		response = "Curso " + curso + " adicionado"
	#  	except:
	#  		response = "Erro ao adicionar curso"
    #  Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


def send_alert(id):
	pedido = run.models.PedidoModel.return_by_id(id)
	pessoa = run.models.PessoaModel.return_by_id(pedido['Pedidos'][0]['id_pessoa'])
	solicitacao = run.models.SolicitacaoModel.return_by_id(pedido['Pedidos'][0]['id_solicitacao'])
	sala = run.models.SalaModel.return_by_id(pedido['Pedidos'][0]['id_sala'])
	slack_client.api_call(
        "chat.postMessage",
        channel="CQE3N774M",
        blocks=[
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Temos uma nova solicitação!"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "Nome: " + str(pessoa['Pessoa'][0]['nome'])
				},
				{
					"type": "mrkdwn",
					"text": "E-mail: " + str(pessoa['Pessoa'][0]['email'])
				},
				{
					"type": "mrkdwn",
					"text": "Tipo de Solicitação: "+ str(solicitacao['Solicitacao'][0]['solicitacao'])
				},
				{
					"type": "mrkdwn",
					"text": "Data: "  + str(pedido['Pedidos'][0]['data'])
				},
				{
					"type": "mrkdwn",
					"text": "Sala: " + str(sala['Sala'][0]['sala'])
				},
                {
					"type": "mrkdwn",
					"text": "Duração:" + str(pedido['Pedidos'][0]['duracao']) + "horas"
				},
                {
					"type": "mrkdwn",
					"text": "Quantidade de pessoas: " + str(pedido['Pedidos'][0]['qtd_pessoas'])
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
	]
    )
	# oi = slack_client.api_call("channel.info", channel="CQE3N774M")
	# print(oi)


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

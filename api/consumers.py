from channels import Group


def ws_connect(message):
    Group('all-users').add(message.reply_channel)
    message.reply_channel.send({
        'accept': True,
    })
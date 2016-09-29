import tvshow_parser
from notification import *
from slacker import Slacker


class Slack(Notification):
    colors = {
        'Error': 'danger',
        'Parsing done': 'good'
    }

    def __init__(self, config):
        Notification.__init__(self, config)
        self.slack = Slacker('', incoming_webhook_url=config['slack']['webhook'])

    def sendNotification(self, type="Parsing done", title="Parsing done", description="", image=""):
        data = {'text': description}
        if type in self.colors:
            data['attachments'] = [{'text': title, 'color': self.colors[type], 'thumb_url': image}]
        print data
        self.slack.incomingwebhook.post(data)




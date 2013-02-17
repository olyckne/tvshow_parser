import gntp.notifier
import tvshow_parser
from notification import *


class Growl(Notification, gntp.notifier.GrowlNotifier):

    def __init__(self, config):
        Notification.__init__(self, config)
        gntp.notifier.GrowlNotifier.__init__(self,
             applicationName = tvshow_parser.__app_name__,
             notifications = ["Parsing done"],
             defaultNotifications = ["Parsing done"],
            )
        self.register()

    def sendNotification(self, type="Parsing done", title="Parsing done", description=""):
        self.notify(
            noteType="Parsing done",
            title=title,
            description=description,
            sticky=False,
            priority=2
            )

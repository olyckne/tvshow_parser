import gntp.notifier
from notification import *


class Growl(Notification, gntp.notifier.GrowlNotifier):

    def __init__(self, config):
        Notification.__init__(self, config)

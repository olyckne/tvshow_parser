import yaml

class Config():

    def __init__(self):
        self.config = {
            "actions": {
                "metadata": True,
                "convert": True,
                "sub": True
            }
        }

    def loadFromFile(self, file):
        self.file = file
        try:
            f = open(file)
            configFromFile = yaml.load(f)
            f.close()
        except IOError:
            print "Couldn't find a config file."
            return False
        configFromFile.update(self.config)
        self.config = configFromFile

        print self.config

        return True

    def saveToFile(self, file=None):
        file = file if file else self.file
        print file
        try:
            f = open(file, 'w+')
            f.write(yaml.dump(self.config))
            f.close()
        except IOError, e:
            print "Couldn't save config file"
            return False

        return True

    def set(self, key, value):
        self.config[key] = value

    def get(self, key, default=None):
        return self.config[key]

    def __contains__(self, key):
        return key.lower() in map(str.lower, self.config)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.set(key, value)

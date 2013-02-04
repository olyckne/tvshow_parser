import sys
import yaml


def loadConfig(file):
    try:
        f = open(file)
        config = yaml.load(f)
        f.close()
    except IOError:
        return False

    return config


def main(argv):
    configFile = "config.yaml"
    config = loadConfig(configFile)

    if not config:
        print "Couldn't read config file " + str(configFile)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])

import sys
import getopt
import yaml

shortArgs = {
    "h": "help",
    "c:": "config file",
    "d:": "debug level",
}

longArgs = {
    "type": "type of media - TV/Movie - Default: TV",
    "temp-dir": "temp directory to use - Default: ./temp",
    "meta-module": "metadata module to use - Default trakt",
    "add-module": "add module to use - Default: itunes",
    "sub-module": "subtitle module to use - Default: subliminal",
    "sub": "subtitle file to use - Default srt/sub with same filename as input",
    "notification-module": "notification module to use - Default: prowl",
    "season": "Set season # - Default: Parse from filename",
    "episode": "Set episode # - Default: Parse from filename",
    "name": "Set name - Default: Parse from filename",
    "year": "Set year - Default: Parse from filename"
}


def loadConfig(file):
    try:
        f = open(file)
        config = yaml.load(f)
        f.close()
    except IOError:
        return False

    return config


def usage():
    print "tvshow-parser"

    for arg in shortArgs:
        print "{0:25} {1:15s}".format("-" + arg.replace(":", ""), shortArgs[arg])

    for arg in longArgs:
        print "{0:25} {1:15s}".format("--" + arg, longArgs[arg])


def main(argv):
    configFile = "config.yaml"
    try:
        opts, args = getopt.getopt(argv, str(shortArgs.keys()), longArgs.keys())
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == "-c":
            configFile = arg

    filename = "".join(args)

    config = loadConfig(configFile)

    if not config:
        print "Couldn't read config file " + str(configFile)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])

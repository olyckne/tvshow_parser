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
    "temp-dir=": "temp directory to use - Default: ./temp",
    "meta-module=": "metadata module to use - Default trakt",
    "add-module=": "add module to use - Default: itunes",
    "sub-module=": "subtitle module to use - Default: subliminal",
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


def parseArgs(argv, config):
    try:
        opts, args = getopt.getopt(argv, str(shortArgs.keys()), longArgs.keys())
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    try:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt == "-c":
                config = loadConfig(arg)
                if not config:
                    print "Couldn't read config file " + str(arg)
                    sys.exit(2)
            elif opt == "--type":
                config['type'] = arg
            elif opt == "--temp-dir":
                config['temp']["path"] = arg
            elif opt == "--meta-module":
                config['modules']["metadata"] = arg
            elif opt == "--add-module":
                config['modules']["addTo"] = arg
    except:
        print "something wrong with config..."
        sys.exit(2)

    config['filename'] = "".join(args)

    return config


def main(argv):
    configFile = "config.yaml"

    config = loadConfig(configFile)

    parseArgs(argv, config)

    print config

if __name__ == "__main__":
    main(sys.argv[1:])

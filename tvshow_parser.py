#! /usr/bin/env python

import sys
import getopt
import yaml
import os
import signal
from modules import config, file, serie, movie
import traceback, os.path

__app_name__ = "tvshow_parser"
__version__ = 0.5

shortArgs = {
    "h:": "help",
    "c:": "config file",
    "d:": "debug level",
}
longArgs = {
    "type=": "type of media - TV/Movie - Default: TV",
    "meta-module=": "metadata module to use - Default trakt",
    "add-module=": "add module to use - Default: itunes",
    "sub-module=": "subtitle module to use - Default: subliminal",
    "sub=": "subtitle file to use - Default srt/sub with same filename as input",
    "notification-module=": "notification module to use - Default: growl",
    "season=": "Set season # - Default: Parse from filename",
    "episode=": "Set episode # - Default: Parse from filename",
    "name=": "Set name - Default: Parse from filename",
    "hd=": "Set HD quality: True/False - Default: Parse from filename",
    "filename=": "Use this string for parsing info instead of actual filename",
    "no-sub": "Don't add subtitle",
    "no-convert": "Don't convert",
    "no-metadata": "Don't add metadata"
}

file_handler = {}

def parseArgs(argv, config):
    try:
        opts, args = getopt.getopt(argv, str(shortArgs.keys()), longArgs.keys())
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    config['file'] = {'metadata': {}}

    print config.config

    try:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt == "-c":
                config["config_file"] = arg
            elif opt == "--type":
                config['type'] = arg.upper()
            elif opt == "--meta-module":
                config['modules']["metadata"] = arg
            elif opt == "--add-module":
                config['modules']["addTo"] = arg
            elif opt == "--sub-module":
                config['modules']['subtitle'] = arg
            elif opt == "--sub":
                config['sub'] = arg
            elif opt == "sendNotification":
                config['modules']['notification'] = arg
            elif opt == "--season":
                config['file']['metadata']['season'] = arg
            elif opt == "--episode":
                config['file']['metadata']['episode'] = arg
            elif opt == "--name":
                config['file']['metadata']['name'] = arg
            elif opt == "--hd":
                config['file']['metadata']['hd'] = arg
            elif opt == "--filename":
                config['file']['metadata']['filename'] = arg
            elif opt == "--no-sub":
                config['actions']['sub'] = False
            elif opt == "--no-convert":
                config['actions']['convert'] = False
            elif opt == "--no-metadata":
                config['actions']['metadata'] = False

    except Exception as e:
        print e
        print "something wrong with config..."
        sys.exit(2)

    theFile = "".join(args)
    config['file']['path'] = os.path.dirname(theFile)
    config['file']['name'] = os.path.basename(theFile)

    if config['file']['path'] == '.' or config['file']['path'] == '':
        config['file']['path'] = os.getcwd()

    if not theFile:
        print "No input..."
        sys.exit(2)

    return config
    
def usage():
    print "tvshow-parser"

    for arg in shortArgs:
        print "{0:25} {1:15s}".format("-" + arg.replace(":", ""), shortArgs[arg])

    for arg in longArgs:
        print "{0:25} {1:15s}".format("--" + arg, longArgs[arg])


def loadModules(config):
    res = {}
    for module in config['modules']:
        path = module.replace("_", ".")
        # If we dont want to add metadata, dont initalize those modules
        # mainly because that will authenticate with trakt
        # and 99% of the time I use --no-metadata it's because Trakt is down
        # and that means the script will fail and exit
        if path == "metadata.fetch" and not config["actions"]["metadata"]:
            continue
        if path == "subtitle" and not config["actions"]["sub"]:
            continue
        try:
            exec("from modules." + path + " import " + config['modules'][module])
            m = sys.modules['modules.' + path + '.' + config['modules'][module]]
            res[module] = getattr(m, config['modules'][module].capitalize())(config)
        except Exception as e:
            print e
	    sys.exit(1)

    return res

def cleanup(signum, frame):
    print "Cleaning up..."
    file_handler.removeTemp()
    sys.exit(0)

def convert(config, modules):
    global file_handler
    # setup signal
    signal.signal(signal.SIGINT, cleanup)

    # init file_handler
    file_handler = file.File(config)

    print config['file']


    # If file isn't a video, try to find one (or more)
    if not os.path.isfile(os.path.join(config['file']['path'], config['file']['name'])):
        print "Not a file? Exiting..."
        sys.exit(1)

    if not file_handler.isVideo(config['file']['name']):
        files = file_handler.findVideo()
        for f in files['files']:
            config['file']['path'] = files['path']
            config['file']['name'] = os.path.basename(f)
            # Call convert again with new file
            convert(config, modules)
    else:
        # Okay, we have a file

        # Init media_handler for the type
        if config['type'] == "TV":
            media_handler = serie.Serie(config)
        elif config['type'] == "MOVIE":
            media_handler = movie.Movie(config)
            print "Not implemented yet!"
            sys.exit(1)

        # LETS GO!
        filename = config['file']['name']
        if "metadata" in config['file'] and "filename" in config['file']['metadata']:
            filename = config['file']['metadata']['filename']

        media_handler.parse(filename)

        # Move file to temp folder to work with
        file_handler.moveToTemp()
        file_handler.cdToTemp()

        artworkLink = ""
        if config['actions']['metadata']:
            try:
                metadata = modules['metadata_fetch'].getInfo({
                                                   "name": media_handler.name,
                                                   "season": media_handler.season,
                                                   "episode": media_handler.episode,
                                                   "hd": media_handler.hd
                                                   })
                print metadata
                modules['metadata_fetch'].getArtwork(media_handler.name, media_handler.season)
                artworkLink = modules['metadata_fetch'].getArtworkLink(media_handler.name, media_handler.season)
            except Exception, e:
                print "Couldn't fetch metadata... exiting..."
                file_handler.removeTemp()
                modules['notification'].sendNotification(type="Error", title="Error: Couldn't fetch metadata: " + str(e), description=config['file']['name'])
                sys.exit(1)
        if config['actions']['sub']:
            try:
                modules['subtitle'].getSubtitle()
            except:
                print "Something wrong with fetching subtitle."

        if config['actions']['convert']:
            try:
                modules['convert'].convert()
            except Exception, e:
                print "Oh Oh. Something wrong!"
                file_handler.removeTemp()
                e = sys.exc_info()[0]
                modules['notification'].sendNotification(type="Error", title="Error: " + str(e), description=config['file']['name'])
                sys.exit(1)

        if config['actions']['metadata']:
            try:
                modules['metadata_add'].addMetadata(metadata)
            except Exception, e:
                print "Couldn't add metdata. Exiting..."
                file_handler.removeTemp()
                modules['notification'].sendNotification(type="Error", title="Error: Couldn't add metadata: " + str(e), description=config['file']['name'])
                sys.exit(1)
        # convert()
        # addTags()
        # optimize()
        try :
            if modules['add'].add(os.path.join(config['temp']['path'], config['temp']['name'])):
                file_handler.removeTemp()
                modules['notification'].sendNotification(description=config['file']['name'], image=artworkLink)
        except Exception, e:
            file_handler.removeTemp()
            modules['notification'].sendNotification(type="Error", title="Error: " + str(e), description=config['file']['name'], image=artworkLink)
            sys.exit(1)


def main(argv):
    settings = config.Config()

    # Parse arguments
    settings = parseArgs(argv[1:], settings)

    # Load config file
    root = os.path.dirname(os.path.realpath(__file__))
    configFile = os.path.join(root, settings["config_file"] if "config_file" in settings else "config.yaml")
    settings['config_file'] = configFile
    if not settings.loadFromFile(configFile):
        sys.exit(0)
        cleanup();

    settings['root'] = root
    settings['config_root'] = os.path.dirname(os.path.realpath(settings['config_file']))

    print(settings.config)

    # Load modules for metadata, addTo and subtitle
    modules = loadModules(settings)

    convert(settings, modules)

if __name__ == "__main__":
    main(sys.argv)

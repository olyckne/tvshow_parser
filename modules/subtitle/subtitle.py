import subliminal
import os
import shutil
from babelfish import Language


class Subtitle(object):

    def __init__(self, config):
        self.config = config

    def getSubtitle(self):
        if not "sub" in self.config or not os.path.isfile(self.config['sub']):
            self.config['sub'] = {}
            name = os.path.splitext(self.config['file']['name'])[0]
            file = os.path.join(self.config['file']['path'], name + ".srt")
            if os.path.isfile(file):
                print "found file. copying to temp"
                shutil.copy(file, self.config['temp']['path'])
                self.config['sub']['file'] = os.path.join(self.config['temp']['path'], name + ".srt")
                self.config['sub']['lang'] = self.config['language']['subtitle'][0]
            else:
                print "trying to download subtitle"
                file = self.config['file']['name']
                lang = self.config['language']['subtitle']
                languages = set();
                for l in lang:
                    languages.add(Language(l))
                print languages
                videoPath = os.path.join(self.config['temp']['path'], file)
                video = set([subliminal.scan_video(videoPath)])
                print video
                cache = self.config['temp']['path'] if "temp" in self.config else self.config['file']['path']
                sub = subliminal.download_best_subtitles(video, languages)
                print sub.items()
                if not sub.items():
                    self.config['sub'] = False
                for item in sub.items():
                    subLang = item[1][0].language.alpha3
                    self.config['sub'][subLang] = {}
                    self.config['sub'][subLang]['lang'] = subLang
                    self.config['sub'][subLang]['file'] = subliminal.subtitle.get_subtitle_path(videoPath, Language(subLang))
                
                print self.config['sub']
        return self.config['sub']

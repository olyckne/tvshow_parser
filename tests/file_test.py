from modules import file

class TestFile():
    
    def testIsVideo(self):
        "It checks if extension seems like a video"
        
        handler = file.File({})

        assert handler.isVideo('TV.Show.mkv') == True

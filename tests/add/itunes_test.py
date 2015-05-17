from modules.add import itunes

class TestItunes():


    def test(self):
        iTunes = itunes.Itunes

        #iTunes.add()

    def testShouldAddDirect(self):
        config = {
            'itunes': {
                'addDirect': True
            }
        }

        config2 = {
            'itunes': {
                'addDirect': False
            }
        }

        iTunes = itunes.Itunes(config)

        iTunes2 = itunes.Itunes(config2)

        assert iTunes.shouldAddDirect() == True
        assert iTunes2.shouldAddDirect() == False

    def testGetDirectCmd(self):
        iTunes = itunes.Itunes({})

        cmd = '/usr/bin/osascript -e "tell application \\"iTunes\\" to add POSIX file \\"TV.Show.S01E01.mkv\\""'

        assert iTunes.getDirectCmd('TV.Show.S01E01.mkv') == cmd

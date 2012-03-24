__author__ = 'Mario'

import unittest
import core

class HandyTestCase(unittest.TestCase):
    def setUp(self):

        self.test_in_file = 'C:\Users\Mario\Downloads\Gossip Girl Season 1\gossip.girl.s01e10.avi'
        self.test_out_file = 'Z:\Video\TV\Gossip Girl\Gossip.girl.s01e10-1.m4v'
        self.test_enc_options = '--preset "AppleTV 2"'

        self.test_srt_track_1 = 'C:\Users\Mario\Downloads\Gossip Girl Season 1\Gossip Girl - 1x10 - Hi  Society.en.srt'
        self.test_srt_track_2 = 'C:\Users\Mario\Downloads\Gossip Girl Season 1\Gossip Girl - 1x10 - Hi  Society.HDTV.XOR.fr.srt'
        self.test_lang_1 = 'eng'
        self.test_lang_2 = 'fra'

        self.correct_srt_args = '--srt-file "C:\Users\Mario\Downloads\Gossip Girl Season 1\Gossip Girl - 1x10 - Hi  Society.en.srt,C:\Users\Mario\Downloads\Gossip Girl Season 1\Gossip Girl - 1x10 - Hi  Society.HDTV.XOR.fr.srt" --srt-codeset UTF-8,UTF-8 --srt-offset 0,0 --srt-lang eng,fra'
        self.correct_file_args = '-i "C:\Users\Mario\Downloads\Gossip Girl Season 1\gossip.girl.s01e10.avi" -o "Z:\Video\TV\Gossip Girl\Gossip.girl.s01e10-1.m4v"'
        self.correct_hand_args = '-i "C:\Users\Mario\Downloads\Gossip Girl Season 1\gossip.girl.s01e10.avi" -o "Z:\Video\TV\Gossip Girl\Gossip.girl.s01e10-1.m4v" --preset "AppleTV 2" --srt-file "C:\Users\Mario\Downloads\Gossip Girl Season 1\Gossip Girl - 1x10 - Hi  Society.en.srt,C:\Users\Mario\Downloads\Gossip Girl Season 1\Gossip Girl - 1x10 - Hi  Society.HDTV.XOR.fr.srt" --srt-codeset UTF-8,UTF-8 --srt-offset 0,0 --srt-lang eng,fra'

        self.non_existent_file = 'c:\\abcd.efg'
        self.always_existent_file = 'c:\\autoexec.bat'

        self.handy_input = core.HandyInput(self.test_in_file, self.test_out_file, self.test_enc_options)
        self.handy_input.addsrt(self.test_srt_track_1,self.test_lang_1)
        self.handy_input.addsrt(self.test_srt_track_2,self.test_lang_2)

    def runTest(self):
        srt_args = self.handy_input.getsrtargs()
        self.assertEqual(self.correct_srt_args,srt_args)

        file_args = self.handy_input.getfileargs()
        self.assertEqual(self.correct_file_args,file_args)

        full_args = self.handy_input.buildargs()
        self.assertEqual(self.correct_hand_args,full_args)

        """Check that no exception is raised with good input/output/srt file"""
        self.handy_input = core.HandyInput(self.always_existent_file, self.non_existent_file, self.test_enc_options)
        self.handy_input.addsrt(self.always_existent_file, 'eng')
        self.handy_input.checkinput()

        """Check that an exception is raised with a bad input file"""
        self.handy_input = core.HandyInput(self.non_existent_file, self.non_existent_file, self.test_enc_options)
        self.assertRaises(IOError, self.handy_input.checkinput)

        """Check that an exception is raised with a bad output file"""
        self.handy_input = core.HandyInput(self.always_existent_file, self.always_existent_file, self.test_enc_options)
        self.assertRaises(IOError, self.handy_input.checkinput)

        """Check that an exception is raised with a bad srt file"""
        self.handy_input = core.HandyInput(self.always_existent_file, self.non_existent_file, self.test_enc_options)
        self.handy_input.addsrt(self.non_existent_file, 'eng')
        self.assertRaises(IOError, self.handy_input.checkinput)


if __name__ == '__main__':
    unittest.main()

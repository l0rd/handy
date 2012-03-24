__author__ = 'Mario'

import subprocess
import os.path
import unittest
import shlex
import time
import sys
from ConfigParser import ConfigParser

properties = "handy.properties"

#TODO: Check for handbrake return code
#TODO: Flush real time handbrake output to console
#TODO: Redirect handbrake output to a log file (i.e. handbrake_[name_of_outputfile].log
#TODO: Rerun the perf test

class HandySrt():

    def __init__(self, srt_file_path, srt_lang, srt_codeset = 'UTF-8', srt_offset='0'):
        self.srt_file_path = srt_file_path
        self.srt_lang = srt_lang
        self.srt_codeset = srt_codeset
        self.srt_offset = srt_offset

class HandyInput():
    def __init__(self, input_file_path, output_file_path, encoding_options):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.encoding_args = encoding_options
        self.srt_list = []

    def addsrt(self, srt_file_path, srt_lang, srt_codeset = 'UTF-8', srt_offset='0'):
        handy_srt = HandySrt(srt_file_path, srt_lang, srt_codeset , srt_offset)
        self.srt_list.append(handy_srt)

    def buildargs(self):
        self.__buildsrtargs()
        self.__buildfilesargs()
        self.handy_input_args =  \
            self.fileargs + " " + \
            self.encoding_args + " " +\
            self.srtargs
        return self.handy_input_args

    def getargs(self):
        self.buildargs()
        return self.handy_input_args

    def getsrtargs(self):
        self.__buildsrtargs()
        return self.srtargs

    def getfileargs(self):
        self.__buildfilesargs()
        return self.fileargs

    def __buildsrtargs(self):
        if len(self.srt_list) == 0 :
            self.srtargs = ''
        else :
            tracks = ",".join(srt.srt_file_path for srt in self.srt_list)
            langs = ",".join(srt.srt_lang for srt in self.srt_list)
            codesets = ",".join(srt.srt_codeset for srt in self.srt_list)
            offsets = ",".join(srt.srt_offset for srt in self.srt_list)

            self.srtargs = '--srt-file "' + tracks + '" ' +\
                           '--srt-codeset ' + codesets + ' ' +\
                           '--srt-offset ' + offsets + ' ' +\
                           '--srt-lang ' + langs

    def __buildfilesargs(self):
        self.fileargs = '-i "' + self.input_file_path +\
               '" -o "' + self.output_file_path + '"'

    def checkinput(self):
        if not os.path.isfile(self.input_file_path):
            raise IOError("Input file \"%s\" does not exists" %self.input_file_path)

        if os.path.isfile(self.output_file_path):
            raise IOError("Output file \"%s\" already exists" %self.output_file_path)

        for srt in self.srt_list:
            if not os.path.isfile(srt.srt_file_path):
                raise IOError("SRT file \"%s\" does not exists" %srt.srt_file_path)

class HandyEncoder():
    def __init__(self, in_file, out_file):
        cfg = ConfigParser()
        cfg.read(properties)

        self.exe_path = cfg.get("handbrake","exe_path")
        self.enc_options = cfg.get("handbrake","encoding_options")
        if not os.path.isfile(self.exe_path):
            raise IOError("Exe file \"%s\" does not exists" %self.exe_path)

        self.handy_input = HandyInput(in_file, out_file, self.enc_options)
        self.handy_input.checkinput()
        self.handbrake_log_file = self.handy_input.output_file_path + '_handy.log'

    def addsrtfile(self,filepath,lang, codeset = 'UTF-8', offset='0'):
        self.handy_input.addsrt(filepath,lang,codeset,offset)
        self.handy_input.checkinput()

    def startencoding(self):
        output_f = open(self.handbrake_log_file, 'w')
        command_line = '"' + self.exe_path + '" ' +\
                    self.handy_input.getargs()
        args = shlex.split(command_line)

        print 'Running Handbrake.',
        p = subprocess.Popen(args, stdout =output_f,
                    stderr =output_f, shell = True, bufsize = -1)
        
        while p.poll() is None :
            print '.',
            sys.stdout.flush()
            time.sleep(1)
        
        print 'DONE'
        rc = p.returncode
        if rc != 0 :
            raise RuntimeWarning("handbrake has exit with error (rc=%d)", rc)

def test1():
    import shutil
    input_file = 'C:\Users\Mario\Videos\Lelouch.avi'
    temp_file = 'C:\Users\Mario\Videos\Lelouch.m4v'
    output_file = 'Z:\Video\Film\Lelouch_1.m4v'
    encoder = HandyEncoder(input_file,temp_file)
    encoder.startencoding()
    shutil.move(temp_file, output_file)

def test2():
    input_file = 'C:\Users\Mario\Videos\Lelouch.avi'
    output_file = 'Z:\Video\Film\Lelouch_2.m4v'
    encoder = HandyEncoder(input_file,output_file)
    encoder.startencoding()

if __name__ == "__main__":
    #input_file = 'C:\Users\Mario\Videos\Lelouch - C''etait Un Rendezvous (1976).avi'
    #output_file = 'C:\Users\Mario\Videos\Lelouch - C''etait Un Rendezvous (1976).m4v'
    #input_file = 'C:\Users\Mario\Downloads\THE DESCENDANTS (2011) DVDScr [H264 MP4][RoB]PR3DATOR RG\THE DESCENDANTS (2011) DVDScr [H264 MP4][RoB]PR3DATOR RG.mp4'
    #output_file = 'Z:\Video\FILM\The descendants.m4v'
    #encoder = HandyEncoder(input_file,output_file)
    #encoder.addsrtfile('C:\Users\Mario\Downloads\THE DESCENDANTS (2011) DVDScr [H264 MP4][RoB]PR3DATOR RG\Spartacus.S02E01.720p.HDTV.X264-DIMENSION.srt','fra')
    #encoder.startencoding()
    print 'Starting TEST1'
    start_time = time.time()
    test1()
    end_time = time.time()
    test1_duration = end_time - start_time
    print 'TEST1 duration: %s' % str(test1_duration)
    print 'Starting TEST2'
    start_time = time.time()
    test2()
    end_time = time.time()
    test2_duration = end_time - start_time
    print 'TEST2 duration: %s' % str(test2_duration)
    os.remove('Z:\Video\Film\Lelouch_1.m4v')    
    os.remove('Z:\Video\Film\Lelouch_2.m4v')    
    print 'Starting TEST1'
    start_time = time.time()
    test1()
    end_time = time.time()
    test1_duration = end_time - start_time
    print 'TEST1 duration: %s' % str(test1_duration)
    print 'Starting TEST2'
    start_time = time.time()
    test2()
    end_time = time.time()
    test2_duration = end_time - start_time
    print 'TEST2 duration: %s' % str(test2_duration)
    os.remove('Z:\Video\Film\Lelouch_1.m4v')    
    os.remove('Z:\Video\Film\Lelouch_2.m4v')    
    print 'Starting TEST1'
    start_time = time.time()
    test1()
    end_time = time.time()
    test1_duration = end_time - start_time
    print 'TEST1 duration: %s' % str(test1_duration)
    print 'Starting TEST2'
    start_time = time.time()
    test2()
    end_time = time.time()
    test2_duration = end_time - start_time
    print 'TEST2 duration: %s' % str(test2_duration)
    os.remove('Z:\Video\Film\Lelouch_1.m4v')    
    os.remove('Z:\Video\Film\Lelouch_2.m4v')    
    print 'Starting TEST1'
    start_time = time.time()
    test1()
    end_time = time.time()
    test1_duration = end_time - start_time
    print 'TEST1 duration: %s' % str(test1_duration)
    print 'Starting TEST2'
    start_time = time.time()
    test2()
    end_time = time.time()
    test2_duration = end_time - start_time
    print 'TEST2 duration: %s' % str(test2_duration)
    os.remove('Z:\Video\Film\Lelouch_1.m4v')    
    os.remove('Z:\Video\Film\Lelouch_2.m4v')    
    print 'Starting TEST1'
    start_time = time.time()
    test1()
    end_time = time.time()
    test1_duration = end_time - start_time
    print 'TEST1 duration: %s' % str(test1_duration)
    print 'Starting TEST2'
    start_time = time.time()
    test2()
    end_time = time.time()
    test2_duration = end_time - start_time
    print 'TEST2 duration: %s' % str(test2_duration)
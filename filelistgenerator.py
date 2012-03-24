from json import encoder
from core import HandyEncoder

__author__ = 'Mario'

import os, fnmatch
from os.path import basename

def matching_files(pattern, basedir=os.curdir):
    '''Locate all files matching supplied filename pattern in and below
  supplied root directory.'''
    for path, dirs, files in os.walk(os.path.abspath(basedir)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)

class FileSetGenerator():
    def __init__(self,files_dir, file_pattern):
        self.files_dir = files_dir
        self.file_pattern = file_pattern
        self.__check_parameters()

    def __check_parameters(self):
        if not os.path.isdir(self.files_dir):
            raise IOError('files_dir "%s" does not exist')

    def create_file_list(self):
        return matching_files(self.file_pattern, self.files_dir)

class FileListGenerator(FileSetGenerator):
    def __init__(self, files_dir, file_pattern, index_position):
        FileSetGenerator.__init__(self,files_dir, file_pattern)
        self.index_position = index_position

    def __get_index_from_file(self,filename):
        pos = self.index_position
        idx_str = filename[pos:pos+2]
        idx_int = int(idx_str)
        return idx_int

    def create_file_list(self):
        for next_file in matching_files(self.file_pattern, self.files_dir) :
            idx = self.__get_index_from_file(basename(next_file))
            yield {"index":idx, "file_path":next_file}

if __name__ == "__main__":
    input_file_pattern = "gossip.girl.s01e*.avi"
    season_dir = "C:\Users\Mario\Downloads\Gossip Girl Season 1"
    output_dir = "Z:\Video\TV\Gossip Girl"
    srt_file_patterns = [{"track":"Gossip Girl - 1xIDX*.en.srt","lang":"eng"},
            {"track":"Gossip Girl - 1xIDX*.fr.srt","lang":"fra"}]
    idx_position = 16

    gossip1 = FileListGenerator(season_dir, input_file_pattern, idx_position)
    for video_file_path in gossip1.create_file_list():
        file_path=video_file_path["file_path"]
        file_idx=video_file_path["index"]
        print file_idx, file_path
        for srt_file_pattern in srt_file_patterns :
            srt_lang = srt_file_pattern["lang"]
            srt_pattern = srt_file_pattern["track"].replace("IDX","%02d"%file_idx)
            srt_files = FileSetGenerator(season_dir,srt_pattern)
            for srt_file in srt_files.create_file_list():
                print '\t', srt_lang.upper(), srt_file

#    for infilepath in matching_files(input_file_pattern,season_dir):
#        idx = self.get_index_from_file(basename(infilepath))
#        en_srt_file_pattern = "Gossip Girl - 1x%02d*.en.srt" % idx
#        fr_srt_file_pattern = "Gossip Girl - 1x%02d*.fr.srt" % idx
#        # #avifilename = avi_file_prefix + "%02d" % i + ".avi"
#        en_srt_filename = ''
#        for filename in matching_files(en_srt_file_pattern,season_dir):
#            en_srt_filename = filename
#        fr_srt_filename = ''
#        for filename in matching_files(fr_srt_file_pattern,season_dir):
#            fr_srt_filename = filename
#
#        output_filename = output_dir + "\Gossip Girl-Season 1-Episode %02d.m4v" % idx
#        encoder = HandyEncoder(infilepath,output_filename)
#
#        if en_srt_filename != '' : encoder.addsrtfile(en_srt_filename,'eng')
#        if fr_srt_filename != '' : encoder.addsrtfile(fr_srt_filename,'fra')
#        encoder.startencoding()

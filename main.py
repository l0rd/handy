from ConfigParser import ConfigParser
import os
import core
import filelistgenerator

__author__ = 'Mario'
class MainEncoder():
    def __build_srt_file_list(self):
        languages = []
        if cfg.has_option("input","srt_languages") :
            languages = cfg.get("input","srt_languages").split(',')

        self.srt_file_list = []
        for lang in languages:
            if cfg.has_option("input","srt_file.%s"%lang) :
                file_path = cfg.get("input","srt_file.%s"%lang)
                self.srt_file_list.append({"track":file_path, "lang":lang})

    def __init__(self,cfg_file):
        self.cfg = ConfigParser()
        self.cfg.read(cfg_file)
        self.input_file_directory = self.cfg.get("input","file_directory")
        self.output_file_directory = self.cfg.get("output","file_directory")
        self.__build_srt_file_list()
        self.video_files = []

    def __repr__(self):
        str_buffer = ''
        for idx, video_file in enumerate(self.video_files) :
            str_buffer +="Creating file %s\n" % (video_file["output_file_path"])
            str_buffer +="\t* Input file: %s\n" % (video_file["input_file_path"])
            for srt_file in video_file["srt_files"] :
                str_buffer +="\t* %s subtitle file: %s\n" % (srt_file["lang"].upper(), srt_file["track"])
        return str_buffer

    def run(self):
        for video_file in self.video_files :
            input_file = video_file["input_file_path"]
            output_file = video_file["output_file_path"]
            encoder = core.HandyEncoder(input_file,output_file)
            for srt_file in video_file["srt_files"] :
                encoder.addsrtfile(srt_file["track"],srt_file["lang"],codeset='ANSI_X3.4')
            encoder.startencoding()

class SingleMovieEncoder(MainEncoder):

    def __init__(self,cfg_file):
        MainEncoder.__init__(self, cfg_file)
        self.__build_video_file_list()

    def __build_video_file_list(self):

        input_file_name = self.cfg.get("movie","input_file_name")
        input_file_path = os.path.join(self.input_file_directory,
            input_file_name)

        output_file_name = os.path.basename(input_file_name)[0]
        output_file_path = os.path.join(self.output_file_directory,
            output_file_name)

        movie = {"input_file_path":input_file_path,
                 "output_file_path":output_file_path,
                 "srt_files": []}

        for srt_file_info in self.srt_file_list :
            srt_lang = srt_file_info["lang"]
            srt_file_path = srt_file_info["track"]
            srt_file = {"track":srt_file_path,"lang":srt_lang}
            movie["srt_files"].append(srt_file)

        self.video_files.append(movie)

class MultipleMovieEncoder(MainEncoder):

    def __init__(self,cfg_file):
        MainEncoder.__init__(self, cfg_file)
        self.__build_video_file_list()

    def __build_video_file_list(self):

        input_file_name = self.cfg.get("movie","input_file_name")

        movies = filelistgenerator.FileSetGenerator(
            self.input_file_directory,
            input_file_name)

        for input_file_path in movies.create_file_list():
            output_file_name = os.path.splitext(os.path.basename(input_file_path))[0] + '.m4v'
            output_file_path = os.path.join(self.output_file_directory,
                output_file_name)
            movie = {"input_file_path":input_file_path,
                     "output_file_path":output_file_path,
                     "srt_files": []}
            self.video_files.append(movie)

class SerialEncoder(MainEncoder):

    def __init__(self,cfg_file):
        MainEncoder.__init__(self, cfg_file)
        self.__build_video_file_list()

    def __build_video_file_list(self):
        input_file_pattern = self.cfg.get("serial","input_file_pattern")
        output_file_pattern = self.cfg.get("serial","output_file_pattern")
        idx_position = int(cfg.get("serial","input_file_pattern.episode_num_position"))

        serial_episodes = filelistgenerator.FileListGenerator(
            self.input_file_directory,
            input_file_pattern,
            idx_position)

        for episode_file in serial_episodes.create_file_list():
            episode_num = episode_file["index"]
            episode_input_file_path = episode_file["file_path"]
            episode_output_file_path = os.path.join(self.output_file_directory,
                output_file_pattern.replace("[EPISODE_NUM]","%02d"%episode_num))
            episode = {"input_file_path":episode_input_file_path,
                       "output_file_path":episode_output_file_path,
                       "srt_files": []}

            for srt_file_pattern in self.srt_file_list :
                srt_lang = srt_file_pattern["lang"]
                srt_pattern = srt_file_pattern["track"].replace("[EPISODE_NUM]","%02d"%episode_num)
                srt_files = filelistgenerator.FileSetGenerator(self.input_file_directory,srt_pattern)
                for srt_file_path in srt_files.create_file_list():
                    srt_file = {"track":srt_file_path,"lang":srt_lang}
                    episode["srt_files"].append(srt_file)

            self.video_files.insert(episode_num, episode)

if __name__ == "__main__":
    cfg = ConfigParser()
    cfg.read(core.properties)
    if cfg.get("input","method") == "serial" :
        encoder = SerialEncoder(core.properties)
    elif cfg.get("input","method") == "single_movie" :
        encoder = SingleMovieEncoder(core.properties)
    elif cfg.get("input","method") == "multiple_movies" :
        encoder = MultipleMovieEncoder(core.properties)
    #print encoder
    encoder.run()

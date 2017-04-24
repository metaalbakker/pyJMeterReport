import pandas as pd
import glob
import os

class PerfData:

    """
    Base Class that reads in the files that reads in comma separated value files with an optional delimiter
    and puts them in a pandas object for further processing
    Also provides function for calculating meaningful statistics
    """

    __log_dir = ""
    __file_format = ""
    __perf_delimiter = ','
    __file_path = ""
    __data_frame = pd.DataFrame()

    def __init__(self, log_dir, file_format, delimiter=','):
        self.__log_dir = log_dir
        self.__file_format = file_format
        self.__perf_delimiter = delimiter
        self.__file_path = os.path.join(log_dir,"*"+file_format)
        self.read_logs()

    def read_logs(self):
        all_files = glob.glob(self.__file_path)
        df_perfdata = pd.DataFrame()
        list_ = []
        df_from_each_file = (pd.read_csv(f) for f in all_files)
        self.__data_frame = pd.concat(df_from_each_file, ignore_index=True)
        #self.__data_frame.fillna("bier")

    def set_index(self, index_name):
        self.__data_frame.set_index(index_name, inplace=True)

    def get_dataframe(self):
        return self.__data_frame

    #sort dataframe on a specific column
    def sort_dataframe(self, column_name):
        df_ = self.__data_frame
        #df_.sort([column_name], ascending=[1])
        df_.sort_values(column_name)

    def select_columns(self, column_list):
        self.__data_frame = self.__data_frame[column_list]

    def get_column(self, column_name):
        return self.__data_frame[column_name]

    def calculate_stats(self, df_):
        return 'statistieken'


    #def calculation,with a time column defined

    def __str__(self):
        return ("Files are read from %s" % (self.__file_path))
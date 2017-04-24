from .PerfData import PerfData
import time
import datetime
import pandas as pd

class PerfmonData(PerfData):

    """
    Class providing the tools for processing JTL files, based on the PerfData Class
    Used to calculate statistics of the jtl file
    """

    __statistics = {}
    __statistics['PerfmonData'] = {}
    __round_number = 2

    def __init__(self, log_dir, file_format):
        PerfData.__init__(self,log_dir,file_format)
        self.load_perfmon_data()
        #PerfData.set_index(self,"timeStamp")
        self.calculate_statistics()

    def perfmon_string_to_timestamp(self, timestamp_string):
        timestamp_string_ = str(timestamp_string).replace('\"','')
        timestamp_string_ = time.mktime(datetime.datetime.strptime(timestamp_string_, "%m/%d/%Y %H:%M:%S.%f").timetuple())
        return timestamp_string_

    def load_perfmon_data(self):

        df_ = self._PerfData__data_frame

        #hernoem de timestamp kolom
        df_.rename(columns=lambda x: "timeStamp" if "(PDH" in x else x, inplace=True)

        #Load all values as numbers
        for col in df_:
            if col!="timeStamp":
                df_[col] = pd.to_numeric(self._PerfData__data_frame[col], errors='coerce')

        #Timestamps from string to unix
        df_["timeStamp"] = df_["timeStamp"].apply(lambda x : self.perfmon_string_to_timestamp(x))

        #print(df_["timeStamp"])


    def __str__(self):
        return str(PerfData.get_dataframe(self))

    #calculate the stats for a certain column for all labels individually
    def calculate_statistics(self):

        df_ = self._PerfData__data_frame
        stats_ = self.__statistics

        df_ = df_.set_index("timeStamp")

        #print(df_)

        metingids_ = list(df_)

        mean_ = df_.mean()
        percentile_ = df_.quantile([0.5, 0.75, 0.95, 0.99])
        st_dev_ = df_.std()
        min_ = df_.min()
        max_ = df_.max()
        count_ = df_.count()

        for metingid_ in metingids_:
            print(metingid_)

            item_ = metingid_.split('\\')

            appserver_ = item_[2]
            metric_ = item_[4]+'\\'+item_[5]

            if appserver_ not in stats_['PerfmonData']:  stats_['PerfmonData'][appserver_] = {}
            if True not in stats_["PerfmonData"][appserver_]: stats_['PerfmonData'][appserver_][True] = {}

            stats_['PerfmonData'][appserver_][True][metric_] = {}
            stats_['PerfmonData'][appserver_][True][metric_]['Count'] = round(count_[metingid_],self.__round_number)
            stats_['PerfmonData'][appserver_][True][metric_]['Mean'] = round(mean_[metingid_],self.__round_number)
            stats_['PerfmonData'][appserver_][True][metric_]['Min'] = round(min_[metingid_],self.__round_number)
            stats_['PerfmonData'][appserver_][True][metric_]['Max'] = round(max_[metingid_],self.__round_number)
            stats_['PerfmonData'][appserver_][True][metric_]['StDev'] = round(st_dev_[metingid_],self.__round_number)
            stats_['PerfmonData'][appserver_][True][metric_]['Percentile.50'] = round(percentile_[metingid_].get_value(0.5),self.__round_number)
            stats_['PerfmonData'][appserver_][True][metric_]['Percentile.75'] = round(percentile_[metingid_].get_value(0.75),self.__round_number)
            stats_['PerfmonData'][appserver_][True][metric_]['Percentile.95'] = round(percentile_[metingid_].get_value(0.95),self.__round_number)
            stats_['PerfmonData'][appserver_][True][metric_]['Percentile.99'] = round(percentile_[metingid_].get_value(0.99),self.__round_number)

    #get the statistics for a specified list of columns
    def get_statistics(self):
        return self.__statistics

    def get_yframe(self,meting,column):

        df_ = self._PerfData__data_frame

        label_ = "\\\\"+meting+"\\\\"+column

        return df_[label_]







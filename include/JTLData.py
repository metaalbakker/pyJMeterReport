from .PerfData import PerfData #moet echt PerfData noemen om de klasse te importeren, anders is het een methode

class JTLData(PerfData):

    """
    Class providing the tools for processing JTL files, based on the PerfData Class
    Used to calculate statistics of the jtl file and to make graphs over time of statistics
    """

    __columns = ["elapsed","bytes"]
    __important_columns = ["label","timeStamp","elapsed","bytes","success"]
    __statistics = {}
    __statistics["JTLData"] = {}
    __round_number = 0

    def __init__(self, log_dir, file_format):
        PerfData.__init__(self,log_dir,file_format)
        PerfData.select_columns(self, self.__important_columns)
        PerfData.sort_dataframe(self, ["timeStamp"])
        #PerfData.set_index(self,"label")
        self.calculate_statistics()

        print('hoi7')

    def __str__(self):
        return str(PerfData.get_dataframe(self))

    #calculate the stats for a certain column for all labels individually
    def calculate_statistics(self):

        df_ = self._PerfData__data_frame


        metingids_ = set(df_["label"])
        stats_ = self.__statistics
        columns_ = self.__columns

        #dit kan vast nog soepeler met pandas, een dataframe van maken ofzo naar json? iets met apply en lambda's en een  nieuw dataframe
        # er is een to_json functie, maar nu eerst even verder hiermee, weet nog nie tof die soepel genoeg is

        for metingid_ in metingids_:
            print(metingid_)

            #for status_ in df_["success"].unique():
            for status_ in (True,False):

                if metingid_ not in stats_["JTLData"]:  stats_["JTLData"][metingid_] = {}

                split_df_ = df_.loc[(df_["label"]==metingid_) & (df_["success"]==status_)]

                if not split_df_.empty:
                    mean_ = split_df_._get_numeric_data().mean() #get_numeric_data erbij voor performance, gaat nie tgoed met de objecten, heel traag, te traag
                    percentile_ = split_df_.quantile([0.5, 0.75, 0.95, 0.99])
                    st_dev_ = split_df_.std()
                    min_ = split_df_.min()
                    max_ = split_df_.max()
                    count_ = split_df_.count()
                    for column_ in columns_:
                        if status_ not in stats_["JTLData"][metingid_]: stats_["JTLData"][metingid_][status_] = {}
                        if column_ not in stats_["JTLData"][metingid_]: stats_["JTLData"][metingid_][status_][column_] = {}
                        stats_["JTLData"][metingid_][status_][column_]['Count'] = round(count_[column_],self.__round_number)
                        stats_["JTLData"][metingid_][status_][column_]['Mean'] = round(mean_[column_],self.__round_number)
                        stats_["JTLData"][metingid_][status_][column_]['Min'] = round(min_[column_],self.__round_number)
                        stats_["JTLData"][metingid_][status_][column_]['Max'] = round(max_[column_],self.__round_number)
                        stats_["JTLData"][metingid_][status_][column_]['StDev'] = round(st_dev_[column_],self.__round_number)
                        stats_["JTLData"][metingid_][status_][column_]['Percentile.50'] = round(percentile_[column_].get_value(0.5),self.__round_number)
                        stats_["JTLData"][metingid_][status_][column_]['Percentile.75'] = round(percentile_[column_].get_value(0.75),self.__round_number)
                        stats_["JTLData"][metingid_][status_][column_]['Percentile.95'] = round(percentile_[column_].get_value(0.95),self.__round_number)
                        stats_["JTLData"][metingid_][status_][column_]['Percentile.99'] = round(percentile_[column_].get_value(0.99),self.__round_number)

    #get the statistics for a specified list of columns
    def get_statistics(self):
        return self.__statistics

    def get_yframe(self,meting,column):

        df_ = self._PerfData__data_frame
        df_ = df_.loc[(df_["label"] == meting) & (df_["success"] == True)]

        return df_[column]










import sys
import os

work_path = str(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, str(os.getcwd())+'/include')
sys.path.insert(1, work_path +'/include')

results_directory = 'results'
graphsdir = 'images'
loguseddir = 'used_logs'
backupdir = 'backup'
logusederrordir = 'error_logs'

jtl_docx_filename = "Performance_Testrapport_jtl.docx"
perfmon_docx_filename = "Performance_Testrapport_perfmon.docx"

from include import JTLData
from include import PerfmonData
from include import PerfdataImages
from include import CustomReport

def make_subfolders():
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)
    if not os.path.exists(results_directory + '/' + graphsdir):
        os.makedirs(results_directory + '/' + graphsdir)
    if not os.path.exists(results_directory + '/' + loguseddir):
        os.makedirs(results_directory + '/' + loguseddir)
    if not os.path.exists(results_directory + '/' + backupdir):
        os.makedirs(results_directory + '/' + backupdir)
    if not os.path.exists(results_directory + '/' + logusederrordir):
        os.makedirs(results_directory + '/' + logusederrordir)



if __name__ == "__main__":

    #clear the command line screen
    os.system('cls')

    print('test')
    make_subfolders()

    print('laad data')

    #jtl_performance_data = JTLData('logfiles','jtl')
    jtl_performance_data = JTLData('logfiles', 'jtl')

    print('laad data2')

    perfmon_performance_data = PerfmonData('logfiles','csv')


    print('bereken statistieken')

    ### calculate the statistics
    jtl_performance_data.calculate_statistics()
    perfmon_performance_data.calculate_statistics()


    print('maak json object')

    ### get the json
    jtl_stats_json = jtl_performance_data.get_statistics()
    perfmon_stats_json = perfmon_performance_data.get_statistics()

    print('maak de plaatjes')

    #maak de plaatjes
    images_jtl = PerfdataImages.make_images(jtl_performance_data,jtl_stats_json,"timeStamp",results_directory,graphsdir)
    images_perfmon = PerfdataImages.make_images(perfmon_performance_data, perfmon_stats_json, "timeStamp",results_directory, graphsdir)

    print('maak het rapport')

    #maka het rapport
    docx_jtl = CustomReport.make_report('JTLData',jtl_docx_filename, jtl_stats_json, images_jtl,results_directory)
    docx_perfmon = CustomReport.make_report('PerfmonData', perfmon_docx_filename, perfmon_stats_json, images_perfmon, results_directory)





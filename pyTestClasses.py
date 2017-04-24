import sys
import os

work_path = str(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(1, str(os.getcwd())+'/include')
sys.path.insert(1, work_path +'/include')

os.system('cls')

def testfunctie(x):
    print(x)
    return

class PerfmonData:

    __logdir = ""

    def __init__(self, logdir):
        self.__logdir = logdir

    def __str__(self):
        return ("Logfile directory is %s" % self.__logdir)


class PerfmonStats:

    def __init__(self, input1):
        teststring = "Hoi"+input1
        print(teststring)


if __name__ == "__main__":

    test = PerfmonData("testdirectory")

    print(test)

    print(dir(test))
    print(dir(""))
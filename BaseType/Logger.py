import os
import datetime

from BaseType.Config import Config
from ModelHelper.FileHelper import FileAppendWrite

class Logger():
    def __new__(self, filePath, printFlag):
        self.filePath = filePath
        self.printFlag = printFlag

    def __init__(self):
        pass

    @classmethod
    def UNKOWN(self, logStr):
        Logger.Log(self, logStr, "UNKOWN")

    @classmethod
    def INFO(self, logStr):
        Logger.Log(self, logStr, "INFO")

    @classmethod
    def WARNING(self, logStr):
        Logger.Log(self, logStr, "WARNING")

    @classmethod
    def ERROR(self, logStr):
        Logger.Log(self, logStr, "ERROR")

    def Log(self, logStr, loggerType):
        if not os.path.exists(Config.LogFolderPath):
            os.makedirs(Config.LogFolderPath)
        dateTodayStr = datetime.datetime.now().strftime("%Y%m%d")
        LogFilePath = Config.LogFolderPath + "log_" + dateTodayStr + ".log"

        datetimeNowStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        try:
            lines = []
            for lineTemp in logStr.split("\n"):
                for line in lineTemp.split("\r"):
                    if self.printFlag:
                        print(line)
                    lines.append("[%s] " % datetimeNowStr + "[%s] " % loggerType + "[%s] " % self.filePath + line)
                    print(lines)

            FileAppendWrite(LogFilePath, lines)
        except:
            pass
        
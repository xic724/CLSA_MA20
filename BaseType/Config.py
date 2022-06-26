from ModelHelper.ConfigHelper import LoadConfigFileAsDict

class Config():
    def __new__(self):
        self.StaticDataFolderPath = None
        self.LogFolderPath = None

    def __init__(self):
        pass

    @classmethod
    def LoadConfigFile(self):
        configFileDict = LoadConfigFileAsDict("./config.txt")

        if "StaticDataFolderPath" in configFileDict:
            self.StaticDataFolderPath = configFileDict["StaticDataFolderPath"]

        if "LogFolderPath" in configFileDict:
            self.LogFolderPath = configFileDict["LogFolderPath"]
            
from ModelHelper.FileHelper import ReadFileToLines

def LoadConfigFileAsDict(filePath):
    configDict = dict()
    lines = ReadFileToLines(filePath)
    for line in lines:
        if "=" not in line:
            continue
        if line.strip()[0] == "#" or line.strip()[:2] == "//":
            continue

        configKey = line.strip().split("=")[0].strip()
        configValue = line.strip().split("=")[1].strip()
        configDict[configKey] = configValue
    return configDict
    
def FileAppendWrite(filePath, lines):
    with open(filePath, "a") as fa:
        for line in lines:
            fa.write(line + "\n")

def ReadFileToLines(filePath):
    with open(filePath) as fr:
        lines = fr.readlines()
        lines = [line.strip().replace("\n", "") for line in lines if line.strip() != ""]
        return lines
        
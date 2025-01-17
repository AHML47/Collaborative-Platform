from datetime import datetime


class Log :
    def __init__(self,filePath):
        self.filePath=filePath

    def write(self,message):
        date = "["+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"] : "
        with open(self.filePath, 'a') as file:
            file.write(date+message+'\n')





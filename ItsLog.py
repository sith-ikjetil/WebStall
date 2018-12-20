import datetime

LOG_TYPE_INFORMATION = 1
LOG_TYPE_WARNING = 2
LOG_TYPE_ERROR = 3
LOG_TYPE_DEBUG = 4
LOG_TYPE_OTHER = 5

class ItsApplicationLog():
    def __init__(self):
        self.log = []

    def Log(self, type = LOG_TYPE_INFORMATION, message = "?"):
        switcher = {
            1: "(i)",
            2: "(w)",
            3: "(e)",
            4: "(d)",
            5: "(o)"
        }

        msg = "{tm}: {t} - {msg}".format(tm=datetime.datetime.now().isoformat(),
                                         t=switcher.get(type, "(?)"),
                                         msg=message)
        self.log.append(msg)

    def GetLogItems(self):
        return self.log

    def ClearLog(self):
        self.log.clear()

    def LogInformation(self, msg):
        self.Log(LOG_TYPE_INFORMATION, msg)

    def LogWarning(self, msg):
        self.Log(LOG_TYPE_WARNING, msg)

    def LogError(self,msg):
        self.Log(LOG_TYPE_ERROR, msg)

    def LogDebug(self, msg):
        self.Log(LOG_TYPE_DEBUG, msg)

    def LogOther(self, msg):
        self.Log(LOG_TYPE_OTHER, msg)

    def PrintToConsole(self):
        for a in self.log:
            print(a)

    def ToString(self):
        result = ""
        for a in self.log:
            result += a
            result += "\n"

        return result

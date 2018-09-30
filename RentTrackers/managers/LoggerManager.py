

class LoggerManager:

    @staticmethod
    def debug(tag, msg):
        print("DEBUG: {} -- {}".format(tag, msg))

    @staticmethod
    def info(tag, msg):
        print("INFO: {} -- {}".format(tag, msg))

    @staticmethod
    def error(tag, msg):
        print("!!! ERROR: {} -- {}".format(tag, msg))



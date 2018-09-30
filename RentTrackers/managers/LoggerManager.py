

class LoggerManager:

    @staticmethod
    def debug(tag, msg):
        level = "DEBUG"
        print("-- {} -- {} -- {}".format(level, tag, msg))

    @staticmethod
    def info(tag, msg):
        level = "INFO"
        print("-- {} -- {} -- {}".format(level, tag, msg))

    @staticmethod
    def error(tag, msg):
        level = "ERROR"
        print("!!! {} -- {} -- {}".format(level, tag, msg))


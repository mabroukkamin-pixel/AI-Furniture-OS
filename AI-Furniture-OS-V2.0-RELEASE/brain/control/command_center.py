
import json
import datetime


class CommandCenter:


    def status(self):

        return {
            "system":"AI Furniture OS V2",
            "controller":"ACTIVE",
            "time":str(datetime.datetime.now())
        }

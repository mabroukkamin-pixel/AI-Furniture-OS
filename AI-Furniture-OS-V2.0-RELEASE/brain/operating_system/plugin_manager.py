
import os


class PluginManager:


    def __init__(self):

        self.plugins=[]



    def scan(self):


        root="brain"


        for item in os.listdir(root):

            if item not in [

            "legacy",

            "__pycache__"

            ]:

                self.plugins.append(item)



        return self.plugins




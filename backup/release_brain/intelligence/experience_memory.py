
import json
import os
import datetime



class ExperienceMemory:


    def __init__(self):

        self.file="brain/memory/experience.json"



    def save(self,data):

        os.makedirs(
        os.path.dirname(self.file),
        exist_ok=True
        )


        old=[]


        if os.path.exists(self.file):

            with open(self.file,"r",encoding="utf-8") as f:

                old=json.load(f)



        old.append(data)



        with open(self.file,"w",encoding="utf-8") as f:

            json.dump(
            old,
            f,
            indent=4,
            ensure_ascii=False
            )




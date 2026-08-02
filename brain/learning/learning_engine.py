import json,os,datetime


class LearningEngine:


    def learn(self,data=None):

        memory={

        "date":str(datetime.datetime.now()),

        "learned":True,

        "data":data

        }


        os.makedirs(
        "brain/learning",
        exist_ok=True)


        with open(
        "brain/learning/memory.json",
        "w",
        encoding="utf8") as f:

            json.dump(
            memory,
            f,
            indent=4)


        return memory

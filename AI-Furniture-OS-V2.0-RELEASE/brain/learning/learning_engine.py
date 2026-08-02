import os
import json
import datetime


class ExperienceMemory:

    def __init__(self):

        self.file = 'brain/learning/experience_memory.json'

        os.makedirs(
            os.path.dirname(self.file),
            exist_ok=True
        )

        if not os.path.exists(self.file):

            with open(
                self.file,
                'w',
                encoding='utf-8'
            ) as f:

                json.dump(
                    [],
                    f,
                    indent=4
                )


    def load(self):

        with open(
            self.file,
            'r',
            encoding='utf-8'
        ) as f:

            return json.load(f)


    def save(self,data):

        with open(
            self.file,
            'w',
            encoding='utf-8'
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )


    def add(self,experience):

        data=self.load()

        data.append(experience)

        self.save(data)

        return True



class LearningEngine:


    def __init__(self):

        self.memory=ExperienceMemory()



    def analyze(self):

        data=self.memory.load()

        result={

            'total_experiences':len(data),

            'success':0,

            'failed':0,

            'patterns':{}

        }


        for item in data:

            if item.get('success'):

                result['success']+=1

            else:

                result['failed']+=1


            style=item.get(
                'style',
                'unknown'
            )


            if style not in result['patterns']:

                result['patterns'][style]=0


            result['patterns'][style]+=1


        return result



    def learn_from_run(self):

        experience={

            'time':str(datetime.datetime.now()),

            'product':'Partition001',

            'style':'gulf_villa',

            'score':100,

            'success':True,

            'source':'AIFOS EXPERIENCE CORE'

        }


        self.memory.add(experience)


        return self.analyze()



if __name__=='__main__':

    engine=LearningEngine()

    print(
        engine.learn_from_run()
    )


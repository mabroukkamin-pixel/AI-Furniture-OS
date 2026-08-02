import os
import json
import datetime


class EvolutionEngine:


    def __init__(self):

        self.learning_file = "brain/learning/experience_memory.json"

        self.weight_file = "brain/evolution/evolution_memory.json"

        os.makedirs(
            "brain/evolution",
            exist_ok=True
        )


        if not os.path.exists(self.weight_file):

            with open(
                self.weight_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    {},
                    f,
                    indent=4
                )


    def load_experience(self):

        if not os.path.exists(
            self.learning_file
        ):

            return []

        with open(
            self.learning_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def load_weights(self):

        with open(
            self.weight_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def save_weights(self,data):

        with open(
            self.weight_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )



    def evolve(self):


        experiences=self.load_experience()

        weights=self.load_weights()


        for item in experiences:


            style=item.get(
                "style",
                "unknown"
            )


            if style not in weights:

                weights[style]={
                    "runs":0,
                    "success":0,
                    "confidence":50
                }


            weights[style]["runs"] += 1


            if item.get("success"):

                weights[style]["success"] += 1



            weights[style]["confidence"] = round(
                (
                    weights[style]["success"]
                    /
                    weights[style]["runs"]
                ) * 100
            )



        self.save_weights(weights)


        return {

            "status":"EVOLVED",

            "time":str(datetime.datetime.now()),

            "weights":weights

        }



if __name__=="__main__":

    engine=EvolutionEngine()

    print(
        engine.evolve()
    )

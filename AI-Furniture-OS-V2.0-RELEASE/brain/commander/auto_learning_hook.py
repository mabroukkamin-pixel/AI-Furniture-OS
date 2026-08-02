from brain.learning.experience_collector import ExperienceCollector
from brain.commander.learning_bridge import LearningBridge
from brain.commander.evolution_bridge import EvolutionBridge


class AutoLearningHook:


    def __init__(self):

        self.collector = ExperienceCollector()
        self.learning = LearningBridge()
        self.evolution = EvolutionBridge()



    def run(self):


        experience = self.collector.add_experience(

            {
            "product":"Partition001",
            "material":"rattan",
            "style":"gulf_villa",
            "score":95,
            "success":True
            }

        )


        learning_result = self.learning.learn()


        evolution_result = self.evolution.evolve()


        return {

            "experience":experience,

            "learning":learning_result,

            "evolution":evolution_result

        }



if __name__=="__main__":

    print(
        AutoLearningHook().run()
    )


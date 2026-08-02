from brain.learning.learning_engine import LearningEngine


class LearningBridge:


    def __init__(self):

        self.engine = LearningEngine()


    def learn(self):

        result = self.engine.learn_from_run()

        return {

            "learning_status": "ACTIVE",

            "experience": result

        }



if __name__ == "__main__":

    print(
        LearningBridge().learn()
    )

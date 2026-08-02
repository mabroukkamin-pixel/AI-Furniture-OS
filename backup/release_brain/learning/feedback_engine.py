from brain.learning.learning_engine import LearningEngine


class FeedbackEngine:


    def run(self):

        engine=LearningEngine()

        return engine.learn_from_run()



if __name__=='__main__':

    print(
        FeedbackEngine().run()
    )


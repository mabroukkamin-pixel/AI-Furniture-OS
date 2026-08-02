from brain.learning.experience_memory import ExperienceMemory
from brain.learning.learning_engine import LearningEngine
from brain.learning.reward_system import RewardSystem


class LearningExecutor:


    def __init__(self):

        self.memory = ExperienceMemory()
        self.learning = LearningEngine()
        self.reward = RewardSystem()



    def execute(self, state):


        experience = self.learning.learn(
            state
        )


        reward = self.reward.calculate(
            experience
        )


        experience["reward"] = reward


        self.memory.save(
            experience
        )


        state.learning = experience


        print("==============================")
        print("LEARNING ENGINE")
        print("==============================")
        print("Experience saved")


        print("==============================")
        print("REWARD SYSTEM")
        print("==============================")
        print(reward)


        return state

from brain.autonomous.task_manager import TaskManager


class GoalManager:


    def execute(self):

        return TaskManager().run()



if __name__=='__main__':

    print(
        GoalManager().execute()
    )

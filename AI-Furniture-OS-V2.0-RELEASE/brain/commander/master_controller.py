
from brain.commander.commander import AIFOSCommander


class MasterController:


    def execute(self):

        return AIFOSCommander().run()



if __name__=="__main__":

    print(
    MasterController().execute()
    )

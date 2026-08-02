import datetime


from brain.commander.command_router import CommandRouter


class AutonomousCore:


    def __init__(self):

        self.router = CommandRouter()

        self.state = {
            "system": "AI Furniture OS V2",
            "mode": "AUTONOMOUS",
            "started": str(datetime.datetime.now()),
            "cycles":0
        }



    def run_cycle(self):

        print("")
        print("==============================")
        print(" AI FURNITURE OS AUTONOMOUS ")
        print(" CYCLE START ")
        print("==============================")



        result = self.router.route("AUTO")


        self.state["cycles"] += 1


        print("")
        print("AUTONOMOUS RESULT")
        print(result)



        return result



    def run(self, cycles=1):


        for i in range(cycles):

            self.run_cycle()



        print("")
        print("==============================")
        print(" AUTONOMOUS MODE COMPLETE ")
        print("==============================")



        print(self.state)



if __name__=="__main__":

    AutonomousCore().run(1)
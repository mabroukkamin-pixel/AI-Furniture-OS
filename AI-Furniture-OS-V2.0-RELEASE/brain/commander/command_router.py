import sys


class CommandRouter:


    def route(self, command):


        command = command.upper()


        if command == "FULL":

            return self.full()



        if command == "PRODUCTION":
            return self.production()

        
        if command == "BUILD":

            from brain.system.aifos_master import AIFOSMaster

            return AIFOSMaster().build()


        if command == "AUTO":

            return self.auto()



        if command == "CHECK":

            return self.check()



        if command == "LEARN":

            return self.learn()



        if command == "EVOLVE":

            return self.evolve()



        return {

            "error":"UNKNOWN COMMAND"

        }



    def full(self):

        return {

            "command":"FULL",

            "status":"READY"

        }





    def production(self):

        from brain.production.production_brain import ProductionBrain

        result = ProductionBrain().run()

        return {
            "production_status": "ACTIVE",
            "result": result
        }


    def auto(self):


        from brain.commander.auto_learning_hook import AutoLearningHook


        return {

            "command":"AUTO",

            "result":
            AutoLearningHook().run()

        }



    def check(self):

        return {

            "command":"CHECK",

            "status":"SYSTEM OK"

        }



    def learn(self):


        from brain.commander.learning_bridge import LearningBridge


        return LearningBridge().learn()



    def evolve(self):


        from brain.commander.evolution_bridge import EvolutionBridge


        return EvolutionBridge().evolve()



if __name__=="__main__":


    command=" ".join(sys.argv[1:])


    print(
        CommandRouter().route(command)
    )


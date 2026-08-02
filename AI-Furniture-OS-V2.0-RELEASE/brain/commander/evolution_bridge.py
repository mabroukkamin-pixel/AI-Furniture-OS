from brain.evolution.evolution_engine import EvolutionEngine


class EvolutionBridge:


    def __init__(self):

        self.engine = EvolutionEngine()



    def evolve(self):

        result = self.engine.evolve()

        return {

            "evolution_status": "ACTIVE",

            "result": result

        }



if __name__ == "__main__":

    print(
        EvolutionBridge().evolve()
    )


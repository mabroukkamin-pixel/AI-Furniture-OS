from brain.world.world_manager import WorldManager


class DecisionEngine:

    def __init__(self, world: WorldManager):
        self.world = world

    def decide_style(self):

        material = self.world.get_world().material.get("name")

        if material == "rattan":

            self.world.update(
                "style",
                {
                    "primary": "bohemian"
                }
            )

            self.world.add_decision(
                {
                    "type": "style",
                    "value": "bohemian"
                }
            )

            self.world.add_trace(
                {
                    "from": "material",
                    "value": "rattan",
                    "reason": "Natural woven material"
                }
            )
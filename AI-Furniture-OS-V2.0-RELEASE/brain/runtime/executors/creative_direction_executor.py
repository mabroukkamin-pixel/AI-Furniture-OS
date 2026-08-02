from brain.runtime.executors.base_executor import BaseExecutor


class CreativeDirectionExecutor(BaseExecutor):

    def execute(self, state):

        print("CREATIVE DIRECTION EXECUTOR")


        dna = state.design_dna

        environment = state.environment

        lighting = state.lighting

        state.creative_direction = {

            "visual_style":
                dna.get(
                    "design_style",
                    ""
                ),


            "mood":
                ", ".join(
                    dna.get(
                        "emotion",
                        []
                    )
                ),


            "goal":
                (
                    "Create a premium Gulf interior "
                    "scene where the furniture product "
                    "is the hero element."
                ),


            "color_direction":
                ", ".join(
                    environment.get(
                        "colors",
                        []
                    )
                ),


            "story":
                (
                    "Blend handcrafted natural material "
                    "with luxury Gulf lifestyle design."
                )

        }


        return state
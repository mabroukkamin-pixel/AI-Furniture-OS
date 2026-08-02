from brain.runtime.executors.base_executor import BaseExecutor


class ActionExecutor(BaseExecutor):

    def execute(self, state):

        print("ACTION EXECUTOR RUNNING")

        action_plan = getattr(
            state,
            "action_plan",
            {}
        )

        actions = action_plan.get(
            "actions",
            []
        )


        for action in actions:

            print(
                "EXECUTING:",
                action
            )


            if action == "generate_prompt":

                self.generate_prompt(
                    state
                )


            elif action == "create_visual":

                self.create_visual(
                    state
                )


            elif action == "save_artifact":

                self.save_artifact(
                    state
                )


        return state



    def generate_prompt(self,state):

        print(
            "PROMPT GENERATION START"
        )

        state.final_prompt = {

            "positive":
            f"""
Luxury furniture advertisement.

Product:
{state.product.get('name')}

Style:
{state.design_dna.get('design_style')}

Scene:
{state.design_dna.get('scene')}

Material:
{state.design_dna.get('material_story')}

Lighting:
{state.design_dna.get('lighting_mood')}

Camera:
{state.design_dna.get('camera_language')}

Premium Gulf Interior.
"""
        }



    def create_visual(self,state):

        print(
            "IMAGE GENERATION READY"
        )

        state.generation = {

            "status":
            "ready",

            "provider":
            "image_generator",

            "input":
            state.final_prompt

        }



    def save_artifact(self,state):

        print(
            "ARTIFACT SAVE REQUEST"
        )

        state.status = "completed"
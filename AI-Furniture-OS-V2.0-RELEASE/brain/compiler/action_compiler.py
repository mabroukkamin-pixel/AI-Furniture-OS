class ActionCompiler:


    def compile(self, state):

        dna = state.design_dna


        plan = {

            "style":
                dna.get(
                    "design_style"
                ),


            "scene":
                dna.get(
                    "scene"
                ),


            "material":
                dna.get(
                    "material_story"
                ),


            "lighting":
                dna.get(
                    "lighting_mood"
                ),


            "camera":
                dna.get(
                    "camera_language"
                ),


            "composition":
                dna.get(
                    "composition"
                ),


            "brand":
                dna.get(
                    "brand_language"
                ),


            "emotion":
                dna.get(
                    "emotion"
                ),


            "actions":[

                "generate_prompt",

                "create_visual",

                "save_artifact"

            ]

        }


        state.execution_plan = plan


        return state
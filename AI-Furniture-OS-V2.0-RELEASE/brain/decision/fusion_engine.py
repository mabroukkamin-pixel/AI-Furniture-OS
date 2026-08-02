class DecisionFusionEngine:


    def fuse(self, state):


        decision = state.decision


        # Existing context

        decision["branding"] = state.branding

        decision["lighting_context"] = state.lighting

        decision["environment"] = state.environment

        decision["camera_context"] = state.camera

        decision["marketing"] = state.marketing



        # ==============================
        # READ BRAIN FUSION RESULT
        # ==============================

        fusion = getattr(
            state,
            "fusion",
            {}
        )


        if fusion:


            decision["primary_style"] = (
                fusion.get(
                    "final_style"
                )
            )


            decision["scene"] = (
                fusion.get(
                    "scene",
                    []
                )
            )


            decision["camera"] = (
                fusion.get(
                    "camera",
                    []
                )
            )


            decision["lighting"] = (
                fusion.get(
                    "lighting",
                    []
                )
            )


            decision["materials"] = (
                fusion.get(
                    "materials",
                    []
                )
            )


            decision["architecture"] = (
                fusion.get(
                    "architecture",
                    {}
                )
            )


            decision["colors"] = (
                fusion.get(
                    "colors",
                    {}
                )
            )


            decision["accessories"] = (
                fusion.get(
                    "accessories",
                    {}
                )
            )


        state.decision = decision


        return state
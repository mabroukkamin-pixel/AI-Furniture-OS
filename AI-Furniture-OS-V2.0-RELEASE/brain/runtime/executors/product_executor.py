from brain.runtime.executors.base_executor import BaseExecutor


class ProductExecutor(BaseExecutor):

    def execute(self, state):

        print("PRODUCT EXECUTOR")

        product = state.product

        if product:

            state.context["product_name"] = product.get(
                "name",
                ""
            )

            state.context["material"] = product.get(
                "material",
                ""
            )

            state.context["brand"] = product.get(
                "brand",
                ""
            )

            state.context["target"] = product.get(
                "target",
                ""
            )

            state.trace.append(
                "ProductExecutor completed"
            )

        return state
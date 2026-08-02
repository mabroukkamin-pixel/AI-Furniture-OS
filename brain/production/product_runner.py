
import os
import json
import datetime

from brain.commander.command_router import CommandRouter


class ProductRunner:


    def __init__(self, product):

        self.product = product


    def run(self):

        result = {

            "product":
            self.product,

            "start":
            str(datetime.datetime.now()),

            "pipeline":
            "STARTED"

        }


        output = CommandRouter().route("AUTO")


        result["brain_result"] = output


        result["status"] = "SUCCESS"


        self.save(result)


        return result



    def save(self,data):

        os.makedirs(
            "docs/reports/products",
            exist_ok=True
        )


        file = (
        "docs/reports/products/"
        + self.product
        + ".json"
        )


        with open(
            file,
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )


if __name__=="__main__":

    import sys

    product = (
        sys.argv[1]
        if len(sys.argv)>1
        else
        "Partition001"
    )


    print(
        ProductRunner(product).run()
    )


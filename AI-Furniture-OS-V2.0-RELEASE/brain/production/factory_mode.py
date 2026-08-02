
import os
import json
import datetime
import subprocess


class AIFOSFactory:


    def __init__(self):

        self.products=[]

        self.report={
            "factory":
            "AI Furniture OS V2",

            "time":
            str(datetime.datetime.now()),

            "runs":[]
        }



    def load_products(self):

        folder="products"


        if not os.path.exists(folder):

            os.makedirs(folder)


        for file in os.listdir(folder):

            if file.endswith(".json"):

                self.products.append(
                    file.replace(".json","")
                )


        if not self.products:

            self.products=[
                "Partition001"
            ]



    def run_product(self,product):

        print("")
        print("======================")
        print(
            "RUN:",
            product
        )
        print("======================")


        result=subprocess.run(

            [
                "python",
                "-m",
                "brain.production.product_runner",
                product
            ],

            capture_output=True,

            text=True

        )


        self.report["runs"].append({

            "product":
            product,

            "status":
            "DONE",

            "output":
            result.stdout[-500:]

        })



    def save(self):

        os.makedirs(
            "docs/reports/factory",
            exist_ok=True
        )


        with open(
            "docs/reports/factory/factory_report.json",
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                self.report,
                f,
                indent=4,
                ensure_ascii=False
            )



    def run(self):

        print(
            "=============================="
        )

        print(
            " AI FURNITURE OS FACTORY MODE "
        )

        print(
            "=============================="
        )


        self.load_products()


        for product in self.products:

            self.run_product(product)



        self.save()


        print("")
        print(
            "FACTORY COMPLETE"
        )

        print(
            "REPORT:"
            " docs/reports/factory/factory_report.json"
        )



if __name__=="__main__":

    AIFOSFactory().run()


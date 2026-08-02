from brain.generators.generator_manager import GeneratorManager



def main():


    manager = GeneratorManager()


    result = manager.generate(

        engine="nano_banana",

        image="products/Partition001/main.jpg",

        prompt="""
Luxury furniture advertising image.
Preserve product exactly.
"""

    )


    print(result)



if __name__ == "__main__":

    main()
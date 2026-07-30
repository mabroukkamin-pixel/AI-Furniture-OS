from brain.generators.generator_manager import GeneratorManager
from brain.prompt.prompt_writer import PromptWriter



def main():


    print("==============================")
    print("AI FURNITURE PRODUCTION")
    print("==============================")


    #
    # هنا مؤقتاً نستخدم Context جاهز
    #
    from test_brain_state import create_context


    context = create_context()


    #
    # Build Prompt
    #

    writer = PromptWriter()

    context = writer.write(context)



    print("==============================")
    print("PROMPT READY")
    print("==============================")


    final_prompt = context.final_prompt["final"]



    #
    # Generate
    #

    generator = GeneratorManager()


    result = generator.generate(

        engine="nano_banana",

        image="products/Partition001/main.jpg",

        prompt=final_prompt

    )


    print("==============================")
    print("RESULT")
    print("==============================")


    print(result)



if __name__ == "__main__":

    main()
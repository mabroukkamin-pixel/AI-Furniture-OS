from brain.prompt_engine.prompt_builder import PromptBuilder


brief = {

"product":
"Partition001",

"concept":
"Luxury Gulf Home Lifestyle",

"style":
"gulf_luxury",

"scene":
[
"luxury_villa",
"beige_stone_wall"
],

"camera":
[
"45_degree",
"lifestyle_shot"
],

"lighting":
[
"golden_hour"
],

"avoid":
[
"product_modification"
]

}


builder = PromptBuilder(brief)


prompt = builder.build()


print("="*50)
print(prompt)
print("="*50)
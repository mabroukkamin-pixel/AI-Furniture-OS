from brain.prompt_engine.prompt_builder import PromptBuilder
from brain.marketing_engine.marketing_engine import MarketingEngine


marketing = MarketingEngine(
    "brain/product_engine/marketing_rules.yaml"
)

marketing_result = marketing.generate(
    "room_divider"
)

print("MARKETING:")
print(marketing_result)


product = {

"product":{
"product":{
"name_ar":"بارتيشن قش",
"category":"room_divider",
"material":"rattan",
"color":"beige_brown",
"dimensions":{
"width":"200 cm",
"height":"180 cm"
}
}
}

}


branding = {

"branding":{
"company":"Chinese Market",
"market":"Kuwait",
"style":[
"premium",
"luxury"
],
"colors":{
"primary":[
"royal_blue",
"gold",
"white"
]
}
}

}


decision = {

"primary_style":"natural",

"style_ranking":[
["natural",10],
["warm_home",10],
["gulf_luxury",10]
],

"scene":[
"luxury_villa",
"beige_stone_wall",
"warm_wood_floor"
],

"camera":[
"45_degree"
],

"lighting":[
"golden_hour"
]

}


prompt = PromptBuilder().build(
    product,
    decision,
    branding,
    marketing_result
)


print(prompt)
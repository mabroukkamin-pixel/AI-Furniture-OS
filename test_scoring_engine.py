from brain.decision_engine.decision_engine import DecisionEngine
from brain.decision_engine.rule_engine import RuleEngine
from brain.decision_engine.scoring_engine import ScoringEngine
from brain.decision_engine.brand_engine import BrandEngine
from brain.reference_engine.reference_metadata import ReferenceMetadata

metadata = ReferenceMetadata(
    "references/partition/reference.yaml"
)

data = metadata.load()

rules = RuleEngine(
    "brain/decision_engine/rules.yaml"
)

scoring = ScoringEngine(
    "brain/decision_engine/weights.yaml"
)

engine = DecisionEngine(
    data,
    rules,
    scoring
)

result = engine.decide()

# تهيئة محرك العلامة التجارية وعمليات الوزن والأوزان الخاصة بالسوق
brand = BrandEngine(
    "brain/decision_engine/brand_weights.yaml"
)

# تحويل القائمة إلى قاموس (Dictionary) لتسهيل إضافة وتعديل النقاط
style_ranking_dict = dict(result.get("style_ranking", {}))

# تطبيق أوزان ونقاط البراند على التصنيفات
result_scores = brand.apply(
    style_ranking_dict
)

print("="*50)
print("Result Scores with Brand Weights:")
print(result_scores)
print("="*50)
print(result)
print("="*50)
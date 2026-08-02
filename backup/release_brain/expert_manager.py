from brain.registry import get_experts, clear
import brain.load_experts
from brain.experts.product_expert import ProductExpert  # تأكد من استيراد الكلاس إن لزم الأمر


class ExpertManager:

    def __init__(self, product_name):
        self.product_name = product_name

    def build(self):

        clear()

        brain.load_experts.load()

        # استرجاع الخبراء المسجلين، مع تحديث أو إضافة ProductExpert بالمسار الجديد
        experts = get_experts()
        
        # إذا كنت تريد التأكد من حقن مسار المنتج مباشرة في الـ ProductExpert عند البناء:
        configured_experts = []
        for expert in experts:
            if isinstance(expert, ProductExpert):
                # إذا كان يدعم تهيئة المسار أو يتم استبداله بالنسخة المخصصة
                configured_experts.append(
                    ProductExpert(f"products/{self.product_name}")
                )
            else:
                configured_experts.append(expert)

        return configured_experts
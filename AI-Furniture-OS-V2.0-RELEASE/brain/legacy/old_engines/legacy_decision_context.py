class DecisionContext:
    def __init__(self, product=None):
        self.product = product
        self.material = None
        self.lighting = None
        self.environment = None
        self.photography = None
        
        # إضافة قاموس لتخزين أي بيانات إضافية مرنة ديناميكياً
        self.metadata = {}
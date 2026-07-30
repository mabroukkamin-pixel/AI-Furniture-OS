class AdGenerator:


    def __init__(
        self,
        product,
        decision,
        branding
    ):

        self.product = product
        self.decision = decision
        self.branding = branding



    def generate(self):

        product_data = (
            self.product
            .get("product", {})
            .get("product", {})
        )


        brand_data = (
            self.branding
            .get("branding", {})
        )


        return {

            "instagram":

                self.instagram_caption(
                    product_data,
                    brand_data
                ),


            "facebook":

                self.facebook_ad(
                    product_data,
                    brand_data
                ),


            "hashtags":

                self.hashtags()

        }



    def instagram_caption(
        self,
        product,
        brand
    ):

        return f"""

✨ {product.get('name_ar')}

أضف لمسة من الفخامة والدفء إلى منزلك 🤍

تصميم أنيق بخامة طبيعية يعطي المكان إحساسًا بالراحة والرقي.

📏 المقاس:
{product.get('dimensions')}

💰 السعر:
{product.get('price')}

🚚 توصيل سريع لجميع المناطق

{brand.get('arabic')}

        """



    def facebook_ad(
        self,
        product,
        brand
    ):

        return f"""

اكتشف جمال التفاصيل مع {product.get('name_ar')}

قطعة ديكور تجمع بين:
- التصميم الراقي
- الخامة الطبيعية
- الاستخدام العملي

السعر:
{product.get('price')}

اطلب الآن من {brand.get('company')}

        """



    def hashtags(self):

        return [

            "#السوق_الصيني",

            "#أثاث_كويتي",

            "#ديكور_منزل",

            "#بيت_كويتي",

            "#ديكور_فاخر"

        ]
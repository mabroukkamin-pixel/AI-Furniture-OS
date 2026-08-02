class RequestBuilder:

    def build(self, brain):

        return {

            "product_id":
                brain.product["id"],

            "prompt":
                brain.prompt["final"],

            "image":
                brain.product_image,

            "branding":
                brain.branding,

            "decision":
                brain.decision,

            "marketing":
                brain.marketing

        }
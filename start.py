import sys

from automation.product_scanner import ProductScanner
from automation.batch_runner import BatchRunner
from automation.job_manager import JobManager



def main():

    print("=" * 60)
    print("        AI FURNITURE OS AUTOMATION")
    print("=" * 60)


    scanner = ProductScanner()

    runner = BatchRunner()

    jobs = JobManager()



    # تشغيل منتج محدد
    if len(sys.argv) > 1:

        product = sys.argv[1]

        job = jobs.start(product)


        runner.run_product(
            product
        )


        jobs.finish(job)


    # تشغيل كل المنتجات
    else:

        products = scanner.scan()


        print()
        print("DETECTED PRODUCTS")
        print("-" * 30)


        for product in products:
            print(product)


        print()


        for product in products:

            job = jobs.start(product)


            runner.run_product(
                product
            )


            jobs.finish(job)



if __name__ == "__main__":
    main()
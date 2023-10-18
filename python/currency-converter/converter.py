from converter.App import App
import sys
import os


if os.getenv('ACCESS_KEY') is None:
    print("Please set your AccessKey environment variable")
    sys.exit(1)
app = App(sys.argv)
print(app.get_result_equation())

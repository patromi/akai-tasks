from converter.App import App
import sys
import os


if os.getenv('ACCESS_KEY') is None:
    print("Please set your AccessKey environment variable")
    sys.exit(1)

if len(sys.argv) != 4:
    print("Please provide arguments")
    sys.exit(1)

app = App(sys.argv)
print(app.get_result_equation())

from TestCase import *
import os

def execute_script(path, command):
    os.system("python {}".format(os.path.join(path, command)))
    print("%s is completed ."%command)

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    input_data=input("Input your number :")
    if input_data == "1":
        execute_script(path, "test_common.py")
    elif input_data=="2":
        execute_script(path,"test_crawel.py")
    elif input_data=="3":
        execute_script(path, "test_tamper.py")
    elif input_data=="4":
        execute_script(path, "test_yara.py")
    elif input_data=="5":
        execute_script(path, "test_crawel.py")
        execute_script(path, "test_tamper.py")
    elif input_data=="6":
        execute_script(path, "test.py")
    elif input_data=="7":
        execute_script(path, "send_data.py")
    else:
        pass
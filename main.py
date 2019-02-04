from core.runner import Runner
import os

if __name__ == "__main__": 
    login, password = os.environ.get('LOGIN'), os.environ.get('PASSWORD')
    print("LOG: {}\tPASS: {}".format(login, password))

    runner = Runner(login, password)

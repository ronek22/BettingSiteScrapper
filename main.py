from core.runner import Runner

if __name__ == "__main__":
    with open('client.secret', 'r') as f:
        login, password = f.readline().split()

    runner = Runner(login, password)

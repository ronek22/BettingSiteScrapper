from core.fortuna import Fortuna


if __name__ == "__main__":
    site = Fortuna()
    site.login()
    site.get_history()

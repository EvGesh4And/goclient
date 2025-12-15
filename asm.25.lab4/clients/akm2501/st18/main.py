if __name__ == '__main__':
    from application import main as application_main
else:
    from .application import main as application_main


def main():
    application_main()


if __name__ == '__main__':
    main()
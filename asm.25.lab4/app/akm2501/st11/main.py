import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import App
from group import group

if __name__ == "__main__":
    print(group().f())
    application = App(__name__)
    application.run()
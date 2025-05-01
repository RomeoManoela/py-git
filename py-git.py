import sys
from core.init import init

command = sys.argv[1]
if command == "init":
    init()

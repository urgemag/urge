from os import listdir, rename, mkdir, system
from os.path import isfile, join
onlyfiles = [f for f in listdir() if isfile(join(f))]

for i in onlyfiles:
    if i == "script.py":
        continue
    name_min = i.split(".")
    name_min.insert(-1,"min")
    name_min = (".".join(name_min))
    system(f"minify -o '{name_min}' '{i}'")

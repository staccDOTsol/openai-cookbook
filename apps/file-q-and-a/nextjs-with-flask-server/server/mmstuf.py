import glob 
import os
from shutil import copyfile
i = 0
with open ('mom.json', 'a+') as f2:
    for file in glob.glob("/home/st/Downloads/messages/*/*/*.json"):
        i = i + 1
        print(file)
        copyfile    (file, '/home/st/' + str(i)+".txt")
from glob import glob 
# spawn a subprocess
# import Popen 
from subprocess import Popen, PIPE
from threading import Thread
from os import spawnv
i = -1

def print_pipe(type_pipe,pipe):
    for line in iter(pipe.readline, ''):
         print( "[%s] %s"%(type_pipe,line))
for file in glob("/home/st/Downloads/*/*.epub"):
    i = i + 1
   
    print("python3.8 -m epub2txt -f \""+file+"\" -d "+str(i)+".txt")
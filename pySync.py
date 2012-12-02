#!/usr/bin/python

import sys, shutil, os, time, configparser
from os.path import *

if os.name == 'nt':
    #msvcrt can't function correctly in IDLE
    if 'idlelib.run' in sys.modules:
        print("Please don't run this script in IDLE.")
        sys.exit(0)
    import msvcrt
    def flush_input(str):
        while msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch == '\xff':
                print("msvcrt is broken, this is weird.")
                sys.exit(0)
        return input(str)
else:
    import select
    def flush_input(str):
        while len(select.select([sys.stdin.fileno()], [], [], 0.0)[0])>0:
            os.read(sys.stdin.fileno(), 4096)
        return input(str)
        
def compare(fa,fb):
    if isfile(fa)==isfile(fb):
        if isdir(fa):
            walktree(fa,fb)
        elif isfile(fa):
            if getsize(fa)!=getsize(fb) or int(getmtime(fa))!=int(getmtime(fb)):
                print(fa,': size=',getsize(fa),'mtime=',time.asctime(time.localtime(getmtime(fa))))
                print(fb,': size=',getsize(fb),'mtime=',time.asctime(time.localtime(getmtime(fb))))
                if getmtime(fa)>getmtime(fb):
                    act='>'
                else:
                    act='<'
                s = flush_input('What to do?(>,<,n)['+act+']')
                if len(s)>0:
                    act=s[0]
                if act=='>':
                    shutil.copy2(fa,fb)
                elif act=='<':
                    shutil.copy2(fb,fa)
        else:
            print('Comp: Skipping',fa)
    else:
        print('Error:',fa,',',fb,'have different protection bit')

def copy(fa,fb):
    s = flush_input('Copy '+fa+' to another side?(r,y,n)[y]')
    if len(s)>0:
        act=s[0]
    else:
        act='y'
    if act =='y':
        if isdir(fa):
            shutil.copytree(fa,fb)
        elif isfile(fa):
            shutil.copy2(fa,fb)
        else:
            print('DirCopy: Skipping ',fa)
    elif act =='r':
        if isdir(fa):
            shutil.rmtree(fa)
        elif isfile(fa):
            os.remove(fa)
        else:
            print('FileCopy: Skipping ',fa)

def walktree(source,target):
    srclist = os.listdir(source)
    tarlist = os.listdir(target)
    for f in srclist:
        if f in tarlist:
            del tarlist[tarlist.index(f)]
            compare(join(source,f),join(target,f))
        else:
            copy(join(source,f),join(target,f))
    for f in tarlist:
        copy(join(target,f),join(source,f))

if __name__ == '__main__':
    stoconf = configparser.RawConfigParser()
    tarconf = configparser.RawConfigParser()
    stoconf.read("pySync.ini")
    tarconf.read(expanduser("~/.pysync"))
    stoname = stoconf.sections()[0]
    tarname = tarconf.sections()[0]
    if stoconf.has_option(stoname,'BASE'):
        stobase=abspath(stoconf.get(stoname,'BASE'))
        stoconf.remove_option(stoname,'BASE')
    else: stobase=os.getcwd()
    if tarconf.has_option(tarname,'BASE'):
        tarbase=abspath(tarconf.get(tarname,'BASE'))
        tarconf.remove_option(tarname,'BASE')
    else: tarbase=expanduser('~/')
    print("Syncing between",stoname,"and",tarname)
    for folder in tarconf.options(tarname):
        if stoconf.has_option(stoname,folder):
            print('Processing',folder)
            walktree(join(stobase,stoconf.get(stoname,folder)),join(tarbase,tarconf.get(tarname,folder)))
    print("Done.")

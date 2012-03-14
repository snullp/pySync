#!/usr/bin/python

import sys, shutil, os, time
from os.path import getsize,getmtime 

deffolder=['Download','Big music','Books','CS&IT','ENGstudy','Image Collection','My photos','My Pictures','Soft','Video collection','Workshop']

def compare(fa,fb):
    if os.path.isfile(fa)==os.path.isfile(fb):
        if os.path.isdir(fa):
            walktree(fa,fb)
        elif os.path.isfile(fa):
            if getsize(fa)!=getsize(fb) or int(getmtime(fa))!=int(getmtime(fb)):
                print(fa,': size=',getsize(fa),'mtime=',time.asctime(time.localtime(getmtime(fa))))
                print(fb,': size=',getsize(fb),'mtime=',time.asctime(time.localtime(getmtime(fb))))
                if getmtime(fa)>getmtime(fb):
                    act='>'
                else:
                    act='<'
                s = input('What to do?(>,<,n)['+act+']')
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
    s = input('Copy '+fa+' to another side?(r,y,n)[y]')
    if len(s)>0:
        act=s[0]
    else:
        act='y'
    if act =='y':
        if os.path.isdir(fa):
            shutil.copytree(fa,fb)
        elif os.path.isfile(fa):
            shutil.copy2(fa,fb)
        else:
            print('DirCopy: Skipping ',fa)
    elif act =='r':
        if os.path.isdir(fa):
            shutil.rmtree(fa)
        elif os.path.isfile(fa):
            os.remove(fa)
        else:
            print('FileCopy: Skipping ',fa)

def walktree(source,target):
    srclist = os.listdir(source)
    tarlist = os.listdir(target)
    for f in srclist:
        if f in tarlist:
            del tarlist[tarlist.index(f)]
            compare(os.path.join(source,f),os.path.join(target,f))
        else:
            copy(os.path.join(source,f),os.path.join(target,f))
    for f in tarlist:
        copy(os.path.join(target,f),os.path.join(source,f))


if __name__ == '__main__':
    if len(sys.argv)==3:
        walktree(sys.argv[1],sys.argv[2])
    elif len(sys.argv)==2:
        walktree('/media/STORE/'+sys.argv[1],'/media/NULL\'s Data Center/'+sys.argv[1])
    else:
        for t in deffolder:
            walktree('/media/STORE/'+t,'/media/NULL\'s Data Center/'+t)

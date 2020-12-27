import json

def getJson(path):
    with open(path,'r',encoding='utf-8') as f:
        d=json.load(f)
    return d

def dumpJson(obj,path):
    with open(path,'w+',encoding='utf-8') as f:
        json.dump(obj,f)

def readTriple(path,sep=None,cod='utf-8'):
    with open(path,'r',encoding=cod) as f:
        for line in f.readlines():
            if sep:
                lines = line.strip().split(sep)
            else:
                lines=line.strip().split()
            if len(lines)!=3:continue
            yield lines

def readFile(path,sep=None,cod='utf-8'):
    with open(path,'r',encoding=cod) as f:
        for line in f.readlines():
            if sep:
                lines = line.strip().split(sep)
            else:
                lines = line.strip().split()
            if len(lines)==0:continue
            yield lines

def writeTripleLine(h,r,t,f):
    f.write(str(h)+'\t'+str(r)+'\t'+str(t)+'\n')

def writeDoubleLine(h,t,f):
    f.write(str(h)+'\t'+str(t)+'\n')

def writeSinalLine(r,f):
    f.write(str(r)+'\n')
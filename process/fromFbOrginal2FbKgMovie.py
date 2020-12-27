__author__ = 'yfr'

import gzip
import re
from tqdm import tqdm
from data_set import filePaths as fp
from utils import osUtils
#in
FBorginal=fp.FBOrginal.RDF

#out
FBMoives=fp.FBMovie.movies_tsv
Names = fp.FBMovie.names_tsv


def scanFreebaseMovies():
    print('scanfreebase')
    fb=gzip.GzipFile(FBorginal,"r")

    with open(FBMoives,'w+') as f:
        for line in tqdm(fb):
            lines = line.decode('utf-8').strip().split("\t")
            head=re.findall('/m\.(.*)>', lines[0])
            if len(head) == 0:continue
            tail=re.findall('/m\.(.*)>', lines[2])
            if len(tail) == 0:continue
            relation=re.findall('<http://rdf\.freebase\.com/ns/film\.(.*)>',lines[1])
            if len(relation) == 0:continue
            head='m.' + head[0]
            tail='m.' + tail[0]
            f.write(head+'\t'+relation[0]+'\t'+tail+'\n')
    fb.close()

def scan_entity_propertits():
    allEntitys=set()
    for h, r, t in tqdm(osUtils.readTriple(FBMoives)):
        allEntitys.add(h)
        allEntitys.add(t)

    fb = gzip.GzipFile(FBorginal, "r")
    with open(Names,'w+',encoding='utf-8') as f:
        for line in tqdm(fb):
            lines = line.decode('utf-8').strip().split("\t")
            relation = re.findall('<http://rdf\.freebase\.com/ns/type\.object\.(.*)>', lines[1])
            if len(relation)==0:continue
            relation = relation[0]
            if relation!='name':continue
            head = re.findall('/m\.(.*)>', lines[0])
            if len(head) == 0: continue
            head = 'm.' + head[0]
            if head not in allEntitys:continue
            f.write(head+'\t'+relation+'\t'+lines[2]+'\n')
    fb.close()

if __name__=='__main__':
    scanFreebaseMovies()
    scan_entity_propertits()
__author__ = 'yfr'

from tqdm import tqdm
from utils import osUtils
from data_set import filePaths as fp

MoviePathDict=fp.MovieLensDatas.pathsDict

#in
ALL_relations_chose=fp.FBEasyMovies.all_relations_chose
ALL_link_file=fp.FBEasyMovies.ml2fb_links
ALL_names=fp.FBEasyMovies.names_tsv
ALL_types=fp.FBEasyMovies.types_tsv
FB_movies=fp.FBEasyMovies.movies_tsv
Easy_movie_json=MoviePathDict['easy-rec']['movieids_json']

#out
E_names=MoviePathDict[fp.RecData.FbKg]['names']
E_types=MoviePathDict[fp.RecData.FbKg]['types']
Kg_tsv=MoviePathDict[fp.RecData.FbKg]['kg']
Link_json=MoviePathDict[fp.RecData.FbKg]['ml2fb_link']
Pairs_count=MoviePathDict[fp.RecData.FbKg]['count']

def scanMovies():
    print('scan_movie')
    all_links,inner_links={},{}
    for h,t in osUtils.readFile(ALL_link_file):
        all_links[h]=t
    mids=osUtils.getJson(Easy_movie_json)
    for mid in tqdm(mids):
        if mid not in all_links: continue
        fb_id = all_links[mid]
        inner_links[mid]=fb_id
    osUtils.dumpJson(inner_links,Link_json)

def getKgfile():
    print('scan_kg')
    relations_chose={r[0] for r in osUtils.readFile(ALL_relations_chose)}

    freebase_movies = set(osUtils.getJson(Link_json).values())
    with open(Kg_tsv,'w+') as f:
        for h,r,t in tqdm(osUtils.readTriple(FB_movies)):
            if r not in relations_chose:continue
            if (h in freebase_movies) or (t in freebase_movies):
                osUtils.writeTripleLine(h,r,t,f)

def scanEntitys():
    print('write_entitys')
    a_names,a_types,e_names,e_types={},{},{},{}
    entitys=set()
    for h,n in osUtils.readFile(ALL_names):
        a_names[h]=n
    for h,t in osUtils.readFile(ALL_types):
        a_types[h]=t
    for h,r,t in tqdm(osUtils.readTriple(Kg_tsv)):
        entitys.add(h)
        entitys.add(t)
    name_file=open(E_names,'w+',encoding='utf-8')
    type_file=open(E_types,'w+',encoding='utf-8')

    for e in tqdm(entitys):
        name=a_names.get(e,None)
        if name:
            name_file.write(e+'\t'+name+'\n')
        type=a_types.get(e,None)
        if type:
            type_file.write(e+'\t'+type+'\n')

def getFBKgFiles():
    scanMovies()
    getKgfile()
    scanEntitys()


def getPairsCount():
    from process import fromFbMovie2easy
    fromFbMovie2easy.getPairsCount(Kg_tsv,Pairs_count)

if __name__ == '__main__':
    getFBKgFiles()
    getPairsCount()
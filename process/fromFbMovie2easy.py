__author__ = 'yfr'
import re
from data_set import filePaths as fp
from utils import osUtils
from tqdm import tqdm
import collections
#in
FB_movies_tsv=fp.FBMovie.movies_tsv
FB_movies_name=fp.FBMovie.names_tsv
#out
FB_movie_paris_count_tsv=fp.FBMovie.paris_count_tsv
e_movies_tsv=fp.FBEasyMovies.movies_tsv
e_names_tsv=fp.FBEasyMovies.names_tsv
e_types_tsv=fp.FBEasyMovies.types_tsv
paris_count_tsv=fp.FBEasyMovies.paris_count_tsv
all_relations_tsv=fp.FBEasyMovies.all_relations
all_relations_tsv_chose=fp.FBEasyMovies.all_relations_chose


def __getOnlyEnNames():
    entitys=set()
    en_names=[]
    for h,r,t in osUtils.readTriple(FB_movies_name):
        if '@en' in t:
            if h in entitys:continue
            name = re.findall('"(.*)"@en', t)
            name = name[0]
            en_names.append((h,name))
            entitys.add(h)
    return en_names

def __getOtherNames():
    en_entitys = set()
    for h, r, t in tqdm(osUtils.readTriple(FB_movies_name)):
        if '@en' in t:
            en_entitys.add(h)

    other_entitys=[]
    for h,r,t in tqdm(osUtils.readTriple(FB_movies_name)):
        if '@en' in t:continue
        if h in en_entitys:continue
        other_entitys.append((h,t))
    return other_entitys

def __getOtherNameOlnyOne():

    lanPropty=['zh','zh-Hant','ja','ko']
    entitysWithNames=collections.defaultdict(dict)

    def writeName(other_names_only_one,h):
        for lang in lanPropty:
            if lang in entitysWithNames[h]:
                other_names_only_one.append((h,entitysWithNames[h][lang]))
                return
        else:
            for lang in entitysWithNames[h]:
                other_names_only_one.append((h, entitysWithNames[h][lang]))
                return

    for h,t in tqdm(__getOtherNames()):
        lang=re.findall('"@(.*)',t)
        lang=lang[0]
        regexstr='"(.*)"@{}'.format(lang)
        name = re.findall(regexstr, t)
        name = name[0]
        entitysWithNames[h][lang]=name

    other_names_only_one=[]
    for h in entitysWithNames:
        writeName(other_names_only_one,h)
    return other_names_only_one


def getNames():
    print('get names')
    with open(e_names_tsv,'w+',encoding='utf-8') as f:
        for h,t in __getOtherNameOlnyOne():
            f.write(h+'\t'+t+'\n')
        for h,t in __getOnlyEnNames():
            f.write(h+'\t'+t+'\n')



def __getDeleteRelations():
    deleteRelations=set()
    for line in osUtils.readFile(FB_movie_paris_count_tsv):
        if int(line[2])<20000:
            deleteRelations.add(line[0])
    return deleteRelations

def __getDeletionMovies():
    deletes=__getDeleteRelations()
    movies_without_delete_relation=[]
    for h,r,t in tqdm(osUtils.readTriple(FB_movies_tsv)):
        if r in deletes:continue
        if r == 'film_regional_release_date.film_regional_debut_venue':continue
        movies_without_delete_relation.append((h,r,t))
    return movies_without_delete_relation

def __getEntityWithOutType(entity_type_2nd,movies_without_delete_relation):

    e2d = __get2ndEJson(entity_type_2nd,movies_without_delete_relation)
    e2dwithOutType=dict()
    e2s = set()
    for r in e2d:
        for entity in e2d[r]:
            e2s.add(entity)
            e2dwithOutType[entity]=e2d[r][entity]
    return e2dwithOutType

def __getEntitysTypes(movies_without_delete_relation):
    entitys=dict()
    for h, r, t in tqdm(movies_without_delete_relation):
        types=re.findall('(.*)\.',r)
        entitys[h]=types[0]
    return entitys



def __get2ndEJson(entity_type_2nd,movies_without_delete_relation):
    e2nds=entity_type_2nd
    e2ndsDict={k:dict() for k in e2nds}
    for h,r,t in tqdm(movies_without_delete_relation):
        types = re.findall('(.*)\.', r)
        ttt=types[0]
        if ttt in e2nds:
            r = r.replace(ttt, '')
            r = r.replace('.', '')
            if r == 'film':continue
            if h not in e2ndsDict[ttt]:
                e2ndsDict[ttt][h]=dict()
            e2ndsDict[ttt][h][r]=t
    return e2ndsDict


def __getPairRelation(movies_without_delete_relation):
    entitys=__getEntitysTypes(movies_without_delete_relation)
    pairs= {}
    only_paris={}
    for h, r, t in tqdm(movies_without_delete_relation):
        if h in entitys and t in entitys:
            pair = (entitys[h],r,entitys[t])
            if pair in pairs:
                pairs[pair]+=1
            else:
                pairs[pair]=1
            only_pair = (entitys[h],entitys[t])
            if only_pair in only_paris:
                only_paris[only_pair]+=1
            else:
                only_paris[only_pair]=1
    return only_paris


def __getParis(movies_without_delete_relation):
    pairs=__getPairRelation(movies_without_delete_relation)
    np=dict()
    for p in pairs:
        if pairs[p]>20000:
            np[p]=pairs[p]
    return np


def __getOnlyPairWithoutFilms(movies_without_delete_relation):
    onlyPairWithOutFilms=[]
    for h,t in __getParis(movies_without_delete_relation):
        if h=='film':continue
        onlyPairWithOutFilms.append((h,t))
    return onlyPairWithOutFilms

def __getEntityType2nd(movies_without_delete_relation):
    entitys=collections.defaultdict(set)
    for h, t in __getOnlyPairWithoutFilms(movies_without_delete_relation):
        entitys[h].add(t)

    ENTITY_TYPE_2ND=set()
    for e in entitys:
        hasF,hasO=False,False
        for r in entitys[e]:
            if 'film'==r:
                hasF=True
            else:
                hasO=True
        if hasO and hasF:
            if e!='actor':
                ENTITY_TYPE_2ND.add(e)
                print(e)
    return ENTITY_TYPE_2ND

def __getAlle2ndRelativeRelation(entity_type_2nd,movies_without_delete_relation):
    e2nds = entity_type_2nd
    e2types = __getEntitysTypes(movies_without_delete_relation)

    fb_movies_without_2nd=[]
    for h,r,t in tqdm(movies_without_delete_relation):
        if e2types.get(h,h) in e2nds or e2types.get(t,t) in e2nds:continue
        fb_movies_without_2nd.append((h,r,t))
    return fb_movies_without_2nd

def __getMovieLinks(entity_type_2nd,movies_without_delete_relation):
    e2d=__getEntityWithOutType(entity_type_2nd,movies_without_delete_relation)
    movieLinks=dict()
    for h,r,t in tqdm(movies_without_delete_relation):
        types = re.findall('(.*)\.', r)
        ttt = types[0]
        if ttt=='film':
            if t in e2d:
                if h not in movieLinks:
                    movieLinks[h]=dict()
                for rrr in e2d[t]:
                    if rrr=='films':continue
                    if rrr not in movieLinks[h]:
                        movieLinks[h][rrr]=[]
                    movieLinks[h][rrr].append(e2d[t][rrr])
    return movieLinks


def writeEasyMovies():
    print('write easy movies')
    movies_without_delete_relation=__getDeletionMovies()
    entity_type_2nd = __getEntityType2nd(movies_without_delete_relation)
    movieLinks=__getMovieLinks(entity_type_2nd,movies_without_delete_relation)
    lines=[]
    for movie in tqdm(movieLinks):
        for r in movieLinks[movie]:
            movieR="film.{}".format(r)
            tailR="{}.film".format(r)
            for e in movieLinks[movie][r]:
                lines.append((movie,movieR,e))
                lines.append((e,tailR,movie))


    for h,r,t in tqdm(__getAlle2ndRelativeRelation(entity_type_2nd,movies_without_delete_relation)):
        lines.append((h,r,t))

    relationsCounts=__getRelationsCounts(lines)

    delteRelations=set()
    for r in relationsCounts:
        if relationsCounts[r]['count']<1000:
            delteRelations.add(r)
    with open(e_movies_tsv,'w+') as f:
        for h,r,t in tqdm(lines):
            if r in delteRelations:continue
            osUtils.writeTripleLine(h,r,t,f)


def __getRelationsCounts(kg_lints):
    relations=dict()
    for h, r, t in tqdm(kg_lints):
        if r not in relations:
            relations[r] = {'count': 0, 'h': set(), 't': set()}
        relations[r]['count'] += 1
        relations[r]['h'].add(h)
        relations[r]['t'].add(t)

    rr={}
    for r in relations:
        rr[r]={'count':relations[r]['count'],'h':len(relations[r]['h']),'t':len(relations[r]['t'])}
    return rr

def getPairsCount(kg_file=e_movies_tsv,count_file=paris_count_tsv):
    print('get pairs count')
    relations0=dict()
    for h, r, t in tqdm(osUtils.readTriple(kg_file)):
        if r not in relations0:
            relations0[r] = {'count': 0, 'h': set(), 't': set()}
        relations0[r]['count'] += 1
        relations0[r]['h'].add(h)
        relations0[r]['t'].add(t)

    relations = {}
    for r in relations0:
        relations[r] = {'count': relations0[r]['count'], 'h': len(relations0[r]['h']), 't': len(relations0[r]['t'])}

    writed_relations=set()
    with open(count_file,'w+',encoding='utf-8') as f:
        for r1 in relations:
            if r1 in writed_relations:continue
            for r2 in relations:
                if r1 in writed_relations:continue
                if r2 in writed_relations:continue
                if r1==r2:continue
                if relations[r1]['count']==relations[r2]['count']:
                    f.write(r1 + '\tcount\t' + str(relations[r1]['count']) + '\th\t' + str(relations[r1]['h']) + '\tt\t' + str(relations[r1]['t']) + '\n')
                    f.write(r2 + '\tcount\t' + str(relations[r2]['count']) + '\th\t' + str(relations[r2]['h']) + '\tt\t' + str(relations[r2]['t']) + '\n')
                    writed_relations.add(r1)
                    writed_relations.add(r2)
        for r in relations:
            if r in writed_relations:continue
            f.write(r+'\tcount\t'+str(relations[r]['count'])+'\th\t'+str(relations[r]['h'])+'\tt\t'+str(relations[r]['t'])+'\n')

def getAllRelations():
    print('get all relations')
    with open(all_relations_tsv, 'w+') as f:
        for line in osUtils.readFile(paris_count_tsv):
            osUtils.writeSinalLine(line[0],f)
    with open(all_relations_tsv_chose, 'w+') as f:
        for line in osUtils.readFile(paris_count_tsv):
            osUtils.writeSinalLine(line[0],f)



def getTypes():
    print('getTypes')
    entitys = dict()
    for h,r,t in tqdm(osUtils.readTriple(e_movies_tsv)):
        types = re.findall('(.*)\.', r)
        tail_type = re.findall('\.(.*)',r)
        entitys[h] = types[0]
        entitys[t] = tail_type[0]

    with open(e_types_tsv, 'w+', encoding='utf-8') as f:
        for e in entitys:
            f.write(e + '\t' + entitys[e] + '\n')


if __name__=='__main__':
    getPairsCount(FB_movies_tsv,FB_movie_paris_count_tsv)

    writeEasyMovies()

    getPairsCount()
    getAllRelations()

    getNames()
    getTypes()
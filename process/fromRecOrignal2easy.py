__author__ = 'yfr'

from data_set import filePaths as fp
from utils import osUtils
from tqdm import tqdm

MoviePathDict=fp.MovieLensDatas.pathsDict

#in
Orginal_rating_path=MoviePathDict['orginal']['ratings']
Orginal_movie_path=MoviePathDict['orginal']['movies']
#out
Easy_rating_path=MoviePathDict['easy-rec']['ratings']
Easy_movie_json=MoviePathDict['easy-rec']['movieids_json']

def getEasyRec():
    encoding='ISO-8859-1'
    sep=None
    if fp.ROOT_DIR_NAME=='ml-1m':
        sep='::'
    elif fp.ROOT_DIR_NAME=='ml-latest-small':
        sep=','

    count=0
    with open(Easy_rating_path,'w+',encoding='utf-8') as f:
        for uid,iid,rating,_ in tqdm(osUtils.readFile(Orginal_rating_path,sep,encoding)):
            if fp.ROOT_DIR_NAME=='ml-latest-small' and count==0:
                count+=1
                continue
            osUtils.writeTripleLine(int(uid),int(iid),int(float(rating)),f)

    if fp.ROOT_DIR_NAME=='ml-100k':
        sep='|'
    moiveids=[]
    for line in tqdm(osUtils.readFile(Orginal_movie_path,sep,encoding)):
        if fp.ROOT_DIR_NAME=='ml-latest-small' and count==0:
                count+=1
                continue
        moiveids.append(line[0])
    osUtils.dumpJson(moiveids,Easy_movie_json)

if __name__ == '__main__':
    getEasyRec()
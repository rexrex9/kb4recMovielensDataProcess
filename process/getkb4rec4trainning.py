__author__ = 'yfr'

from utils import osUtils
from tqdm import tqdm
from data_set import filePaths as fp

MoviePathDict=fp.MovieLensDatas.pathsDict

# in
Kg_tsv=MoviePathDict[fp.RecData.FbKg]['kg']
Link_json=MoviePathDict[fp.RecData.FbKg]['ml2fb_link']
Easy_rating_path=MoviePathDict['easy-rec']['ratings']

# out
Kg_index = MoviePathDict[fp.RecData.Trainning]['kg_index']
Rating_index = MoviePathDict[fp.RecData.Trainning]['rating_index']

Eid2index_json = MoviePathDict[fp.RecData.TrainningLink]['eid2index']
Rid2index_json = MoviePathDict[fp.RecData.TrainningLink]['rid2index']
Uid2index_json = MoviePathDict[fp.RecData.TrainningLink]['uid2index']


def getMid2EidDict():
    mid2EidDict = osUtils.getJson(Link_json)
    eid2midDict = {mid2EidDict[k]: k for k in mid2EidDict}
    return mid2EidDict, eid2midDict


def dealKg():
    mid2EidDict, eid2midDict = getMid2EidDict()
    eSet, rSet = set(), set()
    triples = []
    eid2eindex, rid2rindex = dict(), dict()
    for h, r, t in tqdm(osUtils.readTriple(Kg_tsv)):
        h = eid2midDict.get(h, h)
        t = eid2midDict.get(t, t)
        triple = (h, r, t)
        triples.append(triple)
        eSet.add(h)
        eSet.add(t)
        rSet.add(r)
    n_movie = 0
    all_items = set()

    for e in eSet:
        if e.isnumeric():
            eid2eindex[e] = n_movie
            all_items.add(n_movie)
            n_movie += 1

    for e in eSet:
        if not e.isnumeric():
            eid2eindex[e] = n_movie
            n_movie += 1

    r_index = 0
    for r in rSet:
        rid2rindex[r] = r_index
        r_index += 1

    osUtils.dumpJson(eid2eindex, Eid2index_json)
    osUtils.dumpJson(rid2rindex, Rid2index_json)

    with open(Kg_index, 'w+') as f:
        for triple in triples:
            f.write('\t'.join([str(eid2eindex[triple[0]]), str(rid2rindex[triple[1]]), str(eid2eindex[triple[2]])]))
            f.write('\n')

def dealRatings():
    user_history_items = dict()
    user_history_items_with_neg = dict()

    eid2index = osUtils.getJson(Eid2index_json)
    uid2index = dict()
    fw = open(Rating_index, 'w+')
    with open(Easy_rating_path) as f:
        for line in tqdm(f.readlines()):
            lines = line.strip().split()
            eid = lines[1]
            if eid not in eid2index: continue
            uid = lines[0]
            innerUid = int(uid) - 1
            innerIid = eid2index[eid]
            rating = 1 if int(lines[2]) >= 4 else 0
            fw.write('\t'.join([str(innerUid), str(innerIid), str(rating)]))
            fw.write('\n')
            uid2index[uid] = innerUid
            if str(innerUid) in user_history_items_with_neg:
                user_history_items_with_neg[str(innerUid)].append(innerIid)
            else:
                user_history_items_with_neg[str(innerUid)] = [innerIid]

            if rating == 1:
                if str(innerUid) in user_history_items:
                    user_history_items[str(innerUid)].append(innerIid)
                else:
                    user_history_items[str(innerUid)] = [innerIid]
    fw.close()

    osUtils.dumpJson(uid2index, Uid2index_json)


def deal():
    print('deal trainning kg')
    dealKg()
    print('deal trainning rating')
    dealRatings()

if __name__ == '__main__':
    deal()
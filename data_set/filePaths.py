import os

ROOT_DIR_NAME='ml-100k'

class FBOrginal():
    __BASE = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'freebase-orginal')
    RDF=os.path.join(__BASE,'freebase-rdf-latest.gz')

class FBMovie():
    __BASE = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'fb-kg-movie')
    movies_tsv=os.path.join(__BASE,'fb_movies.tsv')
    names_tsv=os.path.join(__BASE,'names.tsv')
    paris_count_tsv = os.path.join(__BASE, 'paris_count.tsv')

class FBEasyMovies():
    __BASE = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'easy-fb-kg-movie')
    names_tsv=os.path.join(__BASE,'fb_entity_names.tsv')
    types_tsv=os.path.join(__BASE,'fb_entity_types.tsv')
    movies_tsv=os.path.join(__BASE,'fb_movies.tsv')
    ml2fb_links=os.path.join(__BASE,'ml2fb.txt')
    paris_count_tsv=os.path.join(__BASE,'paris_count.tsv')
    all_relations = os.path.join(__BASE, 'all_relations.tsv')
    all_relations_chose = os.path.join(__BASE, 'all_relations_chose.tsv')

class RecData():
    FbKg='easy-fbkg'
    Rec='easy-rec'
    Orginal='orginal'
    Trainning='trainning'
    TrainningLink='trainning-link'

    @staticmethod
    def getKb4RecDateSetPaths(rootDirName):
        rootDir = os.path.join(os.path.split(os.path.realpath(__file__))[0], rootDirName)
        dict={}
        FbkgDir = os.path.join(rootDir,RecData.FbKg)
        dict[RecData.FbKg]={}
        dict[RecData.FbKg]['names']=os.path.join(FbkgDir, 'e_names_fb.tsv')
        dict[RecData.FbKg]['types'] = os.path.join(FbkgDir, 'e_types_fb.tsv')
        dict[RecData.FbKg]['kg'] = os.path.join(FbkgDir, 'kg.tsv')
        dict[RecData.FbKg]['ml2fb_link'] = os.path.join(FbkgDir, 'ml2fb_link.json')
        dict[RecData.FbKg]['count']=os.path.join(FbkgDir,'paris_count.tsv')

        RecDir = os.path.join(rootDir,RecData.Rec)
        dict[RecData.Rec] = {}
        dict[RecData.Rec]['movieids_json'] = os.path.join(RecDir,'ml_movieids.json')
        dict[RecData.Rec]['ratings'] = os.path.join(RecDir,'ratings.tsv')

        TrainningDir = os.path.join(rootDir,RecData.Trainning)
        dict[RecData.Trainning]={}
        dict[RecData.Trainning]['kg_index'] = os.path.join(TrainningDir,'kg_index.tsv')
        dict[RecData.Trainning]['rating_index'] = os.path.join(TrainningDir,'rating_index.tsv')
        dict[RecData.Trainning]['rating_index_5'] = os.path.join(TrainningDir, 'rating_index_5.tsv')

        TrainningLinkDir = os.path.join(rootDir, RecData.TrainningLink)
        dict[RecData.TrainningLink] = {}
        dict[RecData.TrainningLink]['eid2index'] = os.path.join(TrainningLinkDir, 'eid2index.json')
        dict[RecData.TrainningLink]['rid2index'] = os.path.join(TrainningLinkDir, 'rid2index.json')
        dict[RecData.TrainningLink]['uid2index'] = os.path.join(TrainningLinkDir, 'uid2index.json')

        OrginalDir = os.path.join(rootDir,RecData.Orginal)
        dict[RecData.Orginal] = {}
        if rootDirName=='ml-1m':
            dict[RecData.Orginal]['movies'] = os.path.join(OrginalDir,'movies.dat')
            dict[RecData.Orginal]['ratings']=os.path.join(OrginalDir,'ratings.dat')
            dict[RecData.Orginal]['user'] = os.path.join(OrginalDir, 'users.dat')
        elif rootDirName=='ml-100k':
            dict[RecData.Orginal]['movies'] = os.path.join(OrginalDir,'u.item')
            dict[RecData.Orginal]['ratings'] = os.path.join(OrginalDir,'u.data')
            dict[RecData.Orginal]['user'] = os.path.join(OrginalDir,'u.user')
        elif rootDirName=='ml-latest-small':
            dict[RecData.Orginal]['movies'] = os.path.join(OrginalDir,'movies.csv')
            dict[RecData.Orginal]['ratings'] = os.path.join(OrginalDir,'ratings.csv')
        return dict

class MovieLensDatas():
    pathsDict=RecData.getKb4RecDateSetPaths(ROOT_DIR_NAME)













# kb4recMovielensDataProcess

## Directory
* [Quick Start](#Quick_Start)
* [各文件生成过程说明](#各文件生成过程说明)
* [引用说明](#引用说明)
* [Related Papers](#Papers)

## <div id="Quick_Start"></div>Quick Start
* 用来处理freebase, kb4rec, movielens它们数据集的项目。如果你不关心过程，
那么目前可直接使用data_set/ml文件夹下的文件。(ml文件夹指ml-1m,ml=100k,ml-latest-small),
如果你不需要保留freebase和movielens的具体信息的话(如电影名字等等),那么ml/trainning下的文件直接可用作训练。

* kg_index.tsv 是知识图谱三元组数据。文件结构为entity_index, relation_index, entity_index。

* rating_index.tsv是用户评分三元组数据。文件结构为user_index, movie_index, rating_flag。
其中movie_index与kg_index.tsv中的entity_index,但entity_index不仅包含movie_index,还包括movie以外的实体index。

## <div id="各文件生成过程说明"></div>各文件生成过程说明
**1. 整个项目最初的数据是:**

1.1   freebase-rdf-latest.gz<br>
* 这是freebase最新版本的所有数据,下载地址为：https://developers.google.com/freebase/
![freebase dump](readme_figure/dump.jpg)
文件差不多30G，解压后近400G(别信上图中的数字)，但我们不需要解压，直接放在目录data_set/freebase-orginal/ 下即可。

1.2   ml-orginal目录下的文件<br>
* 即movieLens原始数据，下载地址为https://grouplens.org/datasets/movielens/
下载后放在对应的data_set/ml*/ml-orginal文件夹下即可。例如ml-1m的数据就放在data_set/ml-1m/ml-orgnial<br>
已经下载好了ml-1m,ml-100k,ml-latest-small的数据。

1.3   ml2fb.txt<br>
* 这是中国人民大学信息学院的一个项目：<br>
github地址：https://github.com/RUCDM/KB4Rec<br>
paper地址：https://www.mitpressjournals.org/doi/full/10.1162/dint_a_00008<br>
即kb4rec(knowledge base information for recommender system)项目[1]，他们将知识图谱数据与推荐开源数据做了一个连接，ml2fb.txt是他们项目中连接movielens数据集与freebase数据集的文件。
可在他们的github中获取，获取后放在data_set/easy-fb-kg-movie目录下。(已经下载好放在那了)

**2. 主要的脚本文件都在process文件夹下:**

执行顺序如下：

2.1 fromFbOrginal2FbKgMovie.py<br>
* **输入文件:**<br>
data_set/freebase-orginal/freebase-rdf-latest.gz    原freebase文件，除了movie以外还有很多不需要的内容。<br>
* **输出文件:**<br>
data_set/fb-kg-movie/fb_movies.tsv  仅保留freebase中movie的内容。<br>
data_set/fb-kg-movie/names.tsv  仅保留freebase中实体名字的内容。<br>
注意:这个脚本在一般cpu电脑上跑完需要30个小时。

2.2 fromFbMovie2easy.py<br> 
* **输入文件:**<br>
data_set/fb-kg-movie/fb_movies.tsv  仅保留freebase中movie的内容。<br>
data_set/fb-kg-movie/names.tsv  仅保留freebase中实体名字的内容。<br>
* **输出文件:**<br>
data_set/fb-kg-movie/paris_count.tsv  统计freebase中movie数据各个关系对应头尾实体数量的文件。<br>
文件结构：[关系名, "count", 此关系下总共的三元组数量, "h", head实体的去重数量, "t", tail实体的去重数量],<br>
总共7列，打引号的部分在文件中就是呈现那个字符串，用来表示后一列的内容。<br>
data_set/easy-fb-kg-movie/fb_movies.tsv 简化后的freebase中movie的三元组数据,
将一些冗余的节点与很冷门的关系删掉了，提高了数据的稠密性。<br>
data_set/easy-fb-kg-movie/fb_entity_names.tsv 简化后所有实体的对应的唯一名字。<br>
data_set/easy-fb-kg-movie/fb_entity_types.tsv 简化后所有实体的对应的唯一type。<br>
data_set/easy-fb-kg-movie/paris_count.tsv 简化后数据各个关系对头尾实体数量的统计文件。<br>
data_set/easy-fb-kg-movie/all_relations.tsv 简化后数据的所有关系列表。<br>
data_set/easy-fb-kg-movie/all_relations_chose.tsv 用作手动筛选关系的文件,此文件的具体作用在2.4小节中介绍。<br>
注意:为了方便大家快速使用，该步骤的输出文件在该项目中有保存，所以大家可以跳过2.1和2.2步骤。

2.3 fromRecOrignal2easy.py<br>
* **输入文件:**<br>
data_set/ml*/orginal/movies*    原movieslens的movie内容文件。<br>
data_set/ml*/orginal/ratings*    原movieslens的rating内容文件。<br>
* **输出文件:**<br>
data_set/ml*/easy-rec/ml_movieids.json   只剩movie id的json文件。<br>
data_set/ml*/easy-rec/ratings.tsv    干净一点的ratings文件。<br>
注意:该脚本的目的就是把原movielens的数据集统一格式。<br>

2.4 getKb4rec.py<br>
* **输入文件:**<br>
data_set/ml*/easy-rec/ml_movieids.json   只剩movie id的json文件。<br>
data_set/easy-fb-kg-movie/fb_entity_names.tsv 简化后所有实体的对应的唯一名字。<br>
data_set/easy-fb-kg-movie/fb_entity_types.tsv 简化后所有实体的对应的唯一type。<br>
data_set/easy-fb-kg-movie/paris_count.tsv 简化后数据各个关系对头尾实体数量的统计文件。<br>
data_set/easy-fb-kg-movie/all_relations.tsv 简化后数据的所有关系列表。<br>
data_set/easy-fb-kg-movie/all_relations_chose.tsv 用作手动筛选关系的文件,经过此脚本生成的输出文件只会包含该文件下的关系。<br>
* **输出文件:**<br>
data_set/ml*/easy-fbkg/ml2fb_link.json    对应此movielens数据集下的movielens id与freebase id映射表。<br>
data_set/ml*/easy-fbkg/kg.tsv   对应此movielens数据集的知识图谱简化数据集。<br>
data_set/ml*/easy-fbkg/e_names_fb.tsv    对应此movielens数据集实体的名字。<br>
data_set/ml*/easy-fbkg/e_types_fb.tsv    对应此movielens数据集实体的type。<br>
data_set/ml*/easy-fbkg/paris_count.json    对应此movielens数据集各个关系对头尾实体数量的统计文件。<br>

2.5 getKbrec4trainning.py<br>
* **输入文件:**<br>
data_set/ml*/easy-fbkg/ml2fb_link.json    对应此movielens数据集下的movielens id与freebase id映射表。<br>
data_set/ml*/easy-fbkg/kg.tsv   对应此movielens数据集的知识图谱简化数据集。<br>
data_set/ml*/easy-rec/ratings.tsv    干净一点的ratings文件。<br>
* **输出文件:**<br>
data_set/ml*/trainning/kg_index.tsv 极简的索引形式知识图谱三元组，索引由0开始，增量步长1，
文件中的数字可直接作为训练模型时embeding层的索引。<br>
data_set/ml*/trainning/rating_index.tsv 极简的索引形式用户电影评分三元组，索引由0开始，增量步长1，
文件中的数字可直接作为训练模型时embeding层的索引。评分为原来的数字0-5变为评分flag 1 如果 (原评分>=4) 否则 0。<br>
data_set/ml*/trainning-link/eid2index.json  实体的原id对应现索引的映射表，
如果实体是movie，实体原id是movielens id，
否则是freebase id。<br>
data_set/ml*/trainning-link/rid2index.json  关系对应索引的映射表。<br>
data_set/ml*/trainning-link/uid2index.json  用户id对应索引的映射表。<br>

2.6 根目录下的generateKg4recMovielensFiles.py<br>
* 一键执行2.3, 2.4, 2.5的操作。另外dataset/filePaths.py是记录了所有文件地址的文件。
通过修改该文件下的全局常量ROOT_DIR_NAME,可指定处理ml-1m,ml-100k或者ml-latest-small的甚至是大家新放进来的movielens数据集。


## <div id="引用说明"></div>引用说明
如果要使用本项目数据集，请注明出处。
```
@dataset{
   author = {Rex Fangren Yu},
   title = {kb4rec Movielens Data Process},
   year = {2021},
   URL = {https://github.com/rexrex9/kb4recMovielensDataProcess}
}
```

## <div id="Papers"></div>Related Papers
<strong><div id="Ref-1"></div>[1]
Wayne Xin Zhao, Gaole He, Kunlin Yang, Hongjian Dou, Jin Huang, Siqi Ouyang, Ji-Rong Wen.
KB4Rec: A Data Set for Linking Knowledge Bases with Recommender Systems[D].
School of Information, Renmin University of China, Beijing 100872, China. 2018.



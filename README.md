# kb4recMovielensDataProcess

### Quick Start
* 用来处理freebase, kb4rec, movielens它们数据集的项目。如果你不关心过程，
那么目前可直接使用data_set/ml文件夹下的文件。(ml文件夹指ml-1m,ml=100k,ml-latest-small),
如果你不需要保留freebase和movielens的具体信息的话(如电影名字等等),那么ml/trainning下的文件直接可用作训练。

* kg_index.tsv 是知识图谱三元组数据。文件结构为entity_index, relation_index, entity_index。

* rating_index.tsv是用户评分三元组数据。文件结构为user_index, movie_index, rating_flag。
其中movie_index与kg_index.tsv中的entity_index,但entity_index不仅包含movie_index,还包括movie以外的实体index。

## <div id="各文件生成过程说明"></div>各文件生成过程说明
1. 整个项目最初的需要有:

* freebase-rdf-latest.gz<br>
这是freebase最新版本的所有数据,下载地址为：https://developers.google.com/freebase/
![freebase dump](readme_figure/dump.jpg)
文件有30多G，解压后近400G，但我们不需要解压，直接放在目录data_set/freebase-orginal/ 下即可。

* ml-orginal目录下的文件<br>
即movieLens原始数据，下载地址为https://grouplens.org/datasets/movielens/
下载后放在对应的data_set/ml*/ml-orginal文件夹下即可。例如ml-1m的数据就放在data_set/ml-1m/ml-orgnial<br>
我已经下载好了ml-1m,ml-100k,ml-latest-small的数据。

* ml2fb.txt<br>
这是中国人民大学信息学院的一个项目：<br>
github地址：https://github.com/RUCDM/KB4Rec<br>
paper地址：https://www.mitpressjournals.org/doi/full/10.1162/dint_a_00008<br>
即kb4rec(knowledge base information for recommender system)项目[1]，他们将知识图谱数据与推荐开源数据做了一个连接，ml2fb.txt是他们项目中连接movielens数据集与freebase数据集的文件。
可在他们的github中获取，获取后放在data_set/easy-fb-kg-movie目录下。(我已经下载好放在那了)





## <div id="Papers"></div>Related Papers
<strong><div id="Ref-1"></div>[1]
Wayne Xin Zhao, Gaole He, Kunlin Yang, Hongjian Dou, Jin Huang, Siqi Ouyang, Ji-Rong Wen.
KB4Rec: A Data Set for Linking Knowledge Bases with Recommender Systems[D].
School of Information, Renmin University of China, Beijing 100872, China. 2018.



`# kb4recMovielensDataProcess

### Quick Start
用来处理freebase, kb4rec, movielens他们数据集的项目。如果你不关心过程，
那么目前可直接使用data_set/ml文件夹下的文件。(ml文件夹指ml-1m,ml=100k,ml-latest-small),
如果你不需要保留freebase和movielens的具体信息的话(如电影名字等等),那么ml/trainning下的文件直接可用作训练。

kg_index.tsv 是知识图谱三元组数据。文件结构为entity_index, relation_index, entity_index。

rating_index.tsv是用户评分三元组数据。文件结构为user_index, movie_index, rating_flag。
其中movie_index与kg_index.tsv中的entity_index,但entity_index不仅包含movie_index,还包括movie以外的实体index。



### 使用说明
主要的脚本在process文件夹下。

1. 整个项目最初的文件有freebase-rdf-latest.gz,与ml-orginal下的文件。



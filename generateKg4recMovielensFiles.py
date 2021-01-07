__author__ = 'yfr'

#https://github.com/rexrex9/kb4recMovielensDataProcess

from process import fromRecOrignal2easy,getkb4rec,getkb4rec4trainning

if __name__ == '__main__':
    fromRecOrignal2easy.getEasyRec()
    getkb4rec.getFBKgFiles()
    getkb4rec.getPairsCount()
    getkb4rec4trainning.deal()
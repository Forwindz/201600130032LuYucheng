import sys
import json
import os
import nltk
from textblob import TextBlob
from textblob import Word
import pickle
import random

from time import time
import numpy as np
import matplotlib.pyplot as plt

import sklearn
import sklearn.cluster
from sklearn import metrics
from sklearn.cluster import *
from sklearn.mixture import GaussianMixture
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.feature_extraction.text import TfidfVectorizer;
from sklearn.feature_extraction.text import *;

#==========================
def save(name,data,mode=0):
    if(mode==1 and type(data) in [list,dict,set]):
        with open(name+".json",'w') as f:
            json.dump(data,f)
    elif mode==0:
        with open(name+".npy",'wb') as f:
            pickle.dump(data,f,True)
    elif mode==2:
        with open(name+".txt",'w') as f:
            f.write(str(data))
    return;
#=========================
def load(name,mode=0):
    if(mode==1):
        if not os.path.exists(name+".json"):
            return None
        with open(name+".json",'r') as f:
            data = json.load(f)
    elif mode==0:
        if not os.path.exists(name+".npy"):
            return None
        with open(name+".npy",'rb') as f:
            data = pickle.load(f)
    elif mode==2:
        if not os.path.exists(name+".txt"):
            return None
        with open(name+".txt",'r') as f:
            return f.readlines()
    return data;
#========================
#read data
def readTweets():
    f = open("Homework5Tweets.json")
    lines = f.readlines()
    texts = []
    cluster = []
    if len(lines)<=1:
        print("There might some errors while reading file")
    for line in lines:
        tempObj = json.loads(line)
        texts.append(tempObj['text'])
        cluster.append(tempObj['cluster'])
    return texts,cluster;

def procDocs():
    print("check cache...")
    data0=load("data")
    label0=load("label")
    if data0 is None or label0 is None:
        print("Invalid cache, reconstruct data")
    else:
        print("use cache")
        return data0,label0;

    print("read tweets...")
    texts,cluster=readTweets()
    print("doc num = %d" % len(texts))
    print("Get words... Doc ="+str(len(texts)))
    textContent=[]
    wordSet = set([])
    for text in texts:
        words=TextBlob(text.replace('-',' ')).words
        textContent.append(words)
        for word in words:
            wordSet.add(word)

    print("build dictionary")
    wordDict={}
    for i,word in enumerate(wordSet):
        wordDict[word]=i
    print("Total words: %d"% len(wordDict))
    print("build arrays")
    data = np.zeros((len(textContent),len(wordDict)),dtype=int)
    label = np.array(cluster);
    for i,words in enumerate(textContent):
        if i%100==0:
            print("building array... %d"%i,end='\r')
        for word in words:
            data[i][wordDict[word]]+=1

    print("saving as cache...")
    save("data",data);
    save("lable",label);
    return data,label;

def tfidf():
    data,label = readTweets()
    t=sklearn.feature_extraction.text.TfidfVectorizer()
    return t.fit_transform(data),label

if __name__=="__main__":
    #tfidf() input tfidf values
    #procDocs() input word frequency values
    data,label=tfidf()#procDocs()
    print("Data Shape:"+str(data.shape))
    def estimate(name,esti):
        t0=time()
        esti.fit(data)
        print("%-15s\t%.2fs\t%.3f"%(name,time()-t0,
                                       metrics.normalized_mutual_info_score(label,esti.labels_,average_method='arithmetic')))
    def estimate_dense(name,esti):
        t0=time()
        esti.fit(data.todense())
        print("%-15s\t%.2fs\t%.3f"%(name,time()-t0,
                                       metrics.normalized_mutual_info_score(label,esti.labels_,average_method='arithmetic')))
    def estimate_(name,esti):
        t0=time()
        esti.fit_predict(data.todense(),label)
        print("%-15s\t%.2fs\t%.3f"%(name,time()-t0,
                                       metrics.normalized_mutual_info_score(label,esti.predict(data.todense()),average_method='arithmetic')))

    print("name    \ttime  \t score")
    print("_"*40)
    
    
    estimate_dense("Agg ward",AgglomerativeClustering(n_clusters=max(label),linkage="ward"))
    estimate_dense("Agg complete",AgglomerativeClustering(n_clusters=max(label),linkage="complete"))
    estimate_dense("Agg average",AgglomerativeClustering(n_clusters=max(label),linkage="average"))
    estimate_dense("Agg single",AgglomerativeClustering(n_clusters=max(label),linkage="single"))
    
    estimate("Specutal C1",SpectralClustering(n_clusters=max(label),gamma=1,affinity='rbf'))
    estimate("Specutal C1.5",SpectralClustering(n_clusters=max(label),gamma=1.5,affinity='rbf'))
    estimate("Specutal C0.5",SpectralClustering(n_clusters=max(label),gamma=0.5,affinity='rbf'))
    estimate("DBSCAN2",DBSCAN(eps=2.0))
    estimate("DBSCAN1.5",DBSCAN(eps=1.5))
    estimate("DBSCAN1",DBSCAN(eps=1.0))
    estimate("DBSCAN0.5",DBSCAN(eps=0.5))
    
    estimate("K-means_++",KMeans(init='k-means++', n_clusters=max(label), n_init=10))
    estimate("K-means_ran",KMeans(init='random', n_clusters=max(label), n_init=10))
    estimate("Affinty P",AffinityPropagation())
    estimate_dense("MeanShift F",MeanShift(bin_seeding=False))
    estimate_dense("MeanShift T",MeanShift(bin_seeding=True))
    estimate_("Gaussian M",GaussianMixture(max_iter=500))
    
    

        









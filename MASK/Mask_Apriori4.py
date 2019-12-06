#Apriori算法实现
from numpy import *
import re
import numpy as np
from itertools import combinations
import math
import pickle

def loadDataSet():
    #return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    
    L=[]
    fo=open("D:\code\python\MASK/data5\\3_3.data",'r')
    str=fo.readline()
    while(str!=''):
        li=re.findall('\d+',str)
        L.append(li[1:])
        str=fo.readline()
    #for i in L:
        #print(i)
    fo.close()
    return L
    
#======================================================================== 
# 获取候选1项集，dataSet为事务集。返回一个list，每个元素都是set集合
def createC1(dataSet):
    C1 = []   # 元素个数为1的项集（非频繁项集，因为还没有同最小支持度比较）
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()  # 这里排序是为了，生成新的候选集时可以直接认为两个n项候选集前面的部分相同
    # 因为除了候选1项集外其他的候选n项集都是以二维列表的形式存在，所以要将候选1项集的每一个元素都转化为一个单独的集合。
    return list(map(frozenset, C1))   #map(frozenset, C1)的语义是将C1由Python列表转换为不变集合（frozenset，Python中的数据结构）

def combine(li):
    temp_li={}
    num_li=[1,2,4,8,16,32,64,128,256,512,1024,2048]
    num=[]
    #print("长度",len(li))
    for i in range(0,len(li)+1):
        for c in combinations(num_li[:len(li)],i):
            num.append(sum(c))
    #print(num)
    n=0
    for i in range(0,len(li)+1): 
        for c in combinations(li,i):
            temp_li[c]=[0,num[n]]
            #print(c,num[n])
            n=n+1
    #print(temp_li)
    return(temp_li)

def calc_M_(k,p):
    #M_=np.array([[p,p-1],[p-1,p]])
    #M_1=np.array([[M_,][0,M_]])
    #print(M_)
    if k==1:
        M_=np.array([[p,p-1],[p-1,p]])
        return M_
    else:
        M_=calc_M_(k-1,p)
        n=pow(2,k-1)
        #print(M_,k,n)
        M_1=np.concatenate([M_,np.zeros([n,n])],1)
        M_2=np.concatenate([np.zeros([n,n]),M_],1)
        M_B=np.concatenate([M_1,M_2])

        M_1=np.concatenate([p*np.identity(n),(p-1)*np.identity(n)],1)
        M_2=np.concatenate([(p-1)*np.identity(n),p*np.identity(n)],1)
        M_E=np.concatenate([M_1,M_2])
        #print(M_B,'\n',M_E)
        M_=M_B*M_E
        return M_

# 找出候选集中的频繁项集
# dataSet为全部数据集，Ck为大小为k（包含k个元素）的候选项集，minSupport为设定的最小支持度
def scanD(dataSet, Ck, minSupport,kk):
    ssCnt = {}   # 记录每个候选项的个数
    #初始化好每个组合
    for can in Ck:
        ssCnt[can]=combine(can)

    #print(Ck)
    for tid in dataSet:
        #print(tid)
        for can in Ck:
            #print(can)
            for items_dic in ssCnt[can]:
                #print(items_dic)
                #print(items_dic[0])
                if str(items_dic)=='()':
                    #print(set(can))
                    '''
                    if not set(can).issubset(tid):
                        ssCnt[can][items_dic][0]+=1
                    '''
                    pass
                elif set(items_dic).issubset(tid):
                    ssCnt[can][items_dic][0]+=1
                    #print(ssCnt[can][items_dic])
    '''
    #print(ssCnt)
    f1=open("D:\code\python\MASK/data5\\1.txt","a")
    for k,v in ssCnt.items():
        f1.write(str(k))
        f1.write("\t")
        f1.write(str(v))
        f1.write('\n')
    f1.close()
    '''
    numItems = float(len(dataSet))
    #print(numItems)
    retList = []
    supportData = {}
    p=0.8
    M_=(1/(2*p-1))*calc_M_(kk,p)

    #print(M_)
    for key in ssCnt:
        v_result=[] #存储计数个数 290
        k_result=[] #存储编号 1
        #print(ssCnt[key])
        
        for k,v in ssCnt[key].items():
            v_result.append(v[0])
            k_result.append(v[1])
        #print(v_result,k_result)
        support=0
        for j in range(pow(2,kk)):
            #print(j)
            if j==0:
                supp1=numItems-sum(v_result)
                if supp1<0:
                    supp1=0
                support=support+supp1*M_[0][pow(2,kk)-1]
                #print(supp1,M_[0][pow(2,kk)-1],support,'\n')
            else:
                support=support+v_result[j]*M_[0][int(k_result[pow(2,kk)-1-j])]
                #print(v_result[j],M_[0][int(k_result[pow(2,kk)-1-j])],support,'\n')
            #support=(M_[0][0]*ssCnt[key]+M_[0][1]*(numItems-ssCnt[key]))/numItems
        
        support=support/numItems
        #print(ssCnt[key],support,'\n')
        if support >= minSupport:
            retList.insert(0, key)  #将频繁项集插入返回列表的首部
        supportData[key] = support

    return retList, supportData   #retList为在Ck中找出的频繁项集（支持度大于minSupport的），supportData记录各频繁项集的支持度

# 通过频繁项集列表Lk和项集个数k生成候选项集C(k+1)。
def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    #print(lenLk)
    #print(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            # 前k-1项相同时，才将两个集合合并，合并后才能生成k+1项
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]   # 取出两个集合的前k-1个元素
            L1.sort(); L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList

#========================================================================
# 获取事务集中的所有的频繁项集
# Ck表示项数为k的候选项集，最初的C1通过createC1()函数生成。Lk表示项数为k的频繁项集，supK为其支持度，Lk和supK由scanD()函数通过Ck计算而来。
def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet)  # 从事务集中获取候选1项集
    D = list(map(set, dataSet))  # 将事务集的每个元素转化为集合
    L1, supportData = scanD(D, C1, minSupport,1)  # 获取频繁1项集和对应的支持度
    L = [L1]  # L用来存储所有的频繁项集
    k = 2

    while(len(L[k-2])>0):
    #while(k<4):
        Ck=aprioriGen(L[k-2],k)
        #支持度重构
        Lk, supK = scanD(D, Ck, minSupport,k)
        L.append(Lk);supportData.update(supK)
        k+=1
    return L, supportData
    
#========================================================================
#产生强关联规则
def generateRules(L, supportData, minConf=0.7):  #supportData is a dict coming from scanD
    bigRuleList = []
    for i in L:
        print(i)
    for i in range(1, len(L)):#only get the sets with two or more items
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            print(H1)
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    prunedH = [] #create new list to return
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq] #calc confidence
        if conf >= minConf: 
            print(freqSet-conseq,'-->',conseq,'conf:',conf)
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    #print(m,len(freqSet))
    if (len(freqSet) > (m + 1)): #try further merging
        Hmp1 = aprioriGen(H, m+1)#create Hm+1 new candidates
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):    #need at least two sets to merge
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)
       
def pntRules(ruleList, itemMeaning):
    for ruleTup in ruleList:
        for item in ruleTup[0]:
            print(itemMeaning[item])
        print("           -------->")
        for item in ruleTup[1]:
            print(itemMeaning[item])
        print("confidence: %f" % ruleTup[2])
        print('\n')       #print a blank line

#======================================================================== 
if __name__=='__main__':
    dataSet = loadDataSet()  # 获取事务集。每个元素都是列表
    # C1 = createC1(dataSet)  # 获取候选1项集。每个元素都是集合
    # D = list(map(set, dataSet))  # 转化事务集的形式，每个元素都转化为集合。
    # L1, suppDat = scanD(D, C1, 0.5,1)
    # print(L1,suppDat)
    
    L, suppData = apriori(dataSet,minSupport=0.1)
    #rules=generateRules(L,suppData,minConf=0.7)
    #print(rules)
    print(len(L[0]),len(L[1]),len(L[2]))
    #print(L)

    f1=open("D:\code\python\MASK/data5\\pic_result_frequent.pkl","wb")
    pickle.dump(L,f1)
    f1.close()
    
    fo=open("D:\code\python\MASK/data5\\result_supp.txt","w")
    for i in suppData:
        fo.write(str(i))
        fo.write('\t')
        fo.write(str(suppData[i]))
        #fo.write('\n')
        fo.write('\n')
    fo.close()

    fo=open("D:\code\python\MASK/data5\\result_frequent.txt","w")
    for i in L:
        fo.write(str(i))
        fo.write('\n')
        fo.write('\n')
    fo.close()
    '''
    for i in suppData:
        print(i,suppData[i])
    
    '''

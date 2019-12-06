import random
import re

p=0.8
T={}
                   
f_ori=open("D:\code\python\MASK/data4\\3_2.data",'w')
fp=open("D:\code\python\MASK/data4\\333.data",'r')
strs=fp.readline()
#print(re.findall('\d+',strs))
li=re.findall('\d+',strs)

while(strs!=''):
    if li[1] not in T:
        f_ori.write(li[1]+':')
        T[li[1]]=[]
    ls=[]
    pos=li[1]
    while(strs!='' and li[1] in T):
        f_ori.write(li[2]+',')
        ls.append(li[2])
        q=random.random()
        if(q<p):
            #不变
            T[li[1]].append(li[2])
        else:
            #取反
            pass
        strs=fp.readline()
        li=re.findall('\d+',strs)
        #print(li)
    #print(ls)
    #print(T,li[1])
    #for i in range(10):
    for i in range(20):
        if str(i) not in ls:
            #print(i)
            q=random.random()
            if(q>p):
                #gai变
                T[pos].append(str(i))
    f_ori.write('\n')
    #print(T)

    
f_ori.close()
fp.close()

print('finish')
fo=open("D:\code\python\MASK/data4\\3_3.data",'w')
#fo.write('hell'+':')
for i in T:
    fo.write(i+':')
    ls=T[i]
    ls=list(map(int,ls))
    ls.sort()
    #print(ls)
    for j in ls:
        fo.write(str(j)+',')
    fo.write('\n')

fo.close()


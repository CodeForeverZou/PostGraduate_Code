import random
import re

p=0.8
T={}
'''
fp=open("D:\code\python\MASK\\333.data",'r')
f_ori=open("D:\code\python\MASK\\3_2.data",'w')
str=fp.readline()
li=re.findall('\d+',str)
while(str!=''):
    f_ori.write(str(li[1])+':')
    while(str!='' and li[1] in T):
        f_ori.write(str(li[2])+',')
    str=fp.readline()
    li=re.findall('\d+',str)

f_ori.close()
'''                    
f_ori=open("D:\code\python\MASK/data2\\3_2.data",'w')
fp=open("D:\code\python\MASK/data2\\333.data",'r')
str=fp.readline()
#print(re.findall('\d+',str))
li=re.findall('\d+',str)
while(str!=''):
    if li[1] not in T:
        f_ori.write(li[1]+':')
        T[li[1]]=[]
    while(str!='' and li[1] in T):
        f_ori.write(li[2]+',')
        q=random.random()
        if(q<p):
            #不变
            T[li[1]].append(li[2])
        else:
            #取反
            pass
        str=fp.readline()
        li=re.findall('\d+',str)
        #print(li)
    f_ori.write('\n')
    #print(T)
f_ori.close()
fp.close()

print('finish')
fo=open("D:\code\python\MASK/data2\\3_3.data",'w')
#fo.write('hell'+':')
for i in T:
    fo.write(i+':')
    for j in T[i]:
        fo.write(j+',')
    fo.write('\n')

fo.close()


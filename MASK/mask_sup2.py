import random
import re
class Error(Exception):
    #error
    pass

p=1
T={}
n=0
fp=open("D:\code\python\MASK\\222.data",'r')
#print(len(fp))

#str=fp.readline()

str=fp.readline()
#print(re.findall('\d+',str))
li=re.findall('\d+',str)

while(str!=''):
    if li[1] not in T:
        T[li[1]]=[]
    while(str!='' and li[1] in T):
        q=random.random()
        if(q<p):
            #不变
            try:
                T[li[1]].append(li[2])
            except:
                pass
            
        else:
            #取反
            pass
        str=fp.readline()
        li=re.findall('\d+',str)
        #print(li) 
    #print(T)
    
print('finish')
fo=open("D:\code\python\MASK\\2_2.data",'w')
for i in T:
    fo.writelines(T[i])

fo.close()

'''
li=str.split(' ')
li.sort()
n=li.count('')
while(n):
    li.remove('')
    n=n-1
#print(li)
'''

'''
while(str!=''):
    if li[1] not in T:
        T[li[1]]=[]
    while(str!='' and li[1] in T):
        q=random.random()
        if(q<p):
            #不变
            try:
                T[li[1]].append(li[3][:-1])
                raise Error()
            except Error:
                T[li[1]].append(li[2][:-1])
            except:
                pass
            
        else:
            #取反
            pass
        str=fp.readline()
        li=str.split('         ')
        #print(li) 
    #print(T)
    
print(T)
fp.close()

fo=open("D:\code\python\MASK\\2_2.data",'w')
for i in T:
    fo.writelines(T[i])

fo.close()
'''

import pickle

f1=open("D:\code\python\MASK/data5\\pic_result_frequent.pkl","rb")
L1=pickle.load(f1)
f1.close()

f2=open("D:\code\python\MASK/data5\\pic_result_frequent2.pkl","rb")
L2=pickle.load(f2)
f2.close()

len_R=0
L1_=[]
for i in L1:
    L1_1=[]
    for j in i:
        l=list(map(int,j))
        #print(l)
        l.sort()
            
        L1_1.append(l)
        #print(L2)
    len_R+=len(L1_1)
    L1_1.sort()
    L1_.append(L1_1)
    #print(L3)

len_F=0
L2_=[]
for i in L2:
    L2_1=[]
    for j in i:
        l=list(map(int,j))
        #print(l)
        l.sort()
            
        L2_1.append(l)
        #print(L2)
    len_F+=len(L2_1)
    L2_1.sort()
    L2_.append(L2_1)
    #print(L3)

diff_H=0
diff_L=0
diff_l=[]
for i in range(len(L1)):
    for j in L1_[i]:
        if j not in L2_[i]:
            diff_l.append(j)
            diff_H+=1
    for j in L2_[i]:
        if j not in L1_[i]:
            diff_l.append(j)
            diff_L+=1
print(diff_H/len_F,diff_L/len_F,'\n')
print((len_F-len_R)/len_F)
#print(diff,diff_l)
print(diff_H,diff_L,len_F,len_R)
#print(L1_)
print('\n')
#print(L2_)

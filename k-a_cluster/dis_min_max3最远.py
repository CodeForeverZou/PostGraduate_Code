#====================================获取分类树 元组====================================
import os
import trees
import time
begain=time.time()
TS=trees.GetTrees()


#====================================LCA查找最近公共祖先====================================
global father
global dict_vis
dict_arc={} #节点-节点，图
father={}   #并查集的父亲
dict_vis={} #LCA中的标记访问
TL=[]       #每棵树的，dict_arc图

#定义并查集
#def init()：由生成字典完成
def find(v):
    if(father[v]==v):
        return v
    else:
        return find(father[v])

#初始化father、visited===========每次LCA前都要做的====================
def init_f_v(node,ti):
    dict_vis[node.tag]=0    #初始化visited
    father[node.tag]=node.tag   #初始化father，并查集
    
    for i in TS[ti].children(node.tag):
        init_f_v(i,ti)

#生成边字典
def gen_dict_arc(node,ti):
    dict_arc[node.tag]=[i.tag for i in TS[ti].children(node.tag)]

    #print(node.tag)

    for i in TS[ti].children(node.tag):
        #print(type(i.tag))
        gen_dict_arc(i,ti)
        

global np
np=''
#====================================主函数tarjon
def tarjon(s,p,q,ti):
    global np
    dict_vis[s.tag]=1
    if(s.tag==p):
        if(dict_vis[q]):
            np=find(q)
    elif(s.tag==q):
        if(dict_vis[p]):
            np=find(p)

    for i in TL[ti][s.tag]:
        if dict_vis[i]:
            continue
        tarjon(TS[ti].get_node(i),p,q,ti)
        father[i]=s.tag

#================必须做的====================为每棵树产生图，节点-节点，
data=[] #数据元组
QID = (0,1,2,3,4,5) #要进行匿名的属性值

for i in range(len(TS)):
    dict_arc={} #节点-节点，图
    gen_dict_arc(TS[i].get_node(TS[i].root),i)
    TL.append(dict_arc)

#print(TL[3])

low=('neck injury', 'fever', 'cough', 'rhinitis', 'chicken pox', 'diarrhea', 'myopia', 'crus fracture',
     'headache', 'chilblain', 'acute pharyngitis', 'arthritis', 'drug allergy', 'osteoporosis',
     'tonsillitis', 'periodontitis')
#====================================导入原始表====================================
def Init():
    '''
    初始化，生成树,设置阈值，初始化要匿名的属性值
    :return: 所有数据元祖，阈值，所有属性的树
    '''
    #第一步：读取数据，生成元组
    path = os.path.abspath('..')  # 表示当前所处的文件夹上一级文件夹
    data_path = path + '\\k-a_cluster\\data2.txt'
    #data_path = path + '\\k-a_cluster\\data5000.txt'
    #data_path = path + '\\k-a_cluster\\data.txt'
    data_file = open(data_path, 'r')
    lines = data_file.readlines()
    
    for line in lines:
        i = line[:-1].split(',')
        data.append(i)
    data_file.close()

#====================================获得两者间距离
#分类属性距离dis_c
def dis_c(p,q,ti):
    rnode=TS[ti].get_node(TS[ti].root)
    global father
    global dict_vis
    father={}   #并查集的父亲
    dict_vis={} #LCA中的标记访问
    init_f_v(rnode,ti)   #LCA前初始化father、visited
    #print(dict_vis)
    #print(TL[ti])
    tarjon(rnode,p,q,ti) #调试函数tarjon
  
    #print(p,q,np)
    #计算分类属性 内距离
    #节点Nodef、x、y
    Nx=-(TS[ti].level(np)-TS[ti].level(p))+1    #x到最近公共祖先要经过的节点数
    Ny=-(TS[ti].level(np)-TS[ti].level(q))+1    #y到最近公共祖先要经过的节点数
    Nf=TS[ti].level(np)+1     #Nodef到根节点要经过的节点数
    #print(Nx,Ny,Nf)
    dis_s=1-(2*Nf/(Nx+Ny+2*Nf))
    '''
    if(Nx==0 and Ny==0 and Nf==0):
        dis_s=0        
    else:
        dis_s=1-(2*Nf/(Nx+Ny+2*Nf))
    '''
    #Nf=TS[ti].level(np)
    #dis_s=max(TS[ti].level(p),TS[ti].level(q))-Nf
    #print(dis_s)
    return(dis_s)

#数值属性距离dis_n
def dis_n(x,y,scope):
    return abs(y-x)/scope
    
#总距离dis
def get_dis(r,s):
    total_dis=0
    for i in QID:
        try:
            x=int(r[i])
            y=int(s[i])
            if i==0:
                #print(dis_n(x,y,100),'\n')
                total_dis=total_dis+dis_n(x,y,100)
            elif i==2:
                #print(dis_n(x,y,300-90),'\n')
                total_dis=total_dis+dis_n(x,y,300-90)
            #print(1)
        except:
            if i==1:
                ti=0
                #print(dis_c(r[i],s[i],ti),'\n')
                total_dis=total_dis+dis_c(r[i],s[i],ti)
                #print(total_dis,dis_c(r[i],s[i],ti))
            else:
                ti=i-2
                #疾病是不是low中的，不是才能在分类树中找到
                if(ti==3 and (r[i] in low and s[i] in low)):
                    total_dis=total_dis+0
                elif(r[i] in low and s[i] not in low):
                    total_dis=total_dis+dis_c('Diseases',s[i],ti)+0.5   #为了让敏感不见
                elif(r[i] not in low and s[i] in low):
                    total_dis=total_dis+dis_c(r[i],'Diseases',ti)+0.5
                else:
                    #print(dis_c(r[i],s[i],ti),'\n')
                    total_dis=total_dis+dis_c(r[i],s[i],ti)
            #print(2)
    #print(total_dis)
    return total_dis
    
#Init()
r=['34', 'female', '170', 'alone', 'workclass', 'crus fracture']
y=['46', 'male', '255', 'marital-status', 'Federal-gov', 'diabetes']
#print(get_dis(r,y))
#print(data[0])
#TS[3].show()
#print(dis_c('female','male',0))
#====================================获取与r最近的记录s
#随机选择一条记录r，作为匿名开始
#遍历剩下的记录中，寻找与r距离最近的一条s
dict_k={}   #存储k匿名表，｛[k1,,],[k2,,]…｝
temp=data
global min_dis
global max_dis
global mt   #最远记录的位置
k=5     #k匿名
ni=0    #匿名组个数
global temp_add_in_k
temp_add_in_k={}

def find_rs(r):
    global min_dis
    global max_dis
    global temp_add_in_k
    global mt
    #print(temp_add_in_k)
    min_dis=float("inf")
    max_dis=0
    t=0     #最近记录标记
    mt=0    #最远记录标记
    #遍历temp表
    for i in range(len(temp)):
        #print(r,temp[i])
        dis_r=get_dis(r,temp[i])  #获得两者距离
        #=================最近的距离=================
        if dis_r<min_dis:
            min_dis=dis_r
            t=i     #记录该记录位置
        if dis_r<1:   #小于指定阈值
            temp_add_in_k[i]=dis_r
        #=================最远的距离=================
        if dis_r>max_dis:
            max_dis=dis_r
            mt=i     #记录该记录位置
    return t

#第一个记录组迭代到，其个数大于k为止
def repeat_k(r,i):
    n=1     #该匿名组内记录个数，要求大于k
    global mt
    global min_dis
    global max_dis
    global temp_add_in_k
    
    if(len(temp)>0):
        temp_add_in_k={}        
        t=find_rs(r)
        #print(mt,len(temp))
        #print(max_dis,temp[mt])
        temp_add_in_k[t]=min_dis
        
        #处理阈值小的记录
        #print(r,temp_add_in_k,'\n')
        for in_k in temp_add_in_k:
            temp[int(in_k)].append([temp_add_in_k[in_k]])
            dict_k[i].append(temp[int(in_k)])
            n=n+1
        
        #删除掉已经添加进去后的记录
        nd=0
        for in_k in temp_add_in_k:
            del temp[int(in_k)-nd]
            nd=nd+1
        
        #若达不到k值，需要再添加记录
        while(n<k and len(temp)>0):
            temp_add_in_k={}
            t=find_rs(r)        
            temp[t].append(min_dis)
            dict_k[i].append(temp[t])
            #print(temp[mt])
            del temp[t] #删除掉已经添加进去后的记录
            #print(temp[mt-1])
            if(mt>t):mt=mt-1
            n=n+1

        #print(mt-1,len(temp),'\n')
        #if(len(temp)>mt):print(max_dis,temp[mt],'\n')
        #else:print(len(temp))
    dict_k[i].insert(0,n)   

#聚类最远的那条记录
def find_rs_m_dis(mt_record,i):
    n=1     #该匿名组内记录个数，要求大于k
    global min_dis
    global max_dis
    global temp_add_in_k
    
    if len(temp)>0:
        temp_add_in_k={}       
        t=find_rs(mt_record)
        
        temp_add_in_k[t]=min_dis
        #print(mt_record,min_dis)
        
        #处理阈值小的记录
        #print(temp_add_in_k)
        for in_k in temp_add_in_k:
            temp[int(in_k)].append([temp_add_in_k[in_k]])
            dict_k[i].append(temp[int(in_k)])
            n=n+1
        
        #删除掉已经添加进去后的记录
        nd=0
        for in_k in temp_add_in_k:
            del temp[int(in_k)-nd]
            nd=nd+1
        
        #若达不到k值，需要再添加记录
        while(n<k and len(temp)>0):
            temp_add_in_k={}
            t=find_rs(mt_record)        
            temp[t].append(min_dis)
            dict_k[i].append(temp[t])
            del temp[t] #删除掉已经添加进去后的记录
            n=n+1
            
    dict_k[i].insert(0,n)
    
def save2file():
    path = os.path.abspath('..')  # 表示当前所处的文件夹上一级文件夹
    data_path = path + '\\k-a_cluster\\result100-3.txt'
    #data_path = path + '\\k-a_cluster\\result10000-4.txt'
    #data_path = path + '\\k-a_cluster\\result5000-4.txt'
    data_file = open(data_path, 'w')
    #lines = data_file.readlines()
    for i in dict_k:
        data_file.writelines(str(j) for j in dict_k[i])
        data_file.write('\n')

    data_file.close()

#====================================主函数    

Init()  #读入数据
while(len(temp)!=0):
    global mt
    global max_dis
    r=temp[0]
    #print(r)
    del temp[0]
    dict_k[ni]=[r]   #记录下第ni个匿名组
    repeat_k(r,ni)   #迭代使记录组内个数大于k
    #print(dict_k[ni])
    ni=ni+1

    if(len(temp)>mt):
        #print('==========',max_dis)
        mt_record=temp[mt]
        #print(mt_record,'\n')
        del temp[mt]
        dict_k[ni]=[mt_record]
        find_rs_m_dis(mt_record,ni)   #处理离r最远的记录,用mt标志记录,即temp[mt]
        #print(dict_k[ni])
        ni=ni+1

print(time.time()-begain)
print(ni)    
#print(len(dict_k[13]))
save2file() #保存数据























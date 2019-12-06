import os
#生成一棵树
from treelib import Tree

class Tree1(Tree):
    def createTree(self,path):
        infile = open(path, 'r')
        lines = infile.readlines()  # 读取多行

        tree1 = Tree()

        line1 = lines[0]
        root = line1.split(';')[0]
        children = line1.split(';')[1][:-1]
        childs = children.split(',')

        tree1.create_node(root, root)
        for child in childs:
            tree1.create_node(child, child, parent=root)

        for line in lines[1:]:
            parent = line.split(';')[0]
            children = line.split(';')[1][:-1]
            childs1 = children.split(',')
            for child1 in childs1:
                tree1.create_node(child1, child1, parent=parent)
        return tree1

#====================================一棵分类树
tree=Tree1()
path = os.path.abspath('..')  # 表示当前所处的文件夹上一级文件夹的绝对路径
path1 = path + "\k-a_cluster\\attribute_age.txt"
tree1=tree.createTree(path1)


#====================================LCA查找最近公共祖先====================================
dict_arc={}
father={}
dict_vis={}

#定义并查集
#def init()：由生成字典完成
def find(v):
    if(father[v]==v):
        return v
    else:
        return find(father[v])

#生成边字典
def gen_dict_arc(node):
    dict_arc[node.tag]=[i.tag for i in tree1.children(node.tag)]
    dict_vis[node.tag]=0    #初始化visited
    father[node.tag]=node.tag   #初始化father，并查集
    #print(node.tag)

    for i in tree1.children(node.tag):
        #print(type(i.tag))
        '''
        if node.tag not in dict_arc:
            dict_arc[node.tag]=[i.tag]
        else:
            dict_arc[node.tag].append(i.tag)
        '''
        gen_dict_arc(i)
        
#print(type(tree1.get_node(tree1.root)))
#print(tree1.get_node(tree1.root).tag)
#gen_dict_arc(tree1.get_node(tree1.root))
'''
for i in tree1.children(tree1.root):
    print(i.tag)

for i in dict_arc:
    print(dict_vis[i])
print(len(dict_vis),tree1.size())
'''


#p='36-40'#'21-30'#'1-50'#
#q='31-35'#'51-100'
global np
np=''
#====================================主函数tarjon
def tarjon(s,p,q):
    global np
    dict_vis[s.tag]=1
    if(s.tag==p):
        if(dict_vis[q]):
            np=find(q)
            #print(np)
            #return find(q)
            #return np
    elif(s.tag==q):
        if(dict_vis[p]):
            np=find(p)
            #print(np)
            #return np
            #return find(p)

    for i in dict_arc[s.tag]:
        if dict_vis[i]:
            continue
        tarjon(tree1.get_node(i),p,q)
        father[i]=s.tag


'''
#调试函数tarjon
#tree1.show()
gen_dict_arc(tree1.get_node(tree1.root))
#tarjon(tree1.get_node(tree1.root))
tarjon(tree1.get_node(tree1.root))
#print(np)
#====================================
for i in dict_arc:
    print(i,dict_vis[i])

for i in father:
    print(i,father[i])

#====================================
#print(type(tree1.get_node(tree1.root)))
#print(tree1.children(tree1.root))
#tree1.show()
#print(type(tree1.siblings('1-5')[0]))


#计算分类属性 内距离
#节点Nodef、x、y
Nodef=Sfather(x,y)
Nx=depth(Nodef)-depth(x)    #x到最近公共祖先要经过的节点数
Ny=depth(Nodef)-depth(y)    #y到最近公共祖先要经过的节点数

Nf=depth()-depth(Nodef)     #Nodef到根节点要经过的节点数

dis=1-[2*Nf/(Nx+Ny+2Nf)]

print(tree1.level(np))
print(tree1.level(p))
print(tree1.level(q))
tree1.show()

#====================================计算距离====================================
#计算分类属性 内距离
#节点Nodef、x、y
Nx=-(tree1.level(np)-tree1.level(p))    #x到最近公共祖先要经过的节点数
Ny=-(tree1.level(np)-tree1.level(q))    #y到最近公共祖先要经过的节点数
Nf=tree1.level(np)     #Nodef到根节点要经过的节点数

print(Nx,Ny,Nf)
dis_s=1-(2*Nf/(Nx+Ny+2*Nf))
print(dis_s)

#计算数值属性 距离
l=p.split('-')
#print(l)
Nx=(int(l[1])+int(l[0]))/2
l=q.split('-')
#Ny=l[1]-l[0]
Ny=(int(l[1])+int(l[0]))/2    #中间均值
l=tree1.root.split('-')[1]

print(Nx,Ny,l)
dis_n=abs(Ny-Nx)/int(l)
print(dis_n)
'''

#====================================导入原始表====================================
data=[] #数据元组
QID = (0,1,2,3,4,5) #要进行匿名的属性值

def Init():
    '''
    初始化，生成树,设置阈值，初始化要匿名的属性值
    :return: 所有数据元祖，阈值，所有属性的树
    '''
    #第一步：读取数据，生成元组
    path = os.path.abspath('..')  # 表示当前所处的文件夹上一级文件夹
    data_path = path + '\\k-a_cluster\\data.txt'
    data_file = open(data_path, 'r')
    lines = data_file.readlines()
    
    for line in lines:
        i = line[:-1].split(',')
        data.append(i)

    data_file.close()
    print(data[0])
    #return data

#print()
#随机选择一条记录r，作为匿名开始
#遍历剩下的记录中，寻找与r距离最近的一条s

dict_k={}   #存储k匿名表，｛[k1,,],[k2,,]…｝
temp=data


#====================================获得两者间距离
r=['34', 'female', '170', 'alone', 'workclass', 'crus fracture']
s=['35', 'female', '170', 'alone', 'workclass', 'crus fracture']
scope=100



gen_dict_arc(tree1.get_node(tree1.root))

#分类属性距离dis_c
def dis_c(p,q):
    #调试函数tarjon
    #tarjon(tree1.get_node(tree1.root))
    tarjon(tree1.get_node(tree1.root),p,q)
    #print(np)
    
    #计算分类属性 内距离
    #节点Nodef、x、y
    
    Nx=-(tree1.level(np)-tree1.level(p))    #x到最近公共祖先要经过的节点数
    Ny=-(tree1.level(np)-tree1.level(q))    #y到最近公共祖先要经过的节点数
    Nf=tree1.level(np)     #Nodef到根节点要经过的节点数

    print(Nx,Ny,Nf)
    dis_s=1-(2*Nf/(Nx+Ny+2*Nf))
    return(dis_s)

#数值属性距离dis_n
def dis_n(x,y):
    return abs(y-x)/100
    
#总距离dis
def get_dis(r,s):
    for i in QID:
        try:
            x=int(r[i])
            y=int(s[i])
            print(dis_n(x,y))
            #print(1)
        except:
            print(dis_c(r[i],s[i]))
            #print(2)


get_dis(r,s)
 
    

#====================================获取与r最近的记录s
def find_rs(r):
    min_dis=float("inf")
    t=0
    #遍历temp表
    for i in range(len(temp)):
        dis_r=get_dis(r,temp[i])  #获得两者距离
        if dis_r<min_dis:
            min_dis=dis_r
            t=i     #记录该记录位置

    return t

#第一个记录组迭代到，其个数大于k为止
def repeat_k(r,i):
    n=1
    while(n<k):
        t=find_rs(r)
        #print(temp[t])
        dict_k[i].append(temp[t])
        del temp[t]
        n=n+1
'''
#测试repeat_k
def repeat_k(r,i):
    n=1
    while(n<k):
        dict_k[i].append(temp[0])
        del temp[0]
        n=n+1
'''

def save2file():
    path = os.path.abspath('..')  # 表示当前所处的文件夹上一级文件夹
    data_path = path + '\\k-a_cluster\\result.txt'
    data_file = open(data_path, 'w')
    #lines = data_file.readlines()
    for i in dict_k:
        data_file.writelines(str(j) for j in dict_k[i])
        data_file.write('\n')

    data_file.close() 
'''
#====================================主函数
k=2
ni=0
Init()  #读入数据
while(len(temp)!=0):
    r=temp[0]
    #print(r)
    del temp[0]
    dict_k[ni]=[r]
    repeat_k(r,ni)   #迭代使记录组内个数大于k
    ni=ni+1
    
#print(len(dict_k[13]))
save2file() #保存数据
'''
























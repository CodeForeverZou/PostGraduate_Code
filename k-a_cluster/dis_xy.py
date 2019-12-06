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


dict_arc={}
father=[]
dict_vis={}

#生成边字典
def gen_dict_arc(node):
    #dict_arc[node.tag]=[i.tag for i in tree1.children(node.tag)]
    print(node.tag)
    for i in tree1.children(node.tag):
        if node.tag not in dict_arc:
            dict_arc[node.tag]=[i.tag]
        else:
            dict_arc[node.tag].append(i.tag)
        gen_dict_arc(i.tag)

gen_dict_arc(tree1.get_node(tree1.root))
'''
for i in tree1.children(tree1.root):
    print(i.tag)
'''
print(dict_arc)
        
        
        

#====================================
#print(type(tree1.get_node(tree1.root)))
#print(tree1.children(tree1.root))
#tree1.show()
#print(type(tree1.siblings('1-5')[0]))

'''
dfsls=[]
ls_temp=[]
def dfs(node):
    if ls_temp!=None:
        print(ls_temp)
    ls_temp=[]
    ls_temp.append(node.tag)
    #dfsls.append(node.tag)
    if node==None:
        return
    #
    if tree1.children(node.tag):
        dfs(tree1.children(node.tag)[0])
    else:
        for i in tree1.siblings(node.tag):
            dfs(i)
    #
    for i in tree1.children(node.tag):        
        ls_temp.append(i.tag)
        dfs(tree1.get_node(i.tag))
'''
visited={}
def traverse(node):
    #print(node.tag)
    visited[node.tag]=0
    for i in tree1.children(node.tag):
        traverse(i)

traverse(tree1.get_node(tree1.root))

def dfs(node):
    print(node.tag,'-->')
    visited[node.tag]=1;
    for v in tree1.children(node.tag):
         print(v.tag,'-->')
         if(not visited[v.tag]):
             dfs(v)

global top
global stackn
top=0
stackn={}
def pop():
    global top
    global stackn
    node=stackn[top]
    top=top-1
    return node

def push(node):
    global top
    global stackn
    top=top+1
    stackn[top]=node
    

def dfss(node):
    global top
    global stackn
    push(node)
    while(top):
        node=pop()
        print(node.tag)
        for i in tree1.children(node.tag)[::-1]:
            push(i)
        

        

#dfss(tree1.get_node(tree1.root))             
def pre(node):
    ls=[]
    stack=[node]
    if not node:
        return

    while stack:
        node=stack.pop(0)
        if node:
            print(node.tag,'-->')
            for i in tree1.children(node.tag)[::-1]:
                stack.insert(0,i)
#pre(tree1.get_node(tree1.root))               

#dfs(tree1.get_node(tree1.root))
#print(len(dfsls),tree1.size())
#print(len(tree1.paths_to_leaves()))
                
#print(i for i in tree1.rsearch('41-50',filter=None))
#print(tree1.rsearch('41-50',filter=None))

'''
def LCP(node,right,left):
    if (node is None or node==right or node==left):
        return node
    lf=LCP(node.left

#计算分类属性 内距离
#节点Nodef、x、y
Nodef=Sfather(x,y)
Nx=depth(Nodef)-depth(x)    #x到最近公共祖先要经过的节点数
Ny=depth(Nodef)-depth(y)    #y到最近公共祖先要经过的节点数

Nf=depth()-depth(Nodef)     #Nodef到根节点要经过的节点数

dis=1-[2*Nf/(Nx+Ny+2Nf)]
'''

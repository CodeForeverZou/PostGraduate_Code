import os
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

#====================================分类树 元组

#生成树的函数
def GetTrees():
    '''
    获取根据属性生成所有树
    :return: 返回所有属性的树，顺序在'attribute.txt'里面
    '''
    attribute = []
    path = os.path.abspath('..')  # 表示当前所处的文件夹上一级文件夹的绝对路径
    path1 = path + "\k-a_cluster\\data\\attribute.txt"
    infile = open(path1, 'r')
    attribute_file = infile.readline()[:-1]  # 读取一行
    attribute = (attribute_file.split(','))
    trees = []
    for i in range(len(attribute)):
        path2 = path + "\k-a_cluster\\data\\attribute_" + attribute[i]+'.txt'
        tree = Tree1()
        tree1 = tree.createTree(path2)
        trees.append(tree1)
    return trees




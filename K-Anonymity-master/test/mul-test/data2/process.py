import os

def Init():
    '''
    初始化，生成树,设置阈值，初始化要匿名的属性值
    :return: 所有数据元祖，阈值，所有属性的树
    '''
    data=[]
    #第一步：读取数据，生成元组
    path = os.path.abspath('.')  # 表示当前所处的文件夹上一级文件夹
    data_path = path + '\\data.txt'
    data_file = open(data_path, 'r')
    lines = data_file.readlines()
    for line in lines:
        i = line[:-1].split(',')
        data.append(i)
    print(data[1][1])

if __name__=="__main__":
    Init()

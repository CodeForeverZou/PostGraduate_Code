
fp=open("D:\code\python\MASK\\111.txt",'w+')

str="h3ll"
fp.write("h3ll")


fp.close()
'''
fp=open("D:\code\python\MASK\222",'r')
print(fp.readline())
print(fp.readline())
print(fp.readline())

fo = open("D:\code\python\MASK\\runoob.txt", "w+")
print ("文件名: ", fo.name)

str = "6:www.runoob.com"
# 在文件末尾写入一行
fo.seek(0, 2)
line = fo.write( str )

# 读取文件所有内容
fo.seek(0,0)
for index in range(6):
    line = next(fo)
    print ("文件行号 %d - %s" % (index, line))

# 关闭文件
fo.close()
'''

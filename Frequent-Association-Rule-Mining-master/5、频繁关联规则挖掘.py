#-*- coding:utf-8 -*-
import pandas
import copy

# =================================================定义FP-tree类==============================================
class FPTreeNode:
    def __init__(self, value, count, parent):
        self.value = value
        self.count = count
        self.parent = parent
        self.children = {}
        self.brother = None

    def describe(self, indent=1):
        print('  ' * indent, self.value, self.count)
        for child in self.children.values():
            child.describe(indent + 1)

    def increase(self, count):
        self.count += count

    def get_prefix(self):
        ret = []
        if self.parent is None:
            print("不能查找根节点的前缀！")
            return None
        count = self.count
        #print(count,'\n') 当前叶节点出现数
        node = self.parent
        while node.value is not "root":
            ret.append(node.value)
            node = node.parent
        #print(node.count) 父节点出现数
        return frozenset(ret), count

# =================================================…定义主函数…==============================================
class Solution:
    minimum_support = 150   # 最小支持度阈值（频繁项集出现次数超过150）
    min_support = 0.45      # 支持度（针对关联规则而言，是一个比例，不是出现次数）
    min_confidence = 0.9    # 置信度
    rule_dictionary = {}    # rule(frozenset([[A, B], [C, D]]))是否是强规则：{rule1: False, rule2: False, ...}
    cnt_all = 0             # 总记录数

    def create_init_set(self, data_set):
        ret = {}
        for trans in data_set:
            f_set = frozenset(trans)
            ret.setdefault(f_set, 0)
            ret[f_set] += 1
        return ret

    def create_fp_tree(self, data, k=minimum_support):
        head_table = {}  # 头指针表
        # 记录支持度
        for transaction, count in data.items():
            for item in transaction:
                # head_table[item] = head_table.get(item, 0) + 1
                if item in head_table.keys():
                    head_table[item] = head_table[item] + count
                else:
                    head_table[item] = count
        # 根据最小支持度阈值过滤
        to_delete = list(filter(lambda i: head_table[i] < k, head_table.keys()))
        for item in to_delete:
            del(head_table[item])
        '''
        keys = list(headerTable.keys())
        for k in keys:
            if headerTable[k] < minSup:
                del(headerTable[k])
        '''
        freq_item_set = set(head_table.keys())
        # 没有频繁项：直接结束
        if len(freq_item_set) == 0:
            return None, None
        # 增加头节点项
        for item in head_table.keys():
            head_table[item] = [head_table[item], None]
        ret_tree = FPTreeNode("root", 1, None)  # 初始化FP树
        # 逐事务插入树
        for transaction, count in data.items():
            local_id = {}
            for item in transaction:
                if item in freq_item_set:
                    local_id[item] = head_table[item][0]
            if len(local_id) > 0:
                # 按照单个项集的频率进行排序
                ordered_items = [v[0] for v in sorted(local_id.items(), key=lambda p: p[1], reverse=True)]
                self.update_tree(ordered_items, ret_tree, head_table, count)
        return ret_tree, head_table

    def update_tree(self, items, in_tree, header_table, count):
        if items[0] in in_tree.children:  # check if orderedItems[0] in retTree.children
            in_tree.children[items[0]].increase(count)  # increment count
        else:  # add items[0] to inTree.children
            in_tree.children[items[0]] = FPTreeNode(items[0], count, in_tree)
            if header_table[items[0]][1] is None:  # update header table
                header_table[items[0]][1] = in_tree.children[items[0]]
            else:
                self.update_header(header_table[items[0]][1], in_tree.children[items[0]])
        if len(items) > 1:  # call update_tree() with remaining ordered items
            self.update_tree(items[1:], in_tree.children[items[0]], header_table, count)

    def update_header(self, node_to_test, target_node):  # this version does not use recursion
        while node_to_test.brother is not None:  # Do not use recursion to traverse a linked list!
            node_to_test = node_to_test.brother
        node_to_test.brother = target_node
# =================================================查找元素条件模式基============================================
    def find_prefix_path(self, node):
        ret = {}
        while node is not None:
            path, count = node.get_prefix()
            ret[path] = count
            node = node.brother # 遍历下一个相同元素
        return ret
# =================================================递归查找频繁项集==============================================
    #针对字典frequent_dic操作，因为要计算支持度、置信度，所以要统计每个频繁项集出现次数，使用字典
    def mine_tree(self, header_table, prefix, frequent_dic, min_sup=minimum_support):
        #big_l = [v[0] for v in sorted(header_table.items(), key=lambda p: p[1][0])]
        sorted_headerTable = sorted(header_table.items(), key=lambda p: p[1][0])  #返回重新排序的列表。每个元素是一个元组，[（key,[num,treeNode],()）
        #print(sorted_headerTable)
        big_l = [v[0] for v in sorted_headerTable]  # 获取频繁项
        #print(big_l)
        for base_pattern in big_l:
            new_freq_set = copy.deepcopy(prefix)
            new_freq_set.add(base_pattern)
            #print(base_pattern)
            #================所有的频繁项集列表====================
            #freqItemList.append(new_freq_set)  # 所有的频繁项集列表
            f_new_freq_set = frozenset(new_freq_set)
            if f_new_freq_set in frequent_dic.keys():
                print("Error in mine_tree(): Exist!", f_new_freq_set)
            frequent_dic[f_new_freq_set] = header_table[base_pattern][0]
            #====================================
            cond_patt_bases = self.find_prefix_path(header_table[base_pattern][1])  # 获取条件模式基。就是basePat元素的所有前缀路径。它像一个新的事务集
            my_cond_tree, head = self.create_fp_tree(cond_patt_bases, min_sup)  # 创建条件FP树
            
            if head is not None:
                # print('conditional tree for:', new_freq_set)
                self.mine_tree(head, new_freq_set, frequent_dic, min_sup)
                #self.mine_tree(head, new_freq_set, freqItemList, min_sup)  # 递归直到不再有元素
    '''
    #针对列表freqItemList操作，不具备计算支持度、置信度的能力
    def mine_tree(self, header_table, prefix, freqItemList, min_sup=minimum_support):
        #big_l = [v[0] for v in sorted(header_table.items(), key=lambda p: p[1][0])]
        sorted_headerTable = sorted(header_table.items(), key=lambda p: p[1][0])  #返回重新排序的列表。每个元素是一个元组，[（key,[num,treeNode],()）
        print(sorted_headerTable)
        big_l = [v[0] for v in sorted_headerTable]  # 获取频繁项
        #print(big_l)
        for base_pattern in big_l:
            new_freq_set = copy.deepcopy(prefix)
            new_freq_set.add(base_pattern)
            #print(base_pattern)
            #================所有的频繁项集列表====================
            freqItemList.append(new_freq_set)  # 所有的频繁项集列表
            
            f_new_freq_set = frozenset(new_freq_set)
            if f_new_freq_set in frequent_dic.keys():
                print("Error in mine_tree(): Exist!", f_new_freq_set)
            frequent_dic[f_new_freq_set] = header_table[base_pattern][0]
            
            #====================================
            cond_patt_bases = self.find_prefix_path(header_table[base_pattern][1])  # 获取条件模式基。就是basePat元素的所有前缀路径。它像一个新的事务集
            my_cond_tree, head = self.create_fp_tree(cond_patt_bases, min_sup)  # 创建条件FP树
            
            if head is not None:
                # print('conditional tree for:', new_freq_set)
                #self.mine_tree(head, new_freq_set, frequent_dic, min_sup)
                self.mine_tree(head, new_freq_set, freqItemList, min_sup)  # 递归直到不再有元素
    '''
    def find_frequent_items(self, data, k=minimum_support):
        init_set = self.create_init_set(data)  # 转化为符合格式的事务集
        fp_tree, header_table = self.create_fp_tree(init_set, k)  # 形成FP树
        frequent_dic = {}
        self.mine_tree(header_table, set([]), frequent_dic, k)  # 获取频繁项集
        return frequent_dic
    
# =================================================挖掘强关联规则==============================================
    '''
    #针对民主党、共和党投票的关联规则
    def generate_rules(self, frequent_dic, min_support=min_support, min_confidence=min_confidence):
        rules = []
        # cnt = 0
        for item_list in frequent_dic.keys():
            if ('republican0' in item_list or 'democrat0' in item_list) and len(item_list) > 1:
                # print("Recursive", cnt)
                # cnt += 1
                self.generate_rules_recursive(frequent_dic, rules, [i for i in copy.deepcopy(item_list)], [], min_support, min_confidence)
        return rules
    '''
    def generate_rules(self, frequent_dic, min_support=min_support, min_confidence=min_confidence):
        print('支持度（全局）:',min_support,'置信度:', min_confidence)
        rules = []
        # cnt = 0
        for item_list in frequent_dic.keys():
            if len(item_list) > 1:
                # print("Recursive", cnt)
                # cnt += 1
                self.generate_rules_recursive(frequent_dic, rules, [i for i in copy.deepcopy(item_list)], [], min_support, min_confidence)
        return rules
    
    def generate_rules_recursive(self, frequent_dic, rules, left, right, min_support=min_support, min_confidence=min_confidence):
        for item in left:
            if item != 'republican0' and item != 'democrat0':
                # 尝试挪到right
                tmp_left = copy.deepcopy(left)
                tmp_left.remove(item)
                tmp_right = copy.deepcopy(right)
                tmp_right.append(item)
                rule = (frozenset(tmp_left), frozenset(tmp_right))
                # print("check", rule)
                if self.is_strong_rule(rule, frequent_dic):  # 若是强规则，添加，递归；若不是强规则，其子集也不是，故不再递归
                    rules.append(rule)
                    self.generate_rules_recursive(frequent_dic, rules, tmp_left, tmp_right, min_support, min_confidence)

    def is_strong_rule(self, rule, frequent_dic):
        #print(self.min_support,self.min_confidence)
        # found = False
        # if set(rule[0]) | set(rule[1]) == set(['democrat0', 'n4', 'y3', 'y8']):
        #     found = True
        if rule in self.rule_dictionary.keys():
            # print("Hit~")
            if self.rule_dictionary[rule]:
                return True
            else:
                return False
        else:
            # 考察支持度和置信度
            cnt_both = 0
            cnt_left = 0
            for item_list, cnt in frequent_dic.items():
                if rule[0] == item_list:
                    cnt_left += cnt
                    break
            for item_list, cnt in frequent_dic.items():
                if (rule[0] | rule[1]) == item_list:
                    cnt_both += cnt
                    break
            support = cnt_both / self.cnt_all
            if cnt_left==0:
                confidence=0
            else:
                confidence = cnt_both / cnt_left
            # if found:
            #     print(rule, support, confidence, self.cnt_all, cnt_both, cnt_left)
            # print(rule, support, confidence, self.cnt_all, cnt_both, cnt_left)
            if support >= self.min_support and confidence >= self.min_confidence:
                print('Found!',rule, '==>', support, confidence)
                self.rule_dictionary[rule] = True
                return True
            else:
                self.rule_dictionary[rule] = False
                return False
# =================================================函数入口==============================================
    def solve(self):
        '''
# Frequent-Association-Rule-Mining
软统课作业之频繁关联规则挖掘
现在有一份数据集A.csv，数据来自https://archive.ics.uci.edu/ml/datasets/Congressional+Voting+Records ，
每一行的第i项数据代表议员对第i个政策的投票结果记为ni或yi或?i
请根据数据集的描述（https://archive.ics.uci.edu/ml/machine-learning-databases/voting-records/house-votes-84.names ），
读取数据集提取出minimum_support为150时的频繁项集，然后求出此时支持度大于等于0.45，置信度大于等于0.9的，
以包含republican0或democrat0为左边的关联规则。如：['y3', 'democrat0'] => ['n4']
结果返回格式为：[[['democrat0'], ['n4']], [['y3', 'democrat0'], ['n4']], …… ]
        '''
        '''
        data = pandas.read_csv("A.csv")
        self.cnt_all = len(data.index)
        frequent_dic = self.find_frequent_items(data.values)  # 获取频繁项集
        #print(len(frequent_dic), frequent_dic)
        rules = self.generate_rules(frequent_dic)
        ret = list(set(rules))
        #print(len(ret), ret)
        for i in ret: print(i[0],'==>',i[1])
            
        '''
        # 简易数据集测试
        simple_data=[
    ['milk','eggs','bread','chips'],
    ['eggs','popcorn','chips','beer'],
    ['eggs','bread','chips'],
    ['milk','eggs','bread','popcorn','chips','beer'],
    ['milk','bread','beer'],
    ['eggs','bread','beer'],
    ['milk','bread','chips'],
    ['milk','eggs','bread','butter','chips'],
    ['milk','eggs','butter','chips']]
        simple_data = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
        self.cnt_all = len(simple_data)
        dict_data = self.create_init_set(simple_data)  # 转化为符合格式的事务集
        fp_tree, header = self.create_fp_tree(dict_data, 3)  # 形成FP树
        '''
        列表，得不到置信度、支持度
        frequent_item = []
        self.mine_tree(header, set([]), frequent_item, 3)  # 获取频繁项集
        print(len(frequent_item), frequent_item)
        '''
        #字典，处理置信度、支持度====================================
        frequent_dic = {}
        self.mine_tree(header, set([]), frequent_dic, 3)  # 获取频繁项集
        rules = self.generate_rules(frequent_dic)
        ret = list(set(rules))
        #print(len(ret), ret)
        for i in ret: print(i[0],'==>',i[1])
        
        
        # kosarak 数据集测试
        # parsed_data = [line.split() for line in open('kosarak.dat').readlines()]
        # test_frequent = self.find_frequent_items(parsed_data, 100000)
        # print(len(test_frequent), test_frequent)

        #return ret


print("↓")
Solution().solve()
print("↑")

'''
# =================================================查找元素条件模式基===============================================
 
# 直接修改prefixPath的值，将当前节点leafNode添加到prefixPath的末尾，然后递归添加其父节点。
# prefixPath就是一条从treeNode（包括treeNode）到根节点（不包括根节点）的路径
def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)
 
# 为给定元素项生成一个条件模式基（前缀路径）。basePet表示输入的频繁项，treeNode为当前FP树中对应的第一个节点
# 函数返回值即为条件模式基condPats，用一个字典表示，键为前缀路径，值为计数值。
def findPrefixPath(basePat, treeNode):
    condPats = {}  # 存储条件模式基
    while treeNode != None:
        prefixPath = []  # 用于存储前缀路径
        ascendTree(treeNode, prefixPath)  # 生成前缀路径
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count  # 出现的数量就是当前叶子节点的数量
        treeNode = treeNode.nodeLink  # 遍历下一个相同元素
    return condPats

# =================================================递归查找频繁项集==============================================
class FPTreeNode:
    def __init__(self, value, count, parent):
        self.value = value
        self.count = count
        self.parent = parent
        self.children = {}
        self.brother = None
        
    def get_prefix(self):
        ret = []
        if self.parent is None:
            print("不能查找根节点的前缀！")
            return None
        count = self.count
        node = self.parent
        while node.value is not "root":
            ret.append(node.value)
            node = node.parent
        return frozenset(ret), count
        
    def find_prefix_path(self, node):
        ret = {}
        while node is not None:
            path, count = node.get_prefix()
            ret[path] = count
            node = node.brother
        return ret
    
'''

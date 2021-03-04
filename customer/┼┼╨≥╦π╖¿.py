list = [4,2,5,3,1,7]

# 冒泡
def maopao(list):
    for i in range(len(list)-1):
        for j in range(0,len(list)-i-1):
            if list[j] < list[j+1]:
                list[j],list[j+1] = list[j+1],list[j]
    return list
# res = maopao(list)
# print(res)

# 选择
def select(list):
    n = len(list)
    for i in range(n):
        min = i
        for j in range(i+1,n):
            if list[min] > list[j]:
                list[min],list[j] = list[j],list[min]
    return list

# res2 = select(list)
# print(res2)

# 插入
# def insert(list):
#     n = len(list)
#     for i in range(n):
#         for j in range(i+1,n):
#             if list[i] <list[j]:

sort
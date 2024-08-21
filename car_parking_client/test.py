# print('test')
str_arr = '[1, 2, 3, 4]'
# print(str_arr)
# convert str array to number array
def convert2IntArr(str_arr):
    # print(len(str_arr))
    # delete [ , ] -> 1,2,3
    sTemp = str_arr.replace('[', '').replace(']', '')
    strArr = sTemp.split(',')
    return list(map(lambda x: int(x.strip()), strArr))

prev = []

aaa = convert2IntArr(str_arr=str_arr)
prev = aaa.copy()
print(aaa, prev)
aaa.clear()
print(aaa, prev)
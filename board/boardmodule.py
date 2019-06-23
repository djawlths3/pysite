from builtins import range, len, type


def paging(nowpage, pagesize):
    if pagesize == 0:
        pagesize = 1
    print(nowpage <= 2 )
    print(pagesize >= 5)
    if nowpage <= 4:
        nowpage = 3

    li = []
    for i in range(-2, 3):
        result = nowpage + i
        if result >= 1 and result <= pagesize:
            li.append(result)
    print(li[0])
    if len(li) < 5 and li[0] > 2:
        differnce = pagesize - nowpage
        if differnce == 1:
            li.insert(0, li[0] -1 )
        elif differnce ==0:
            li.insert(0, li[0] -1 )
            li.insert(0, li[0] - 1)

    return li

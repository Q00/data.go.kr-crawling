import csv

with open('testexcel.csv', 'r', encoding= 'utf-8-sig') as f:
    rdr = csv.reader(f)
    makelist = list(rdr)

# 키 값 뽑아오기
existKey = input("is key exist? Y/N")
if existKey != "Y" and existKey != "N":
    print("wrong answer")

# 키값을 제외한 나머지 리스트
getVList = []

if existKey == "Y":
    keylist = makelist[0]
for i, line in enumerate(makelist):
    if i == 0:
        continue
    else:
        getVList.append(line)

# pk 값 뽑아오기
pkKey = input("which column is primary?")
if pkKey not in keylist:
    print("wrong column")

print("your primary key is" + pkKey)
pkIndex = keylist.index(pkKey)

#make dictionary
#getDict = dict((others[index], others) for index,others in getVList if index == pkKey)
getDict = {}
for lst in getVList:
    print(lst)
    for index,ov in enumerate(lst):
        if index == pkIndex:
            print("인덱스",index)
            print("값 ", ov)

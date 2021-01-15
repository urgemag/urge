price=2000000
List=[]
for i in (str(price)):
    List.append(i)
for x in range ((len(str(price))-1)//3):
    count = (x+1) * 3
    List.insert(len(str(price))-count,",")
print (List)
print("".join(List))
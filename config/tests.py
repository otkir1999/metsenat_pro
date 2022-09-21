class obj:
    count = 0
    def __init__(self,id,name):
       self.id = id
       self.name = name
       obj.count +=1
       print(self.id)
       print(self.name)

o1 = obj(1,'vin')
o2 = obj(2,'bini')
o3 = obj(3,'lin')
print('object called' ,obj.count)

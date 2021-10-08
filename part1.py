from collections import defaultdict

class Package:
    def __init__(self, id):
        self.id = id
        self.address = ""
        self.office = ""
        self.ownerName = ""
        self.collected = False
        self.delivered = False

class Truck:
    def __init__(self, id, n, loc):
        self.id = id
        self.size = n
        self.location = loc
        self.packages = defaultdict(list)
        self.sidelist = []

    def corrlocation(self, pk):
        if self.location == pk.office:
            return True
        elif self.location == pk.address:
            return True
        return False

    def collectPackage(self, pk):
        total = len(self.sidelist)
        if not self.corrlocation(pk):
            pk.collected = False
        if total == self.size:
            return
        if total < self.size and self.corrlocation(pk):
            pk.collected = True
            self.packages[pk.address].append(pk)
            if pk.id not in self.sidelist:
                self.sidelist.append(pk.id)
            
    def deliverOnePackage(self, pk):
        if self.corrlocation(pk) and pk.collected == True and pk.delivered == False:
            pk.delivered = True
            self.sidelist.remove(pk.id)

    def deliverPackages(self):
        for key in self.packages[self.location]:        
            key.delivered = True
            self.sidelist.remove(key.id)
                    
    def removePackage(self, pk):
        pk.collected = False
        if pk.id in self.sidelist:
            pk.office = self.location
            self.sidelist.remove(pk.id)
    
    def driveTo(self, loc):
        self.location = loc

    def getPackagesIds(self):
        return self.sidelist

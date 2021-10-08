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
            return
        if total == self.size:
            return
        if total < self.size and self.corrlocation(pk):
            pk.collected = True
            self.packages[pk.address].append(pk)
            if pk.id not in self.sidelist:
                self.sidelist.append(pk.id)
            
    def deliverOnePackage(self, pk):
        if self.corrlocation(pk) and pk.collected == True:
            self.sidelist.remove(pk.id)
            self.packages[pk.address].remove(pk)
            if self.packages[self.location] == []:
                del self.packages[self.location]
            pk.delivered = True

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

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)



def deliveryService(map, truck, packages):
    deliveredTo = {}
    adj = build_adjlist(map)
    stops = [truck.location]
    sortedbyOffice = sortPkgs(packages)
    collected_pks = []
    #print("sorted by office is", sortedbyOffice)
    for office in sortedbyOffice:   
        completeDrive(truck, adj, stops, office) 
        pksToCollect = sortedbyOffice[office]
        #print("pks to collect are", pksToCollect)
        while pksToCollect:
            collect(truck, pksToCollect, collected_pks)
            #print("truck.packages is", truck.packages)
            proceed(truck, adj, stops, deliveredTo, collected_pks)
            #print("delivered to is", deliveredTo)
            if collected_pks is None:
                break
            completeDrive(truck, adj, stops, office)
    print("stops is", stops)
    return (deliveredTo, stops) 


def proceed(truck, adj, stops, deliveredTo, collected_pks):
    for pk in collected_pks.copy():
        #print("pk is", pk)
        addr = pk[1]
        completeDrive(truck, adj, stops, addr)
        deliver(truck, deliveredTo, pk)
        collected_pks.remove(pk)
    #print("collected pks is NOW", collected_pks)
    return

def completeDrive(truck, adj, stops, destination):
    path = find_path(adj, truck.location, destination)[1:]
    for loc in path:     
        truck.driveTo(loc)
        stops.append(loc)
    return
    
def collect(truck, pksToCollect, collected_pks):
    for pk in pksToCollect.copy():
        if truck.location == pk.office and (len(truck.sidelist) < truck.size):
            truck.collectPackage(pk)
            collected_pks.append((pk.id, pk.address, pk))
            if len(collected_pks) == truck.size:
                return 
            pksToCollect.remove(pk)
        #print("collected pks are", collected_pks)
    return 

def deliver(truck, deliveredTo, pk):
    if truck.location == pk[1]:
        truck.deliverOnePackage(pk[2])
        deliveredTo[pk[0]] = pk[1]
    return 

def sortPkgs(packages):
    pkgOffice = defaultdict(list)
    for pk in packages:
        pkgOffice[pk.office].append(pk)
    return pkgOffice

def find_path(adj, source, destination):    
    status = {}
    for link in adj:
        status[link] = "unvisited"
    q = Queue()
    q.enqueue([source])
    status[source] = "visiting"
    while not q.isEmpty():
        vertex = q.dequeue()
        if vertex[-1] == destination:
            return vertex
        for n in adj[vertex[-1]]:
            if status[n] != "visited":
                status[n] = "visited"
                q.enqueue(vertex + [n])

def build_adjlist(map):
    adj = {}
    for v in map:
        source = v[0]
        destination = v[1]
        if source not in adj:
            adj[source] = []
        adj[source].append(destination)
    for v in map:
        source = v[1]
        destination = v[0]
        if source not in adj:
            adj[source] = []
        adj[source].append(destination)
    for u in adj.keys():
        adj[u].sort()
    return adj





m = [("UPS", "Brecon", 3), ("Jacob City", "Owl Ranch", 3), ("Jacob City", "Sunfield",15), ("Sunfield", "Brecon", 25)]

p = [("pk1","UPS","Brecon"),("pk2","UPS","Jacob City"),("pk3","UPS","Owl Ranch"),("pk4","UPS","Sunfield")]

truck = Truck("truck", 2, "UPS")

def setupPackages(pkgs):
    packages = []
    for row in pkgs:
        pk = Package(row[0])
        pk.office = row[1]
        pk.address = row[2]
        packages.append(pk)
    return packages


p = setupPackages(p)





















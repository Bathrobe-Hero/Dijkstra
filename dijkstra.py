infinity = 1000000
invalid_node = -1

class Node:
    previous = invalid_node
    distfromsource = infinity
    visited = False

class Dijkstra:

    def __init__(self):
        '''initialise class'''
        self.startnode = 0
        self.endnode = 0
        self.network = []
        self.network_populated = False
        self.nodetable = []
        self.nodetable_populated = False
        self.route = []
        self.route_populated = False
        self.currentnode = 0
        self.networkBackup =[]   #used to keep a backup of the network

    def populate_network(self, filename):
        '''populate network data structure'''
        try:
            fileRead = open(filename,"r")
        except IOError:
            print("File could not be opened")
            return

        fileData = fileRead.readlines()
        fileRead.close       

        for line in fileData:  #spliet the list into a 2d arry
             #remove \n at this point - single line 
            line = line.replace('\n','')     #.replace only retruns a string not edit the data
            line = line.split(",") 
            line = [int(i) for i in line] #converts line list into ints            
            self.network.append(line)       
        print (self.network)
        self.network_populated = True        
    

    def populate_node_table(self):
        '''populate node table - creats a Node for each enrty in the list network'''
        for networkLenghth in self.network:
            self.nodetable.append(Node())
        print("Node table populated")
        self.nodetable_populated = True
        self.nodetable[self.startnode].distfromsource = 0 #set the start node dis = 0 for ination
        self.nodetable[self.startnode].visited = True

    def parse_route(self, filename):
        '''load in route file'''
        try:
            fileRead = open(filename,"r")#check if file can be opend
        except IOError:
            print("File could not be opened")
            return

        fileData = fileRead.read()
        fileRead.close 
        print (fileData)        
        #remove \n at this point - single line 
        route = fileData.replace('\n','')     #.replace only retruns a string not edit the data
        route = route.split(">") 
        route[0]= route[0].upper()#forces the letter to be uppercase
        route[1]= route[1].upper()
        route[0] = ord(route[0])-65#changes the numbers to there node index      
        route[1] = ord(route[1])-65    
        print (f"{route[0]}>{route[1]}\n--------")    
        self.startnode = route[0]
        self.endnode = route[1]     
        
    def return_near_neighbour(self):
        '''determine nearest neighbours of current node'''
        nearestNbr = []        
        for nbr in range(len(self.network[self.currentnode])):
            if  self.network[self.currentnode][nbr] != 0:#check is the current disnbr is less thena current and is not a 0
                if self.nodetable[nbr].visited == False:#checks the node hasent been visted yet
                    nearestNbr.append(nbr)                     
        return (nearestNbr)#retruns the list with the node number

    def calculate_tentative(self):
        '''calculate tentative distances of nearest neighbours'''
        
        for nearestNbr in self.return_near_neighbour():
            newDiss = self.nodetable[self.currentnode].distfromsource + self.network[self.currentnode][nearestNbr]
            if newDiss < self.nodetable[nearestNbr].distfromsource:
                self.nodetable[nearestNbr].distfromsource = newDiss
                self.nodetable[nearestNbr].previous = self.currentnode
                

    def determine_next_node(self):
        '''determine next node to examine'''
        self.calculate_tentative()
        CurrentShortest = infinity
        currentNext = invalid_node
        for CNode in range(len(self.nodetable)):
            if self.nodetable[CNode].distfromsource < CurrentShortest and self.nodetable[CNode].visited == False:#check for shotest dients to next node
                currentNext = CNode
                CurrentShortest = self.nodetable[CNode].distfromsource 
        return(currentNext)#retruns next node number
      
    def calculate_shortest_path(self):
        '''calculate shortest path across network'''
        self.currentnode = self.startnode
        
        while self.currentnode != self.endnode:#keeps looping unill we reach end node
            tempnode = self.determine_next_node()
            if self.currentnode == tempnode:#if theres no movemnt
                print ("no movent")
                break
            else:
                self.currentnode = tempnode
                self.nodetable[self.currentnode].visited = True
        return()

    def return_shortest_path(self):
        '''return shortest path as list (start->end), and total distance'''
        self.calculate_shortest_path()
        path = [self.endnode]
        self.currentnode = self.endnode
        while self.currentnode != self.startnode:
            self.currentnode = self.nodetable[self.currentnode].previous
            path.append(self.currentnode)
        return(path)       


class MaxFlow(Dijkstra):    
     
    def reset_visted(self):#restes visted and disance for loop thoru the same node table
        for CNode in self.nodetable:
            CNode.visited = False
            CNode.distfromsource = infinity
        self.nodetable[self.startnode].distfromsource = 0 #set the start node dis = 0 for ination
        self.nodetable[self.startnode].visited = True


    def network_Copy(self): # creates a backup copy of self.network
        for node in self.network:
            temp = []
            for point in node:
                temp.append(point)
            self.networkBackup.append(temp)
        return self.networkBackup  

    def max_flow(self): 
        #inislaeation of max flow data
        self.populate_network(filename)
        self.parse_route(fileroute)  
        self.populate_node_table() 
        path = self.return_shortest_path()


        #change network[] for each node used on the route. lower by lowest conection on the route
        lowestFlow = infinity
        totalFlow = 0 #how much data has flown throu the nextwork#
        #if the path retruns empity then max flow reached        
        self.networkBackup = self.network_Copy()#creates a backup  
        
        while (lowestFlow !=0): #loop untill no movent. 
            self.reset_visted()
            path = self.return_shortest_path() 
            lowestFlow = infinity #lowest flow in the route

            for CNPath in path: #loops throuh current path                                        
                if lowestFlow > self.network[CNPath][self.nodetable[CNPath].previous] and CNPath != self.startnode:#check the flow of between the currentnode and preivest node agients the current lowest flow
                    lowestFlow = self.network[CNPath][self.nodetable[CNPath].previous]
                
            totalFlow += lowestFlow
            for CNPath in path: #loops throuh current path to remove that paths lowest flow
                if CNPath != self.startnode:
                    self.network[CNPath][self.nodetable[CNPath].previous] -=lowestFlow
                    self.network [self.nodetable[CNPath].previous] [CNPath]-=lowestFlow #removes forawrd conection

            if (lowestFlow!=0):
                pathLetter = []
                for p in path:
                    pathLetter.append(chr(p + 65))
                print(f"path in maxflow:{pathLetter}")
                print(f"path flow:{lowestFlow}")   
                
        self.nodetable = [] #cleans out nodetable and retets
        self.populate_node_table
        return totalFlow

if __name__ == "__main__":
    filename = "network.txt"
    fileroute = "route.txt"
    print("-------------Dijkstra-------------")  
    D = Dijkstra()    
    D.populate_network(filename)
    D.parse_route(fileroute)  
    D.populate_node_table()      
    path = D.return_shortest_path()
    pathLetter =[]
    for n in path:
        pathLetter.append(chr(n + 65))
      
    print(f"path:{str(path)}")    
    print(f"path:{pathLetter}")
    distance = 0
    for p in path:
        distance += D.network[p][D.nodetable[p].previous]
        
    print(f"distance:{distance} \n-------------Max flow-------------")
    MF = MaxFlow()
    print(f"total max flow: {MF.max_flow()}")
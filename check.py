class Graph():
    def __init__(self, V:int, E:set[tuple[int,int]], color:int) -> None:
        """
        頂点:1,...,V
        辺:隣接リスト
        色:1,...,k
        として保存
        """
        self.V = {v for v in range(1,V+1)}
        self.adj_list = {v:set() for v in range(1,V+1)}
        self.color = color
        for u,v in E:
            self.adj_list[u].add(v)
            self.adj_list[v].add(u)
        self.colorings = self.get_colorings(dict())
    
    def get_colorings(self, coloring):
        ret = []
        uncolored = self.V - set(coloring.keys())
        if not uncolored:
            return [coloring]
        v = uncolored.pop()
        for c in range(1,self.color+1):
            for w in self.adj_list[v]:
                if w in coloring and coloring[w] == c:
                    break
            else:
                ret+=self.get_colorings(coloring | {v:c})
        return ret
        
        
def main():
    G = Graph(3,{(1,2),(2,3)},3)
    print(G.colorings)

if __name__ == "__main__":
    main()



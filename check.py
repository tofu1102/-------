from collections import deque
from copy import deepcopy
import graphviz
import random
from itertools import combinations

COLOR_CODE = [
    '#1f77b4',
    '#ff7f0e',
    '#2ca02c',
    '#d62728',
    '#9467bd',
    '#8c564b',
    '#e377c2',
    '#7f7f7f',
    '#bcbd22',
    '#17becf'
    ]

class Graph():
    def __init__(self, V:int, E:set[tuple[int,int]], color:int, colorList = None) -> None:
        """
        頂点:1,...,V
        辺:隣接リスト
        色:1,...,k
        として保存
        """
        self.V = {v for v in range(1,V+1)}
        self.adj_list = {v:set() for v in range(1,V+1)}
        self.edge_list = E
        self.color = color

        if colorList == None:
            self.colorList = {i:{c for c in range(1, self.color + 1)} for i in self.V}
        else:
            self.colorList = colorList
        
        for u,v in E:
            self.adj_list[u].add(v)
            self.adj_list[v].add(u)
        self.colorings = set(self.get_colorings(Coloring((None for _ in range(V)))))
    
    def components_size(self, recolorble_set):
        sol = self.solution_space(recolorble_set)
        for i, (component, edges) in enumerate(sol):
            print(f"Component{i}:{len(component)}")
    
    def get_colorings(self, coloring):
        ret = []
        uncolored = {i+1 for i,v in enumerate(coloring) if v == None}
        if not uncolored:
            return [coloring]
        v = uncolored.pop()
        for c in self.colorList[v]:
            for w in self.adj_list[v]:
                if coloring[w] == c:
                    break
            else:
                new_coloring = list(coloring)
                new_coloring[v-1] = c
                new_coloring = Coloring(new_coloring)
                ret+=self.get_colorings(new_coloring)
        return ret
    
    def solution_space(self, recolorble_set):
        """
        解空間を連結成分ごとに列挙
        """
        #扱いやすいようにrecolorble_setを隣接リストの形に変更
        recolorble = {i:set() for i in range(1,self.color + 1)}
        for c1, c2 in recolorble_set:
            recolorble[c1].add(c2)
            recolorble[c2].add(c1)
        
        colorings = deepcopy(self.colorings)
        sol = []
        while colorings:
            source = colorings.pop()
            q = deque([source])
            component = set([source])
            edges = []
            while q:
                current_coloring = q.popleft()
                for v in self.V:
                    for c in recolorble[current_coloring[v]] & self.colorList[v]:
                        new_coloring = list(current_coloring)
                        new_coloring[v-1] = c
                        new_coloring = Coloring(new_coloring)
                        if new_coloring in colorings:
                            edges.append((current_coloring, new_coloring))
                            component.add(new_coloring)
                            q.append(new_coloring)
                            colorings.remove(new_coloring)
            sol.append((component, edges))
        return sol
    
    def visualize(self, recolorble_set):
        sol = self.solution_space(recolorble_set)
        g = graphviz.Graph(format='pdf', filename='test')
        g.attr(compound = 'true', fontname="MS Gothic")

        with g.subgraph(name="clusterR") as R:
            for c in range(1,self.color + 1):
                R.node(name=str(c), label="", fillcolor = COLOR_CODE[c], style = "filled")
            R.edges(map(lambda x:(str(x[0]),str(x[1])),recolorble_set))
            R.attr(label = "Recolorbility Graph")
            
        for i,(component, edges) in enumerate(sol):
            with g.subgraph(name = f"cluster{i}") as C:
                for coloring in component:
                    with C.subgraph(name = "cluster"+"".join(map(str,coloring))) as c:
                        for v in self.V:
                            c.node(f"{v}_{coloring}", label=f"{v}",fillcolor = COLOR_CODE[coloring[v]], style = "filled")
                        for u,v in self.edge_list:
                            c.edge(f"{u}_{coloring}", f"{v}_{coloring}")
                C.attr(penwidth = "5", pencolor = "#00ff00")
                
                for c1,c2 in edges:
                    g.edge(f"1_{c1}", f"1_{c2}", ltail='cluster'+''.join(map(str,c1)), lhead='cluster'+''.join(map(str,c2)))
        g.view()

    @classmethod
    def path(cls, V, color):
        """
        頂点数Vのパスを生成する
        """
        E = {(i,i+1) for i in range(1,V)}
        return cls(V, E, color)
    
    @classmethod
    def random_tree(cls, V, color):
        """
        たまに描画がバグる
        """
        if V <= 2:
            return cls.path(V,color)
        E = set()
        E.add((1,2))
        for v in {i for i in range(3,V+1)}:
            E.add((v,random.randint(1,v-1)))
        print(E)
        return cls(V,E,color)
    
    @classmethod
    def random_graph(cls, V, color, ratio = 0.5):
        """
        辺がratioの確率で引かれているグラフ
        """
        E = set()
        for u,v in combinations(range(1,V+1),2):
            if ratio > random.random():
                E.add((u,v))
        print(E)
        return cls(V,E,color)
    
    @classmethod
    def cycle(cls, V, color):
        """
        頂点数Vのサイクルを生成する
        """
        E = {(i,i+1) for i in range(1,V)}
        E.add((1,V))
        return cls(V, E, color)
    @classmethod
    def binary_tree(cls, height, color):
        V = pow(2,height + 1) - 1
        E = [{i, i//2} for i in range(1, V + 1) if i // 2 > 0]
        return cls(V, E, color)



class Coloring(tuple):
    """
    0-indexだとちょっと都合が悪いから1-indexにするだけ
    """
    def __getitem__(self, key):
        return super().__getitem__(key - 1)

        
def main():
    G = Graph(3, {(1,2),(2,3)}, 4)
    G.visualize({(1,2), (2,3), (3,4), (4, 1)})
    

if __name__ == "__main__":
    main()



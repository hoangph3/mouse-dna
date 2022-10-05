"""
Display load of each CPU in a cluster of nodes, using PySimpleGUI.

A Cluster object contains multiple ClusterNode objects, which in turn
contains multiple NodeCPU objects.

The window layout is: [[<node1 frame>, ..., <nodeN frame>]]
which may be broken up into sublists for multiple rows (NODES_PER_ROW).
A node frame layout is: [[<cpu1 graph>, ..., <cpuN graph>]]
where each CPU graph object is a PySimpleGUI Graph (canvas).

To simulate a real cluster, the load numbers are generated randomly
and vary gradually from interval to interval.
"""

from random import randint
import PySimpleGUI as psg

NODES_PER_CLUSTER = 12
CPUS_PER_NODE = 4

NODES_PER_ROW = 4

graphsize = (30, 100)
colors = ("red", "green", "yellow", "blue")

class NodeCPU:
    """Create an CPU object and define the Graph layout"""
    def __init__(self, num):
        self.color = colors[num]
        self.graph = psg.Graph(graphsize, (0, 0), graphsize)
        self._load = 0

    @property
    def load(self):
        """Adjust the load randomly, bound between 0 and 100"""
        self._load += randint(-5, 5)
        self._load = max(0, min(self._load, 100))
        return self._load

    def update_graph(self):
        """Update the graph, shifting the display to the left"""
        self.graph.Move(-1, 0)
        self.graph.DrawLine((graphsize[0], 0), (graphsize[0], self.load),
                            width=1, color=self.color)

class ClusterNode:
    """A ClusterNode consists of CPUs and defines the frame layout"""
    def __init__(self, num):
        self.name = f"node{num+1:02d}"
        self.cpus = [NodeCPU(cpu) for cpu in range(CPUS_PER_NODE)]
        self.frame = psg.Frame(self.name,
                              [[cpu.graph for cpu in self.cpus]],
                              title_location="n")

    def __len__(self):
        return len(self.cpus)

    def __getitem__(self, index):
        return self.cpus[index]

class Cluster:
    """A Cluster consists of ClusterNodes and defines the window layout"""
    def __init__(self):
        # set global options
        psg.theme("Black")
        psg.SetOptions(element_padding=(0, 0))
        self.nodes = [ClusterNode(node) for node in range(NODES_PER_CLUSTER)]
        self.layout = [self[node].frame for node in range(NODES_PER_CLUSTER)]
        # split the layout into multiple rows
        self.layout = self.split_list(self.layout, NODES_PER_ROW)
        self.window = psg.Window("Cluster CPU Load", self.layout,
                                resizable=False, grab_anywhere=True)
        self.window.Finalize()

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, index):
        return self.nodes[index]

    @staticmethod
    def split_list(lst, elements):
        """Split a list into sublists of 'n' elements"""
        if not isinstance(elements, int) or elements < 1:
            raise ValueError("sublist size must be int > 0")
        return [lst[i:i+elements] for i in range(0, len(lst), elements)]


def main():
    clust = Cluster()

    # event loop; show half the nodes each loop for better performance
    odds = True
    while True:
        event, values = clust.window.read(timeout=75)
        if event == psg.WIN_CLOSED:
            break
        for node in clust[odds::2]:
            for cpu in node:
                cpu.update_graph()
        odds = not odds
    clust.window.close()

if __name__ == "__main__":
    main()


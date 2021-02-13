"""
This program creates a assignment graph given a graph G with pebbling assignment 
(S_G).

"""

from pygraphviz import *
from networkx import *
"""
from copy import *
from threading import *
"""

def displayCycles(assignment_graph, root):
    #see NetworkX docs for description of the cycle_basis function
    #Note: there is also a minimum_cycle_basis function
    cycles = cycle_basis(assignment_graph, root)     
    print("\n\n\n")
    for i in cycles:
        print("-"*50)
        print("\n")
        print(len(i))
        if (len(i) == 6 or len(i) == 8):
            print(i)
        print("\n")
        print("\n")

    return

def assignPebbles(graph):
    assignment = dict()
    for i in range(len(graph.nodes())):
        if (i==0):
            assignment[graph.nodes()[i]] = 2
        else:
            assignment[graph.nodes()[i]] = 1 
    
    return assignment

def binaryEncode(assignment):
    encoding = []
    for key in assignment:
        encoding.append(assignment[key])
        
    return str(encoding)


def createAssignmentGraph(assignment, assignment_graph, graph, level, parent, assignment_graph_dict):
    """
    level is the number of pebbles at each level of the assignment graph
    assignment -- dictionary of the pebbling assignment of the current assignment 
                  graph node
    node_list -- list of assignment_graph_nodes (which are dictionaries)
    graph     -- graph on which we are playing the pebbling game 
    node_num  -- an index to uniquely label each node in the assignment graph
    assignment_graph  -- AGraph() object (object?)
    
    """
    if level == 1:
        print("Level is 1!!!")
        """
        if (len(assignment_graph.neighbors(str(parent))) == 1):
            assignment_graph.delete_node(parent)
        return 
        """
    else:
        for key in assignment:
            if assignment[key] == 2:
                for i in range(len(graph.neighbors(key))):
                    assignment_graph_node = dict(assignment) 
                    assignment_graph_node[key] = 0
                    assignment_graph_node[graph.neighbors(key)[i]] += 1
                    child = (level - 1, binaryEncode(assignment_graph_node)) 
                    #print("Number of pebbles: ", level, "\n", assignment_graph_node, "\t", assignment, "\t parent", parent, "\t child", child)
                    assignment_graph.add_edge(str(parent), str(child))
                    assignment_graph_dict[child] = assignment_graph_node
                    print("ASSIGNMENT GRAPH DICT \t", assignment_graph_dict)

                    createAssignmentGraph(assignment_graph_node, assignment_graph, graph, level-1, child, assignment_graph_dict)

    
    return
    
def main():
    dot_file = input("\n Input dot file name:  ")
    output_file_name = input("\n dot file for assignment graph:  ")
    G=AGraph(dot_file)
    S_G = assignPebbles(G)
    print(S_G)
    pebbles = len(G.nodes()) + 1
    print("Number of pebbles to start: ", pebbles)
    S_G_brack = AGraph()
    binary_S_G = binaryEncode(S_G)
    S_G_brack.add_node(str((pebbles,binary_S_G)))
    assignment_graph_dict = {(pebbles,binary_S_G): S_G}
    createAssignmentGraph(S_G, S_G_brack, G, pebbles, (pebbles,binary_S_G), assignment_graph_dict)
    print("\n\n\n")
    S_G_brack_net = nx_agraph.from_agraph(S_G_brack)
    displayCycles(S_G_brack_net, str((pebbles,binary_S_G))) 
    S_G_brack.write(output_file_name)


main()


#! python

import re

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))
        
def testInput():
    return [
        "light red bags contain 1 bright white bag, 2 muted yellow bags.",
        "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
        "bright white bags contain 1 shiny gold bag.",
        "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
        "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
        "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
        "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
        "faded blue bags contain no other bags.",
        "dotted black bags contain no other bags."
    ]

container_re = re.compile(r'^(?P<container>[a-z ]+) bags contain(?P<rest>.*)$')
other_bagsre    = re.compile(r'^ (?P<num>\d+) (?P<bagtype>[a-z ]+) bags?(?P<ending>[\.,])(?P<rest>.*)$')
no_other_bagsre = re.compile(r'^ no other bags.$')
def parse_contents( line ):
    container_match = container_re.match(line)
    if container_match:
        if no_other_bagsre.match( container_match['rest'] ):
            return ( container_match['container'], None )
        else:
            rest = container_match['rest']
            container = {}
            while len(rest) > 0:
                match = other_bagsre.match( rest )
                assert match is not None, rest
                container[match['bagtype']] = match['num']
                rest = match['rest']
            return ( container_match['container'], container )

def add_node(graph, type):
    if type not in graph['nodes']:
        graph['nodes'].add(type)

def add_edge(graph, from_type, to_type, cost):
    assert (from_type,to_type) not in graph['edges']
    graph['edges'][(from_type,to_type)] = int(cost)

def parse_graph( input ):
    graph = {}
    graph['nodes'] = set()
    graph['edges'] = {}
    
    for line in input:
        (container,containees) = parse_contents( line )
        add_node(graph, container)                
        if containees is not None:
            for type in containees:
                add_node(graph, type)
                add_edge(graph, container, type, containees[type])
    return graph

def find_edges_from( graph, start ):
    for edge in graph['edges']:
        if edge[0] == start:
            yield edge

graph = parse_graph(readInput())
#print(graph)

num_bags = 0
bags = [('shiny gold', 1)]

for bag in bags:
    for edge in find_edges_from( graph, bag[0] ):
        #print(edge, graph['edges'][edge])
        bags += [ (edge[1], bag[1]*graph['edges'][edge] ) ]
        #print( bags )
        num_bags += ( bag[1] * graph['edges'][edge] )

print(num_bags)


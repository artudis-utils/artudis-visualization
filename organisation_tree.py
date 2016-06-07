#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import click
import collections
import os
import pygraphviz as pgv
import pprint

Org = collections.namedtuple('Org', 'id, name, link')

@click.command()
@click.argument('filename', nargs=1, type=click.File('r'))
def create_tree(filename):
    """Process an artudis organisations json file. 
       Create a tree viz."""

    graph=pgv.AGraph(overlap="false", directed=True, rankdir="RL", ranksep="0.5", dpi="120")

    # set some default node attributes
    graph.node_attr['style']='filled'
    graph.node_attr['shape']='oval'
    graph.node_attr['fillcolor'] = 'aliceblue'
    graph.node_attr['fontname']='Nimbus Sans'
    graph.edge_attr['fontname']='Nimbus Sans'

    # Add all orgs
    for line in filename:
        json_org = json.loads(line)
        org = Org(json_org['__id__'], json_org["name"], "https://carleton.artudis.com/org/{}/".format(json_org["__id__"])) 
        graph.add_node(org.id, label=org.name)

    filename.seek(0)

    # Add edges
    for line in filename:
        json_org = json.loads(line)     
        for relation in json_org['relation']:
            if relation['organisation'] != None:                
                graph.add_edge(json_org['__id__'], relation['organisation'].split(":")[1], label=relation['role'])
    
    print(graph.string()) # print to screen
    graph.write('orgs.dot') # write to simple.dot
    graph.draw('orgs.png', prog='dot') # draw png

if __name__ == '__main__':
    create_tree()

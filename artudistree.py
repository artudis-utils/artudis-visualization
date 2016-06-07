#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import click
import os
import pygraphviz as pgv

@click.command()
@click.option('--orgs', required=True, show_default=True, 
               type=click.File('r', encoding='utf-8'), 
               help="Organisation export JSON file from Artudis.")
@click.option('--people', show_default=True, required=False,
               type=click.File('r', encoding='utf-8'), 
               help="Person export JSON file from Artudis.")
@click.option('--output', required=True, show_default=True, 
              type=click.Path(dir_okay=False, writable=True, resolve_path=True), 
              help="Output image file.", 
              default="output.png")
@click.option('--rankdir', show_default=True, 
               help="Direction of graph layout: TB, BT, RL, LR.", 
               default="RL")
@click.option('--dpi', show_default=True, 
               help="Ouput pixels per inch.", 
               default=50)
@click.option('--orgfillcolor', 
               help="Fill color for org nodes.", 
               default='aliceblue')
@click.option('--orgedgecolor',  
               help="Color for org relationship edges.", 
               default='navy')
@click.option('--personfillcolor',  
               help="Fill color for person nodes.", 
               default='darkolivegreen1')
@click.option('--personedgecolor', 
               help="Color for person relationship edges.", 
               default='darkgreen')
def create_tree(orgs, people, output, rankdir, dpi, 
                orgfillcolor,orgedgecolor, personfillcolor, personedgecolor):
    """Process an artudis organisations and (optionally) a person json file. 
       Create a tree visualization from the relationships."""
    
    # Create a directed graph, with no overlaps. 
    graph=pgv.AGraph(overlap="false", directed=True, 
                     rankdir=rankdir, ranksep="0.1", dpi=str(dpi))

    # Set some default node attributes.
    graph.node_attr['style']='filled'
    graph.node_attr['shape']='oval'
    graph.node_attr['fontname']='Nimbus Sans'
    graph.edge_attr['fontname']='Nimbus Sans'

    # Add all the orgs to the graph, as nodes.
    for line in orgs:
        json_org = json.loads(line)
        graph.add_node("o"+json_org['__id__'], 
                       label=json_org["name"], 
                       fillcolor=orgfillcolor)

    # Move the cursor back to the beginning of the file.
    orgs.seek(0)

    # Add relationships as edges.
    for line in orgs:
        json_org = json.loads(line)     
        for relation in json_org['relation']:
            if relation['organisation'] != None:                
                graph.add_edge("o"+json_org['__id__'], 
                               "o"+relation['organisation'].split(":")[1], 
                               label=relation['role'], 
                               color=orgedgecolor)

    # If applicable, add people.               
    if people: 
        for line in people:
            json_person = json.loads(line)
            graph.add_node("p"+json_person['__id__'], 
                           label=json_person["family_name"]+", "+
                                 json_person["given_name"], 
                           fillcolor=personfillcolor)
        
        # Move the cursor back to the beginning of the file.
        people.seek(0)
        
        # Add edges
        for line in people:
            json_person = json.loads(line)     
            for affiliation in json_person['affiliation']:
                if affiliation['organisation'] != None:                               
                    graph.add_edge("p"+json_person['__id__'], 
                                   "o"+affiliation['organisation'].split(":")[1], 
                                   label=affiliation['role'], 
                                   color=personedgecolor)

    graph.draw(output, prog='dot') 

if __name__ == '__main__':
    create_tree()

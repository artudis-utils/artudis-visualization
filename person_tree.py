#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import click
import collections
import os
import pygraphviz as pgv
import pprint

Org = collections.namedtuple('Org', 'id, name, link')
Person = collections.namedtuple('Person', 'id, familyname, givenname, link')

@click.command()
@click.option('--orgfile', nargs=1, required=True, type=click.File('r'))
@click.option('--personfile', nargs=1, required=True, type=click.File('r'))
def create_tree(orgfile, personfile):
    """Process an artudis organisations and person json file. 
       Create a tree viz."""

    graph=pgv.AGraph(overlap="false", directed=True, rankdir="RL", ranksep="0.1", dpi="50")

    # set some default node attributes
    graph.node_attr['style']='filled'
    graph.node_attr['shape']='oval'
    graph.node_attr['fontname']='Nimbus Sans'
    graph.edge_attr['fontname']='Nimbus Sans'

    # Add all orgs
    for line in orgfile:
        json_org = json.loads(line)
        org = Org("o"+json_org['__id__'], json_org["name"], "https://carleton.artudis.com/org/{}/".format(json_org["__id__"])) 
        if org.name == "Carleton Univesity":
            graph.add_node(org.id, label=org.name, root=True)
        else:
            graph.add_node(org.id, label=org.name, fillcolor='aliceblue')

    orgfile.seek(0)

    # Add edges
    for line in orgfile:
        json_org = json.loads(line)     
        for relation in json_org['relation']:
            if relation['organisation'] != None:                
                graph.add_edge("o"+json_org['__id__'], "o"+relation['organisation'].split(":")[1], label=relation['role'], color='navy')


    # Add People

    # Add all orgs
    for line in personfile:
        json_person = json.loads(line)
        person = Person("p"+json_person['__id__'], json_person["family_name"], json_person["given_name"], "https://carleton.artudis.com/ppl/{}/".format(json_person["__id__"])) 
        graph.add_node(person.id, label=person.familyname+", "+person.givenname, fillcolor='darkolivegreen1')

    personfile.seek(0)

    # Add edges
    for line in personfile:
        json_person = json.loads(line)     
        for affiliation in json_person['affiliation']:
            if affiliation['organisation'] != None:                               
                graph.add_edge("p"+json_person['__id__'], "o"+affiliation['organisation'].split(":")[1], label=affiliation['role'], color='darkgreen')

    graph.write('people.dot') 
    graph.draw('people.png', prog='dot') 

if __name__ == '__main__':
    create_tree()

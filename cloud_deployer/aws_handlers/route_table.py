#!/usr/bin/env python

#import modules
import csv

#Create route tables
def rt_create(awsc, my_csv, archi, tags=None):
    #open csv file and read each row as dictionary 
    rt_file =  open(my_csv, 'rb')
    rt_reader = csv.DictReader(rt_file)
            
    print "##########################    Starting route tables creation         ###############################" 
    if 'rt' not in archi:
        archi['rt'] = {}
        
    #iterate through rows checking for route tables to create
    for rt_dict in rt_reader:
        if rt_dict['route_table'] not in archi['rt']:
            rt = awsc.create_route_table(vpc_id=archi['vpc'][rt_dict['vpc']], dry_run=False)
            rt.add_tag("Name", rt_dict['route_table'])
            rt.add_tag("Group", rt_dict['vpc'])
            rt.add_tags(tags)
            archi['rt'][rt_dict['route_table']]  = rt.id
            print rt_dict['route_table'] + " created"
    print "done creating route tables :) "
    return archi
    
#Create routes
def route_create(awsc, my_csv, archi, tags=None):
    #open csv file and read each row as dictionary
    route_file =  open(my_csv, 'rb')
    route_reader = csv.DictReader(route_file)
            
    print "##########################    Starting routes creation         ###############################" 
    if 'route' not in archi:
        archi['route'] = {}
    #iterate through rows checking for routes types
    for route_dict in route_reader:
        if route_dict['route_type']=='peering':
            route = awsc.create_route(route_table_id=archi['rt'][route_dict['route_table']], destination_cidr_block=route_dict['cidr'], vpc_peering_connection_id=archi['peering'][route_dict['route']], dry_run=False)
            print route_dict['route'] + " created for route table " + route_dict['route_table']
        if route_dict['route_type']=='instances':
            route = awsc.create_route(route_table_id=archi['rt'][route_dict['route_table']], destination_cidr_block=route_dict['cidr'], instance_id=archi['instance'][route_dict['route']], dry_run=False)
            print route_dict['route'] + " created for route table " + route_dict['route_table']
    print "done creating routes :) "
    return archi
#!/usr/bin/env python

#import modules
import csv
from neutronclient.v2_0 import client as neutronclient

#Create route tables
def rt_create(credentials, my_csv, archi, tags=None):
    #open csv file and read each row as dictionary 
    rt_file =  open(my_csv, 'rb')
    rt_reader = csv.DictReader(rt_file)
            
    print "##########################    Starting route tables creation         ###############################" 
    if 'rt' not in archi:
        archi['rt'] = {}    
    #iterate through rows checking for route tables to creates
    for rt_dict in rt_reader:
        if rt_dict['vpc']+'_'+rt_dict['route_table'] not in archi['rt']:
            archi['rt'][rt_dict['vpc']+'_'+rt_dict['route_table']] = []
            print rt_dict['route_table'] + " created"
        if rt_dict['route_type']!='instances':
            archi['rt'][rt_dict['vpc']+'_'+rt_dict['route_table']].append('add')
        archi['rt'][rt_dict['vpc']+'_'+rt_dict['route_table']].append(rt_dict)
    print "done creating route tables :) "
    return archi
    
#Create routes
def route_create(credentials, my_csv, routes, archi, tags=None):
    #open csv file and read each row as dictionary
    route_file =  open(my_csv, 'rb')
    route_reader = csv.DictReader(route_file)
            
    print "##########################    Starting route tables creation         ###############################" 
    #iterate through rows checking for routes types
    my_rt = []
    my_update_router = {}
    for route_dict in route_reader:
        if route_dict['route_type']=='instances':
            if route_dict['vpc'] not in my_update_router:
                my_update_router[route_dict['vpc']] = {'router':{'routes':[]}}
            if route_dict['route']+'_'+route_dict['cidr'] not in my_rt:
                my_rt.append(route_dict['route']+'_'+route_dict['cidr'])
                my_update_router[route_dict['vpc']]'router']['routes'].append({'destination':route_dict['cidr'],'nexthop':routes[route_dict['route']]})
                print str({'destination':route_dict['cidr'],'nexthop':routes[route_dict['route']]}) + " added to router " + route_dict['vpc']+'-router'
                
    for vpc in my_update_router.keys():
        neutron = neutronclient.Client(username=credentials['username'],password=credentials['password'],tenant_name=archi['vpc'][vpc],auth_url=credentials['auth_url'])
        router = neutron.update_router(archi['router'][vpc+'-router'],my_update_router[vpc])
    print "done creating routes :) "
    return archi
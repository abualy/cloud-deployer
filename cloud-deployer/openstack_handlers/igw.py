#!/usr/bin/env python

#import modules
import csv
from neutronclient.v2_0 import client as neutronclient

#write a new rule with a Cidr block reference
def igw_create(credentials, my_csv, external_pool, archi, tags=None):
    #open csv file and read each row as dictionary
    igw_file =  open(my_csv, 'rb')
    igw_reader = csv.DictReader(igw_file)
    
    print "##########################    Starting internet gateway creation         ###############################" 
    #iterate through rows checking for igws
    if 'igw' not in archi:
            archi['igw'] = {}
            
    for igw_dict in igw_reader:
        neutron = neutronclient.Client(username=credentials['username'],password=credentials['password'],tenant_name=archi['vpc'][igw_dict['vpc']],auth_url=credentials['auth_url'])        
        igw = neutron.create_router({"router": {"external_gateway_info": {"network_id": archi['network'][external_pool]}, "name": igw_dict['igw']+"-router", "admin_state_up": True}})
        print igw_dict['igw'] + " created"

        archi['igw'][igw_dict['igw']]  = igw['router']['id']
    print "done creating internet gateways :) "
    return archi
    

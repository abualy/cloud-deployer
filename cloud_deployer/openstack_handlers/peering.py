#!/usr/bin/env python

#import modules
import csv
from neutronclient.v2_0 import client as neutronclient

def peering_create(credentials, my_csv, external_pool, archi, tags=None):
    #open csv file and read each row as dictionary
    peering_file =  open(my_csv, 'rb')
    peering_reader = csv.DictReader(peering_file)
            
    print "##########################    Starting peering connection creation         ###############################" 
    if 'peering' not in archi:
        archi['peering'] = {}
        
    #iterate through rows checking for peering
    for peering_dict in peering_reader:
        neutron = neutronclient.Client(username=credentials['username'],password=credentials['password'],tenant_name=archi['vpc'][igw_dict['vpc']],auth_url=credentials['auth_url'])        
        peering = neutron.create_router({"router": {"external_gateway_info": {"network_id": archi['network'][external_pool]}, "name": peering_dict['peering']+"-router", "admin_state_up": True}})
        print peering_dict['peering'] + " created"
        archi['peering'][peering_dict['peering']]  = peering['router']['id']
    print "done creating peering connections :) "
    return archi
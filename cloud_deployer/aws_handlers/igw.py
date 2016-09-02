#!/usr/bin/env python

#import modules
import csv

#Create IGWs
def igw_create(awsc, my_csv, archi, tags=None):
    #open csv file and read each row as dictionary
    igw_file =  open(my_csv, 'rb')
    igw_reader = csv.DictReader(igw_file)
    
    print "##########################    Starting internet gateway creation         ###############################" 
    #iterate through rows checking for igws
    if 'igw' not in archi:
            archi['igw'] = {}
            
    for igw_dict in igw_reader:
        igw = awsc.create_internet_gateway(dry_run=False)
        igw.add_tag("Name", igw_dict['igw'])
        igw.add_tag("Group", igw_dict['vpc'])
        igw.add_tags(tags)
        print igw_dict['igw'] + " created"
        attach_igw = awsc.attach_internet_gateway(igw.id, archi['vpc'][igw_dict['vpc']], dry_run=False)
        print igw_dict['igw'] +" igw attachement to "+ igw_dict['vpc'] + "  state: " + str(attach_igw)
        archi['igw'][igw_dict['igw']]  = igw.id
        
        #attach main route table to igw
        route_main = awsc.get_all_route_tables(filters={'association.main':'true','vpc-id':archi['vpc'][igw_dict['vpc']]}, dry_run=False)
        assoc_main = awsc.create_route(route_table_id=route_main[0].id, destination_cidr_block='0.0.0.0/0', gateway_id=igw.id, dry_run=False)
        print igw_dict['igw'] + " associated to main route table for vpc " + igw_dict['vpc'] + " with status " + str(assoc_main)

    print "done creating internet gateways :) "
    return archi
    

#!/usr/bin/env python

#import modules
import csv

#Create a new Subnet
def subnet_create(awsc, my_csv, archi, tags=None):
    #open csv file and read each row as dictionary
    subnet_file =  open(my_csv, 'rb')
    subnet_reader = csv.DictReader(subnet_file)
    
    print "##########################    Starting subnet creation         ###############################" 
    if 'subnet' not in archi:
        archi['subnet'] = {}
        
    #iterate through rows checking for subnets
    for subnet_dict in subnet_reader:
        subnet = awsc.create_subnet(vpc_id=archi['vpc'][subnet_dict['vpc']], cidr_block=subnet_dict['cidr'], availability_zone=subnet_dict['availability_zone'], dry_run=False)
        subnet.add_tag("Name", subnet_dict['subnet'])
        subnet.add_tag("Group", subnet_dict['vpc'])
        subnet.add_tags(tags)
        print subnet_dict['subnet'] + " created"
        archi['subnet'][subnet_dict['subnet']]  = subnet.id
        if subnet_dict['route_table']:
            assoc_rt = awsc.associate_route_table(route_table_id=archi['rt'][subnet_dict['route_table']], subnet_id=subnet.id, dry_run=False)
            print subnet_dict['subnet'] + " associated to route table " + archi['rt'][subnet_dict['route_table']] + " state: " + assoc_rt
    print "done creating subnets :) "
    return archi
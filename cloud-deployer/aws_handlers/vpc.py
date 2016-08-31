#!/usr/bin/env python

#import modules
import csv

#Create a new VPC
def vpc_create(awsc, my_csv, archi, tags=None):
    #open csv file and read each row as dictionary
    vpc_file =  open(my_csv, 'rb')
    vpc_reader = csv.DictReader(vpc_file)
     
    print "##########################    Starting VPCs creation            ###############################"
    #iterate through rows checking for vpcs
    if 'vpc' not in archi:
            archi['vpc'] = {}
            
    for vpc_dict in vpc_reader:
        vpc = awsc.create_vpc(cidr_block=vpc_dict['cidr'], instance_tenancy="default", dry_run=False)
        vpc.add_tag("Name", vpc_dict['vpc'])
        vpc.add_tags(tags)
        vpc.add_tag("Group", vpc_dict['Group'])
        print vpc_dict['vpc'] + " created"
        archi['vpc'][vpc_dict['Group']] = vpc.id
        
    print "done creating vpcs :) "
    return archi
    
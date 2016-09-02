#!/usr/bin/env python

#import modules
import csv

#create peering connections
def peering_create(awsc, my_csv, archi, tags=None):
    #open csv file and read each row as dictionary
    peering_file =  open(my_csv, 'rb')
    peering_reader = csv.DictReader(peering_file)
            
    print "##########################    Starting peering connection creation         ###############################" 
    if 'peering' not in archi:
        archi['peering'] = {}
        
    #iterate through rows checking for peering connections
    for peering_dict in peering_reader:
        peering = awsc.create_vpc_peering_connection(vpc_id=archi['vpc'][peering_dict['vpc']], peer_vpc_id=archi['vpc'][peering_dict['vpc_peer']], peer_owner_id=None, dry_run=False)
        peering.add_tag("Name", peering_dict['peering'])
        peering.add_tags(tags)
        print peering_dict['peering'] + " created"
        archi['peering'][peering_dict['peering']]  = peering.id
    print "done creating peering connection :) "
    return archi
    
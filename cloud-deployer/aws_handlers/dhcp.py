#!/usr/bin/env python

#import modules
import csv

#Create Dhcp Option Sets
def dhcp_create(awsc, my_csv, archi, tags=None):
    #open csv file and read each row as dictionary
    dhcp_file =  open(my_csv, 'rb')
    dhcp_reader = csv.DictReader(dhcp_file)
    
    print "##########################    Starting dhcp options creation         ###############################" 
    #iterate through rows checking for dhcp sets
    if 'dhcp' not in archi:
            archi['dhcp'] = {}
            
    for dhcp_dict in dhcp_reader:
        reservation = awsc.get_all_instances(instance_ids=[archi['instance'][dhcp_dict['domain_server']]])
        instance = reservations[0].instances[0]
        domain_name_server = instance.private_ip_address
        dhcp = awsc.create_dhcp_options(domain_name=dhcp_dict['domain_name'], domain_name_servers=domain_name_server, dry_run=False)
        dhcp.add_tag("Name", dhcp_dict['dhcp'])
        dhcp.add_tag("Group", dhcp_dict['vpc'])
        dhcp.add_tags(tags)
        archi['dhcp'] [dhcp_dict['dhcp']] = dhcp.id
        print dhcp_dict['dhcp'] + " created"
        
    print "done creating dhcp options :) "
    return archi
    

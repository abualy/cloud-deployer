#!/usr/bin/env python

#import modules
import csv
import time
import string

#Asocciate ACLs to correspondig subnets
def acl_assoc_create(awsc, my_csv, archi, tags=None):
#open csv file and read each row as dictionary
    acl_assoc_file =  open(my_csv, 'rb')
    acl_assoc_reader = csv.DictReader(acl_assoc_file)  
    
    print "##########################    Starting ACLs association         ###############################"  
    for acl_assoc_dict in acl_assoc_reader:
        acl_assoc = awsc.associate_network_acl(network_acl_id=archi['acl'][acl_assoc_dict['acl']], subnet_id=archi['subnet'][acl_assoc_dict['subnet']])
        print acl_assoc_dict['subnet'] + " to " + acl_assoc_dict['acl'] + " with ID: " + acl_assoc
    print "done creating ACL associations :) "
    return archi


#Create ACLs
def acl_create(awsc, my_csv, archi, tags=None):
    #open csv file and read each row as dictionary
    acl_file =  open(my_csv, 'rb')
    acl_reader = csv.DictReader(acl_file)
    timer = 0            
    print "##########################    Starting ACLs creation         ###############################" 
    if 'acl' not in archi:
        archi['acl'] = {}
    if 'acl_prior_numb' not in archi:
        archi['acl_prior_numb'] = {}
    #iterate through rows checking for acl rules to create    
    for acl_dict in acl_reader:
        for acl_item in string.split(acl_dict['acl'],sep='&'):
            #if ACL not created, then create it first 
            if acl_item not in archi['acl']:
                acl = awsc.create_network_acl(vpc_id=archi['vpc'][acl_dict['vpc']])
                time.sleep(3)
                acl.add_tag("Name", acl_item)
                acl.add_tag("Group", acl_dict['vpc'])
                acl.add_tags(tags)
                print ">> >> " + acl_item + " created"
                archi['acl'][acl_item]  = acl.id
                archi['acl_prior_numb'][acl_item] = 0
            
            if acl_dict['tcp']=='*':
                if acl_dict['ingress/egress']=='ingress':
                    archi['acl_prior_numb'][acl_item] = archi['acl_prior_numb'][acl_item] + 100
                    entry = awsc.create_network_acl_entry(network_acl_id=archi['acl'][acl_item], rule_number=archi['acl_prior_numb'][acl_item], protocol=6, rule_action="allow", cidr_block=acl_dict[
                    'cidr'], egress = False, port_range_from=acl_dict['from'], port_range_to=acl_dict['to'])

                    print 'tcp' +" from: "+ acl_dict['from'] +" to: " + acl_dict['to'] + " for: " + acl_dict['cidr'] + " acl: " + acl_item + " ingress opening state: " + str(entry)
                if acl_dict['ingress/egress']=='egress':
                    archi['acl_prior_numb'][acl_item] = archi['acl_prior_numb'][acl_item] + 100
                    entry = awsc.create_network_acl_entry(network_acl_id=archi['acl'][acl_item], rule_number=archi['acl_prior_numb'][acl_item], protocol=6, rule_action="allow", cidr_block=acl_dict['cidr'], egress = True, port_range_from=acl_dict['from'], port_range_to=acl_dict['to'])
                    print 'tcp' +" from: "+ acl_dict['from'] +" to: " + acl_dict['to'] + " for: " + acl_dict['cidr'] + " acl: " + acl_item + " egress opening state: " + str(entry)

            if acl_dict['udp']=='*':
                if acl_dict['ingress/egress']=='ingress':
                    archi['acl_prior_numb'][acl_item] = archi['acl_prior_numb'][acl_item] + 100
                    entry = awsc.create_network_acl_entry(network_acl_id=archi['acl'][acl_item], rule_number=archi['acl_prior_numb'][acl_item], protocol=17, rule_action="allow", cidr_block=acl_dict['cidr'], egress = False, port_range_from=acl_dict['from'], port_range_to=acl_dict['to'])

                    print 'udp' +" from: "+ acl_dict['from'] +" to: " + acl_dict['to'] + " for: " + acl_dict['cidr'] + " acl: " + acl_item + " ingress opening state: " + str(entry)
                if acl_dict['ingress/egress']=='egress':
                    archi['acl_prior_numb'][acl_item] = archi['acl_prior_numb'][acl_item] + 100
                    entry = awsc.create_network_acl_entry(network_acl_id=archi['acl'][acl_item], rule_number=archi['acl_prior_numb'][acl_item], protocol=17, rule_action="allow", cidr_block=acl_dict['cidr'], egress = True, port_range_from=acl_dict['from'], port_range_to=acl_dict['to'])
                    print 'udp' +" from: "+ acl_dict['from'] +" to: " + acl_dict['to'] + " for: " + acl_dict['cidr'] + " acl: " + acl_item + " egress opening state: " + str(entry)
                    
            if acl_dict['icmp']=='*':
                if acl_dict['ingress/egress']=='ingress':
                    archi['acl_prior_numb'][acl_item] = archi['acl_prior_numb'][acl_item] + 100
                    entry = awsc.create_network_acl_entry(network_acl_id=archi['acl'][acl_item], rule_number=archi['acl_prior_numb'][acl_item], protocol=1, rule_action="allow", cidr_block=acl_dict['cidr'], egress = False, icmp_type='-1', icmp_code='-1')
                    print 'icmp' +" from: "+ acl_dict['from'] +" to: " + acl_dict['to'] + " for: " + acl_dict['cidr'] + " acl: " + acl_item + " ingress opening state: " + str(entry)
                if acl_dict['ingress/egress']=='egress':
                    archi['acl_prior_numb'][acl_item] = archi['acl_prior_numb'][acl_item] + 100
                    entry = awsc.create_network_acl_entry(network_acl_id=archi['acl'][acl_item], rule_number=archi['acl_prior_numb'][acl_item], protocol=1, rule_action="allow", cidr_block=acl_dict['cidr'], egress = True, icmp_type='-1', icmp_code='-1')
                    print 'icmp' +" from: "+ acl_dict['from'] +" to: " + acl_dict['to'] + " for: " + acl_dict['cidr'] + " acl: " + acl_item + " egress opening state: " + str(entry)
                
    print "done creating ACLs :) "
    return archi

#!/usr/bin/env python

#import modules
import csv
import time
from novaclient import client as novaclient

#write a new rule with a Cidr block reference
def sg_create(credentials, my_csv, archi, tags=None):
    #open csv file and read each row as dictionary
    sg_file =  open(my_csv, 'rb')
    sg_reader = csv.DictReader(sg_file)
                
    print "##########################    Starting security groups creation         ###############################" 
    if 'sg' not in archi:
        archi['sg'] = {}
        
    for sg_dict in sg_reader:
        nova = novaclient.Client(2,credentials['username'],credentials['password'],archi['vpc'][sg_dict['vpc']],credentials['auth_url'])
        if sg_dict['security_group'] not in archi['sg']:
            sg = nova.security_groups.create(sg_dict['security_group'], sg_dict['sg_description'])
            print ">> >> " + sg_dict['security_group'] + " created"
            archi['sg'][sg_dict['security_group']]  = sg.id
            
            #TODO: need to revoke egress security group (not available in Openstack API yet)
        if sg_dict['tcp']=='*':
            if sg_dict['ingress/egress']=='ingress':
                rule = nova.security_group_rules.create(archi['sg'][sg_dict['security_group']], ip_protocol='tcp', from_port=sg_dict['from'], to_port=sg_dict['to'], cidr=sg_dict['cidr'])
                print 'tcp' +" from: "+ sg_dict['from'] +" to: " + sg_dict['to'] + " for: " + sg_dict['cidr'] + " ingress opening state: " + str(rule)
            if sg_dict['ingress/egress']=='egress':
                print 'tcp' +" from: "+ sg_dict['from'] +" to: " + sg_dict['to'] + " for: " + sg_dict['cidr'] + " egress opening state: " + "egress not yet implemented"
                
        if sg_dict['udp']=='*':
            if sg_dict['ingress/egress']=='ingress':
                rule = nova.security_group_rules.create(archi['sg'][sg_dict['security_group']], ip_protocol='udp', from_port=sg_dict['from'], to_port=sg_dict['to'], cidr=sg_dict['cidr'])
                print 'udp' +" from: "+ sg_dict['from'] +" to: " + sg_dict['to'] + " for: " + sg_dict['cidr'] + " ingress opening state: " + str(rule)
            if sg_dict['ingress/egress']=='egress':
                print 'udp' +" from: "+ sg_dict['from'] +" to: " + sg_dict['to'] + " for: " + sg_dict['cidr'] + " egress opening state: " + "egress not yet implemented"

        if sg_dict['icmp']=='*':
            if sg_dict['ingress/egress']=='ingress':
                rule = nova.security_group_rules.create(archi['sg'][sg_dict['security_group']], ip_protocol='icmp', from_port=sg_dict['from'], to_port=sg_dict['to'], cidr=sg_dict['cidr'])
                print 'icmp' +" from: "+ sg_dict['from'] +" to: " + sg_dict['to'] + " for: " + sg_dict['cidr'] + " ingress opening state: " + str(rule)
            if sg_dict['ingress/egress']=='egress':
                print 'icmp' +" from: "+ sg_dict['from'] +" to: " + sg_dict['to'] + " for: " + sg_dict['cidr'] + " egress opening state: " + "egress not yet implemented"
                
    print "done creating security groups :) "
    return archi


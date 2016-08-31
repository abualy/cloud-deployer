#!/usr/bin/env python

#import modules
import csv
import time

#Create security group rules within all listed security groups
def sg_create(awsc, my_csv, archi, tags=None):
    #open csv file and read each row as dictionary
    sg_file =  open(my_csv, 'rb')
    sg_reader = csv.DictReader(sg_file)
                
    print "##########################    Starting security groups creation         ###############################" 
    if 'sg' not in archi:
        archi['sg'] = {}
    #iterate through rows checking for rules    
    for sg_dict in sg_reader:
        #if security group not created, then create it first 
        if sg_dict['security_group'] not in archi['sg']:
            sg = awsc.create_security_group(name=sg_dict['security_group'], description=sg_dict['sg_description'], vpc_id=archi['vpc'][sg_dict['vpc']], dry_run=False)
            time.sleep(3)
            sg.add_tag("Name", sg_dict['security_group'])
            sg.add_tag("Group", sg_dict['vpc'])
            sg.add_tags(tags)
            print ">> >> " + sg_dict['security_group'] + " created"
            archi['sg'][sg_dict['security_group']]  = sg.id
            
            rule = awsc.revoke_security_group_egress(group_id=sg.id, ip_protocol="-1", from_port=-1, to_port=-1, cidr_ip="0.0.0.0/0", dry_run=False)
            print sg_dict['security_group'] + " egress closing state: " + str(rule)
            
        if sg_dict['tcp']=='*':
            if sg_dict['ingress/egress']=='ingress':
                rule = awsc.authorize_security_group(group_id=archi['sg'][sg_dict['security_group']], ip_protocol='tcp', from_port=sg_dict['from'], to_port=sg_dict['to'], cidr_ip=sg_dict['cidr'], dry_run=False)
                print 'tcp' +" from: "+ sg_dict['from'] +" to: " + sg_dict['to'] + " for: " + sg_dict['cidr'] + " ingress opening state: " + str(rule)
            if sg_dict['ingress/egress']=='egress':
                rule = awsc.authorize_security_group_egress(group_id=archi['sg'][sg_dict['security_group']], ip_protocol='tcp', from_port=sg_dict['from'], to_port=sg_dict['to'], cidr_ip=sg_dict['cidr'], dry_run=False)
                print 'tcp' +" from: "+ sg_dict['from'] +" to: " + sg_dict['to'] + " for: " + sg_dict['cidr'] + " egress opening state: " + str(rule)

        if sg_dict['udp']=='*':
            if sg_dict['ingress/egress']=='ingress':
                rule = awsc.authorize_security_group(group_id=archi['sg'][sg_dict['security_group']], ip_protocol='udp', from_port=sg_dict['from'], to_port=sg_dict['to'], cidr_ip=sg_dict['cidr'], dry_run=False)
                print 'udp' +" from: "+ sg_dict['from'] +" to: " + sg_dict['to'] + " for: " + sg_dict['cidr'] + " ingress opening state: " + str(rule)
            if sg_dict['ingress/egress']=='egress':
                rule = awsc.authorize_security_group_egress(group_id=archi['sg'][sg_dict['security_group']], ip_protocol='udp', from_port=sg_dict['from'], to_port=sg_dict['to'], cidr_ip=sg_dict['cidr'], dry_run=False)
                print 'udp' +" from: "+ sg_dict['from'] +" to: " + sg_dict['to'] + " for: " + sg_dict['cidr'] + " egress opening state: " + str(rule)

        if sg_dict['icmp']=='*':
            if sg_dict['ingress/egress']=='ingress':
                rule = awsc.authorize_security_group(group_id=archi['sg'][sg_dict['security_group']], ip_protocol='icmp', from_port=sg_dict['from'], to_port=sg_dict['to'], cidr_ip=sg_dict['cidr'], dry_run=False)
                print 'icmp' +" from: "+ sg_dict['from'] +" to: " + sg_dict['to'] + " for: " + sg_dict['cidr'] + " ingress opening state: " + str(rule)
            if sg_dict['ingress/egress']=='egress':
                rule = awsc.authorize_security_group_egress(group_id=archi['sg'][sg_dict['security_group']], ip_protocol='icmp', from_port=sg_dict['from'], to_port=sg_dict['to'], cidr_ip=sg_dict['cidr'], dry_run=False)
                print 'icmp' +" from: "+ sg_dict['from'] +" to: " + sg_dict['to'] + " for: " + sg_dict['cidr'] + " egress opening state: " + str(rule)
                
    print "done creating security groups :) "
    return archi

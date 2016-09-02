#!/usr/bin/env python

#import modules
import csv
import string
import time

#Create ELBs
def elb_create(awsc, my_csv, archi, tags=None):
    #open csv file and read each row as dictionary
    elb_file =  open(my_csv, 'rb')
    elb_reader = csv.DictReader(elb_file)
    
    print "##########################    Starting elbs creation         ###############################" 
    #iterate through rows checking for elbs
    if 'elb' not in archi:
            archi['elb'] = {}
            
    for elb_dict in elb_reader:
        sg_ids = []
        for sg in string.split(elb_dict['security_groups'],sep='&'):
            sg_ids.append(archi['sg'][sg])
        subnet_ids = []
        for subnet in string.split(elb_dict['subnets'],sep='&'):
            subnet_ids.append(archi['subnet'][subnet])
        ports = []
        tmp = string.split(elb_dict['listeners'],sep='&')
        for port in tmp:
            ports.append(tuple(string.split(port,sep='$')))
        elb = awsc.create_load_balancer(name=elb_dict['elb'], listeners=ports, subnets=subnet_ids, security_groups=sg_ids, scheme='internet-facing')
        time.sleep(3)
        elb.add_tag("Name", elb_dict['elb'])
        elb.add_tag("Group", elb_dict['vpc'])
        elb.add_tags(tags)
        archi['elb'] [elb_dict['elb']] = elb.id
        print ">> >> " + elb_dict['elb'] + " created"
        
        instance_ids = []
        for instance in string.split(elb_dict['instances'],sep='&'):
            subnet_ids.append(archi['instance'][instance])
        instance_register = awsc.register_instances(load_balancer_name=elb_dict['elb'], instances=instance_ids)
        print elb_dict['instances'] + " registered to elb " + elb_dict['elb']
        
        atts = {}
        for att in string.split(elb_dict['attributes'],sep='&'):
            atts[att] = True
            
        #Create ELB policies
        policy = awsc.create_lb_policy(lb_name=elb_dict['elb'], policy_name=elb_dict['policy_name'], policy_type=elb_dict['policy_type'], policy_attributes = atts)
        print elb_dict['policy_name'] + " created with policy type " + elb_dict['policy_type']
        
        #attach policies to corresponding elbs
        for por in string.split(elb_dict['ports'],sep='&'):
            attach_policies = awsc.set_lb_policies_of_backend_server(lb_name=elb_dict['elb'], instance_port=por, policies=elb_dict['policy_name'])
            print elb_dict['elb'] + " set its policy to " + elb_dict['policy_name']
        
    print "done creating elbs :) "
    return archi
    

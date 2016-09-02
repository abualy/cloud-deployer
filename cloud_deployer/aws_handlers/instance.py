#!/usr/bin/env python

#import modules
import csv
import json
import string
import time
import os

#Create instances
def instance_create(awsc, my_csv, archi, ami_id, user_data, keys_path=None, tags=None):
    #open csv file and read each row as dictionary
    instance_file =  open(my_csv, 'rb')
    instance_reader = csv.DictReader(instance_file)
    
    print "##########################    Starting instances creation         ###############################" 
    if 'instance' not in archi:
        archi['instance'] = {}
    if 'public_ip' not in archi:
        archi['public_ip'] = {}    
    #iterate through rows checking for instances to run
    for instance_dict in instance_reader:
        if instance_dict['run'] == "YES":
            #keypair creation operation
            keys = awsc.get_all_key_pairs()
            found = False
            for k in keys:
                if k.name == instance_dict['access_key_name']:
                    found = True
                    print instance_dict['access_key_name'] + " already exists"
                    break
            if found == False:
                key = awsc.create_key_pair(instance_dict['access_key_name'], dry_run=False)
                print instance_dict['access_key_name'] + " created"
                if not os.path.exists(keys_path):
                    os.makedirs(keys_path)
                key_save = key.save(keys_path)
                print instance_dict['access_key_name'] + " saved to the specified directory with state: " + str(key_save)
            #getting secrity group ids
            sg_ids = []
            for sg in string.split(instance_dict['security_groups'],sep='&'):
                sg_ids.append(archi['sg'][sg])
            
            user_data["hostname"] = instance_dict['instance']
            user_data["roles"] = json.loads(instance_dict['roles'])
            reservation = awsc.run_instances(image_id=ami_id, key_name=instance_dict['access_key_name'], user_data=json.dumps(user_data), instance_type=instance_dict['type'], subnet_id=archi['subnet'][instance_dict['subnet']], disable_api_termination=True, private_ip_address=instance_dict['ip'], security_group_ids=sg_ids, dry_run=False) 
            instance = reservation.instances[0]
            time.sleep(3)
            instance.add_tag("Name", instance_dict['instance'])
            instance.add_tag("Group", instance_dict['vpc'])
            instance.add_tags(tags)
            print ">> >> " + instance_dict['instance'] + "." + instance_dict['vpc'] + " created"
            archi['instance'][instance_dict['instance'] + "." + instance_dict['vpc']]  = instance.id
            if instance_dict['public_ip'] == "YES": 
                if 'public_ip' not in archi:
                    archi['public_ip'] = {}
                public_ip = awsc.allocate_address(domain="vpc", dry_run=False)
                print "elastic ip " + public_ip.public_ip + " allocated"
                time.sleep(5)
                assoc_public = awsc.associate_address(instance_id=instance.id, allocation_id=public_ip.allocation_id, private_ip_address=instance_dict['ip'])
                print "elastic ip " + public_ip.public_ip + " associated to " + instance_dict['instance'] + "." + instance_dict['vpc'] + " with state: " + str(assoc_public)
                archi['public_ip'][instance_dict['instance'] + "." + instance_dict['vpc']]  = public_ip.public_ip
    
    print "done creating instances :) "
    return archi
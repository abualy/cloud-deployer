#!/usr/bin/env python

#import modules
import csv
import json
import string
import time
from novaclient import client as novaclient

#Create instances
def instance_create(credentials, my_csv, ami_id, external_pool, user_data, keys_path, archi, tags=None):
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
            nova = novaclient.Client(2,credentials['username'],credentials['password'],archi['vpc'][instance_dict['vpc']],credentials['auth_url'])
            #keypair creation operation
            keys = nova.keypairs.list()
            found = False
            for k in keys:
                if k.name == instance_dict['access_key_name']:
                    found = True
                    print instance_dict['access_key_name'] + " already exists"
                    break
            if found == False:
                key = nova.keypairs.create(instance_dict['access_key_name'])
                print instance_dict['access_key_name'] + " created"
                f = open(keys_path+"/"+instance_dict['access_key_name']+".pem", "w")
                f.write(key.private_key)
                f.close()
                print instance_dict['access_key_name'] + " saved to the specified directory"
            #getting secrity group ids
            sg_ids = []
            for sg in string.split(instance_dict['security_groups'],sep='&'):
                sg_ids.append(archi['sg'][sg])
            user_data["hostname"] = instance_dict['instance']
            user_data["roles"] = json.loads(instance_dict['roles'])
            instance = nova.servers.create(name=instance_dict['instance'], image=ami_id, flavor=instance_dict['type'], security_groups=sg_ids, userdata=json.dumps(user_data), key_name=instance_dict['access_key_name'], nics=[{"net-id": archi['network'][instance_dict['subnet']], "v4-fixed-ip": instance_dict['ip']}])
            print ">> >> " + instance_dict['instance'] + "." + instance_dict['vpc'] + " created"
            archi['instance'][instance_dict['instance'] + "." + instance_dict['vpc']]  = instance.id
            instance.lock()
            time.sleep(3)
            if instance_dict['public_ip'] == "YES": 
                if 'public_ip' not in archi:
                    archi['public_ip'] = {}
                public_ip = nova.floating_ips.create(external_pool)
                print "elastic ip " + public_ip.ip + " allocated"
                time.sleep(3)
                assoc_public = nova.servers.add_floating_ip(server=instance.id, address=public_ip.ip)
                print "elastic ip " + public_ip.ip + " associated to " + instance_dict['instance'] + "." + instance_dict['vpc'] + " Successfully "
                archi['public_ip'][instance_dict['instance'] + "." + instance_dict['vpc']]  = public_ip.ip
    
    print "done creating instances :) "
    return archi
#!/usr/bin/env python

#import modules
import csv
import time
from novaclient import client as novaclient

#Create Openstack volumes
def ebs_create(credentials, my_csv, archi, tags=None):
    #open csv file and read each row as dictionary
    ebs_file =  open(my_csv, 'rb')
    ebs_reader = csv.DictReader(ebs_file)

    print "##########################    Starting volumes creation         ###############################"
    if 'ebs' not in archi:
        archi['ebs'] = {}

    #iterate through rows checking for volumes to create
    for ebs_dict in ebs_reader:
        if ebs_dict['run'] == "YES":
            nova = novaclient.Client(2,credentials['username'],credentials['password'],archi['vpc'][ebs_dict['vpc']],credentials['auth_url'])
            ebs = nova.volumes.create(size=ebs_dict['size'], availability_zone=ebs_dict['zone'], volume_type="iscsi", display_name=ebs_dict['ebs'], display_description=ebs_dict['description'])
            status = 'creating'
            while(status != 'available'):
                print ">> >> " + ebs_dict['ebs'] + " status : "+status
                time.sleep(1)
                status = nova.volumes.get(ebs.id).status
            time.sleep(3)
            print ">> >> " + ebs_dict['ebs'] + " created"
            archi['ebs'][ebs_dict['ebs']]  = ebs.id
            attach_ebs = nova.volumes.create_server_volume(archi['instance'][ebs_dict['instance']], ebs.id, device="/dev/xvdf")
    print "done creating volumes :) "
    return archi
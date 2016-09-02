#!/usr/bin/env python

#import modules
import csv
import time

#Create EBS volumes
def ebs_create(awsc, my_csv, archi, tags=None):
    #open csv file and read each row as dictionary
    ebs_file =  open(my_csv, 'rb')
    ebs_reader = csv.DictReader(ebs_file)
    
    print "##########################    Starting ebs creation         ###############################" 
    if 'ebs' not in archi:
        archi['ebs'] = {}
        
    #iterate through rows checking for volumes to create
    for ebs_dict in ebs_reader:
        if ebs_dict['run'] == "YES":
            ebs = awsc.create_volume(size=ebs_dict['size'], zone=ebs_dict['zone'], volume_type="gp2", dry_run=False) 
            time.sleep(3)
            ebs.add_tag("Name", ebs_dict['ebs'])
            ebs.add_tag("Group", ebs_dict['vpc'])
            ebs.add_tags(tags)
            print ">> >> " + ebs_dict['ebs'] + " created"
            archi['ebs'][ebs_dict['ebs']]  = ebs.id
            attach_ebs = ebs.attach(instance_id=archi['instance'][ebs_dict['instance']], device="/dev/xvdf", dry_run=False)
    print "done creating ebs :) "
    return archi
#!/usr/bin/env python

#import modules
import csv
from keystoneclient.v2_0 import client as keystoneclient
from neutronclient.v2_0 import client as neutronclient
from novaclient import client as novaclient

#Create a new VPC 
def vpc_create(credentials, my_csv, external_pool, archi):
    #open csv file and read each row as dictionary
    vpc_file =  open(my_csv, 'rb')
    vpc_reader = csv.DictReader(vpc_file)
     
    print "##########################    Starting VPCs creation            ###############################"
    #iterate through rows checking for vpcs
    if 'vpc' not in archi:
            archi['vpc'] = {}
    if 'subnet' not in archi:
            archi['subnet'] = {}
    if 'network' not in archi:
            archi['network'] = {}        
    for vpc_dict in vpc_reader:
        keystone = keystoneclient.Client(username=credentials['username'],password=credentials['password'],tenant_name=credentials['tenant_name'],auth_url=credentials['auth_url'])
        neutron = neutronclient.Client(username=credentials['username'],password=credentials['password'],tenant_name=credentials['tenant_name'],auth_url=credentials['auth_url'])
        nova = novaclient.Client(2,credentials['username'],credentials['password'],credentials['tenant_name'],credentials['auth_url'])
        vpc = keystone.tenants.create(tenant_name=vpc_dict['vpc'],description=vpc_dict['cidr'], enabled=True)
        roles = keystone.roles.list()
        users = keystone.users.list()
        my_admin_role = [x for x in roles if x.name=='admin'][0]
        my_admin_user = [x for x in users if x.name==credentials['username']][0]
        keystone.roles.add_user_role(my_admin_user.id, my_admin_role.id, vpc.id)
        neutron.update_quota(tenant_id = vpc.id,body = {'quota': {'network':60, 'subnet':60, 'security_group': 60, 'security_group_rule': 1000, 'port':'200'}})
        nova.quotas.update(tenant_id=vpc.id ,instances=50, floating_ips=20, cores=50)
        net = neutron.list_networks(name = external_pool)
        archi['network'][external_pool]  = net['networks'][0]['id']
        subs = neutron.list_subnets(network_id = net['networks'][0]['id'])
        for sub in subs['subnets']:
            archi['subnet'][sub['name']]  = sub['id']
        print vpc_dict['vpc'] + " created"
        archi['vpc'][vpc_dict['Group']] = vpc_dict['vpc']
        archi['vpc'][vpc_dict['Group']+'_cidr'] = vpc_dict['cidr']
        
    print "done creating vpcs :) "
    return archi
    
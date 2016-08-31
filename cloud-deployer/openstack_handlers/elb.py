#!/usr/bin/env python

#import modules
import csv
import string
import time
from neutronclient.v2_0 import client as neutronclient
from novaclient import client as novaclient

#write a new rule with a Cidr block reference
def elb_create(credentials, my_csv, external_pool, archi, tags=None):
    #open csv file and read each row as dictionary
    elb_file =  open(my_csv, 'rb')
    elb_reader = csv.DictReader(elb_file)
    
    print "##########################    Starting elbs creation         ###############################" 
    #iterate through rows 
    if 'elb' not in archi:
        archi['elb'] = {}
    if 'public_ip' not in archi:
        archi['public_ip'] = {}
    for elb_dict in elb_reader:
        neutron = neutronclient.Client(username=credentials['username'],password=credentials['password'],tenant_name=archi['vpc'][elb_dict['vpc']],auth_url=credentials['auth_url'])
        nova = novaclient.Client(2,credentials['username'],credentials['password'],archi['vpc'][elb_dict['vpc']],credentials['auth_url'])
        subnets = []
        for subnet in string.split(elb_dict['subnets'],sep='&'):
            subnets.append(tuple([subnet,archi['subnet'][subnet]]))
        ports = []
        tmp = string.split(elb_dict['listeners'],sep='&')
        for port in tmp:
            ports.append(tuple(string.split(port,sep='$')))
        instance_ips = []
        for instance in string.split(elb_dict['servers'],sep='&'):
            ip = nova.servers.ips(archi['instance'][instance]).itervalues().next()[0]['addr']
            instance_ips.append(ip)
        for subnet in subnets:
            for port in ports:
                pool_name = elb_dict['elb']+ '_' + port[0]
                pool = neutron.create_pool({'pool': {'name':pool_name,'description':pool_name,'provider':'haproxy','subnet_id':subnet[1],'protocol':port[2].upper(),'lb_method':'ROUND_ROBIN','admin_state_up':True}})
                archi['elb'] [elb_dict['elb']] = pool['pool']['id']
                print ">> >> pool " + pool_name + " created"
                health = neutron.create_health_monitor({'health_monitor': {'admin_state_up': True, 'delay': 10, 'max_retries': 3, 'timeout': 10, 'type': port[2].upper()}})
                neutron.associate_health_monitor(pool['pool']['id'], {'health_monitor': {'id': health['health_monitor']['id']}})
                print ">> >> health monitor associated to pool : " + pool_name
                vip = neutron.create_vip({'vip':{'protocol': port[2].upper(), 'name': pool_name+'_vip', 'description': pool_name+'_vip', 'admin_state_up': True, 'subnet_id': subnet[1], 'pool_id': pool['pool']['id'], 'session_persistence': {'type': 'SOURCE_IP'}, 'protocol_port': port[1]}})
                status = 'creating'
                while(status != 'ACTIVE'):
                    print ">> >> VIP status : " + status
                    time.sleep(1)
                    status = neutron.show_vip(vip['vip']['id'])['vip']['status']
                fip = neutron.create_floatingip({'floatingip': {'floating_network_id': archi['network'][external_pool],'fixed_ip_address': vip['vip']['address'], 'port_id':vip['vip']['port_id']}})
                archi['public_ip'] [pool_name] = fip['floatingip']['floating_ip_address']
                print ">> >> Floating IP associated to : " + pool_name
                for ip in instance_ips:
                    status = 'creating'
                    while(status != 'ACTIVE'):
                        print ">> >> " + pool_name + " status : " + status
                        time.sleep(1)
                        status = neutron.show_pool(pool['pool']['id'])['pool']['status']
                    neutron.create_member({'member': {'protocol_port': port[1], 'weight': 1, 'admin_state_up': True,'pool_id': pool['pool']['id'], 'address': ip}})
                    print ">> >> member with ip : " + ip + " added to pool : " + pool_name
    print "done creating elbs :) "
    return archi
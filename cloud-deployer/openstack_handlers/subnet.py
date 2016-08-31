#!/usr/bin/env python

#import modules
import csv
from netaddr import IPNetwork
from neutronclient.v2_0 import client as neutronclient

#Create a new Subnet
def subnet_create(credentials, my_csv, dns_servers, external_pool, archi, tags=None):
    #open csv file and read each row as dictionary
    subnet_file =  open(my_csv, 'rb')
    subnet_reader = csv.DictReader(subnet_file)
    
    print "##########################    Starting routers, networks and subnets creation         ###############################" 
    if 'router' not in archi:
        archi['router'] = {}
    if 'subnet' not in archi:
        archi['subnet'] = {}
    if 'network' not in archi:
        archi['network'] = {}
        
    #iterate through rows checking for subnets
    for subnet_dict in subnet_reader:
        ip_data = IPNetwork(subnet_dict['cidr'])
        neutron = neutronclient.Client(username=credentials['username'],password=credentials['password'],tenant_name=archi['vpc'][subnet_dict['vpc']],auth_url=credentials['auth_url'])
        
        #create Openstack network
        network = neutron.create_network({'network':{'name': subnet_dict['subnet'], 'admin_state_up': True}})
        my_dns = []
        my_update_subnet = {'subnet':{'host_routes':[]}}
        my_dns.append(dns_servers[subnet_dict['vpc']])
        for server in dns_servers:
            if server != subnet_dict['vpc']:
                my_dns.append(dns_servers[server])
                
        #create Openstack subnet        
        subnet = neutron.create_subnet({'subnets': [{'name': subnet_dict['subnet'],'cidr': subnet_dict['cidr'], 'ip_version': 4, 'dns_nameservers':my_dns, 'network_id': network['network']['id']}]})
        print subnet_dict['subnet'] + " created"
        archi['network'][subnet_dict['subnet']]  = network['network']['id']
        archi['subnet'][subnet_dict['subnet']]  = subnet['subnets'][0]['id']
        
        if subnet_dict['vpc']+'-router' not in archi['router']:
            #create Openstack internal router             
            router = neutron.create_router({'router': {'name': subnet_dict['vpc']+'-router','admin_state_up': True}})
            archi['router'][subnet_dict['vpc']+'-router'] = router['router']['id']
            print subnet_dict['vpc']+'-router' + " created"
        ip_data = IPNetwork(subnet_dict['cidr'])
        internal_port = 1
        
        #create Openstack routes  
        if subnet_dict['route_table'] :
            if 'add' in archi['rt'][subnet_dict['vpc']+'_'+subnet_dict['route_table']]:
                internal_port = 3
                my_update_subnet['subnet']['host_routes'].append({'destination':archi['vpc'][subnet_dict['vpc']+'_cidr'],'nexthop':str(ip_data[internal_port])})
                for route_dict in archi['rt'][subnet_dict['vpc']+'_'+subnet_dict['route_table']]:    

                    if route_dict != 'add':
                        if route_dict['route_type']=='igw':
                            port = neutron.create_port({'port': {'name': subnet_dict['subnet'], 'admin_state_up': True, 'network_id': network['network']['id'],'fixed_ips': [{'subnet_id': subnet['subnets'][0]['id'], 'ip_address': str(ip_data[1])}]}})
                            route = neutron.add_interface_router(archi['igw'][route_dict['route']], {"port_id": port['port']['id'] })
                            print subnet_dict['subnet'] + " attached to "+route_dict['route']
                        if route_dict['route_type']=='instances':
                            my_update_subnet['subnet']['host_routes'].append({'destination':route_dict['cidr'],'nexthop':str(ip_data[internal_port])})
                            print subnet_dict['subnet'] + " attached to "+route_dict['route']
                            
        port = neutron.create_port({'port': {'name': subnet_dict['subnet'], 'admin_state_up': True, 'network_id': network['network']['id'],'fixed_ips': [{'subnet_id': subnet['subnets'][0]['id'], 'ip_address': str(ip_data[internal_port])}]}})
        interface = neutron.add_interface_router(archi['router'][subnet_dict['vpc']+'-router'], {"port_id": port['port']['id'] })
        print subnet_dict['subnet'] + " attached to internal network"                     
        subnet = neutron.update_subnet(subnet['subnets'][0]['id'],my_update_subnet)        

            
    print "done creating routers, networks and subnets :) "
    return archi
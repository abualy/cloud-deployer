# TODO: bugs on openstack firewall from openstack_handlers.acl import *
from openstack_handlers.ebs import *
from openstack_handlers.elb import *
from openstack_handlers.igw import *
from openstack_handlers.instance import *
# TODO: bugs on openstack peering from openstack_handlers.peering import *
from openstack_handlers.route_table import *
from openstack_handlers.security_group import *
from openstack_handlers.subnet import *
from openstack_handlers.vpc import *
import logging
import argparse
import config_loader as loader
import datetime
import os

handler = logging.FileHandler('/var/log/cloud-deployer.log')
handler.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addHandler(handler)

class Openstack():
    def __init__(self, username, password, global_architecture = {}, tenant_name=None, auth_url = None): 
        self.osconfig = {}
        self.credentials = {}
        loader.load_config_file('%s/config/config.json' % os.path.dirname(os.path.abspath(__file__)), self.osconfig)
        assert('openstack' in self.osconfig)
        assert('tenant_name' in self.osconfig['openstack'])
        assert('auth_url' in self.osconfig['openstack'])
        assert('userdata' in self.osconfig['openstack'])
        
        self.tenant_name = self.osconfig['openstack']['tenant_name']
        self.auth_url = self.osconfig['openstack']['auth_url']
        self.user_data = self.osconfig['openstack']['userdata']
        if tenant_name is not None:
            self.tenant_name  = tenant_name
        if auth_url is not None:
            self.auth_url  = auth_url
            
        self.global_architecture = global_architecture
        if username is not None:
            self.username  = username
        else:
            raise Exception("missing openstack parameter: username")
        if password is not None:
            self.password  = password
        else:
            raise Exception("missing openstack parameter: password")
        self.credentials['username'] = username
        self.credentials['password'] = password
        self.credentials['auth_url'] = auth_url
        self.credentials['tenant_name'] = tenant_name
        
    def create_acls(self, csv=None):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = acl_create(self.credentials, csv, self.global_architecture )
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the acls creation, check logs")    
            
    def create_acl_associations(self, csv=None):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = acl_assoc_create(self.credentials, csv, self.global_architecture )
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the acl associations creation, check logs")   

    def create_dhcps(self, csv=None):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = dhcp_create(self.credentials, csv, self.global_architecture )
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the dhcp options creation, check logs")  

    def create_elbs(self, csv=None, external_pool="external"):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = elb_create(self.credentials, csv, external_pool, self.global_architecture)
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the elbs creation, check logs")  

    def create_ebs(self, csv=None):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = ebs_create(self.credentials, csv, self.global_architecture )
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the ebs creation, check logs") 
            
    def create_igws(self, csv=None, external_pool="external"):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = igw_create(self.credentials, csv, external_pool, self.global_architecture )
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the igws creation, check logs")

    def create_instances(self, csv=None, ami_id=None, keys_path=None, puppet_env=None, external_pool="external"):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            if ami_id is None: 
                raise Exception("missing parameter: ami_id")
            self.user_data["puppet"]["environment"] = puppet_env
            self.global_architecture = instance_create(self.credentials, csv, ami_id, external_pool, self.user_data, keys_path, self.global_architecture)
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the instances creation, check logs")

    def create_peering(self, csv=None, external_pool="external"):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = peering_create(self.credentials, csv, external_pool, self.global_architecture )
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the peering creation, check logs")
 
    def create_route_tables(self, csv=None):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = rt_create(self.credentials, csv, self.global_architecture )
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the route tables creation, check logs")

    def create_routes(self, csv=None, routes=[]):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = route_create(self.credentials, csv, routes, self.global_architecture )
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the routes creation, check logs")            
            
    def create_security_groups(self, csv=None):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = sg_create(self.credentials, csv, self.global_architecture )
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the security groups creation, check logs")   

    def create_subnets(self, csv=None, dns_servers = [], external_pool="external"):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = subnet_create(self.credentials, csv, dns_servers, external_pool, self.global_architecture)
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the subnets creation, check logs")             
            
    def create_vpcs(self, csv=None, external_pool="external" ):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = vpc_create(self.credentials, csv, external_pool, self.global_architecture)
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the vpcs creation, check logs")            
            
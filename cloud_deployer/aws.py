from aws_handlers.acl import *
from aws_handlers.dhcp import *
from aws_handlers.ebs import *
from aws_handlers.elb import *
from aws_handlers.igw import *
from aws_handlers.instance import *
from aws_handlers.peering import *
from aws_handlers.route_table import *
from aws_handlers.security_group import *
from aws_handlers.subnet import *
from aws_handlers.vpc import *
from boto import vpc
from boto.ec2 import elb
import logging
import argparse
import config_loader as loader
import datetime
import os

handler = logging.FileHandler('/var/log/cloud-deployer.log')
handler.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addHandler(handler)

class AWS():
    def __init__(self, region=None, global_architecture = {}, global_tags = {}, aws_access_key_id=None, aws_secret_access_key=None ): 
        self.config = {}
        loader.load_config_file('%s/config/config.json' % os.path.dirname(os.path.abspath(__file__)), self.config)
        assert('aws' in self.config)
        assert('region' in self.config['aws'])
        assert('tags' in self.config['aws'])
        assert('userdata' in self.config['aws'])
        
        self.region = self.config['aws']['region']
        self.global_tags = self.config['aws']['tags']
        self.user_data = self.config['aws']['userdata']
        
        today = str(datetime.date.today())
        self.global_tags["creation Date"] = today
        
        if region is not None:
            self.region  = region
        self.global_architecture = global_architecture
        if global_tags:
            self.global_tags = global_tags
        if aws_access_key_id is not None:
            self.aws_access_key_id  = aws_access_key_id
        else:
            raise Exception("missing AWS parameter: aws_access_key_id")
        if aws_secret_access_key is not None:
            self.aws_secret_access_key  = aws_secret_access_key
        else:
            raise Exception("missing AWS parameter: aws_secret_access_key")
        
        self.c = vpc.connect_to_region(region_name = self.region, aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key)
        self.elb = elb.connect_to_region(region_name = self.region, aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key)
    def create_acls(self, csv=None):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = acl_create(self.c, csv, self.global_architecture, self.global_tags)
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
            self.global_architecture = acl_assoc_create(self.c, csv, self.global_architecture, self.global_tags)
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
            self.global_architecture = dhcp_create(self.c, csv, self.global_architecture, self.global_tags)
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the dhcp options creation, check logs")  

    def create_elbs(self, csv=None):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = dhcp_create(self.elb, csv, self.global_architecture, self.global_tags)
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
            self.global_architecture = ebs_create(self.c, csv, self.global_architecture, self.global_tags)
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the ebs creation, check logs") 
            
    def create_igws(self, csv=None):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = igw_create(self.c, csv, self.global_architecture, self.global_tags)
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the igws creation, check logs")

    def create_instances(self, csv=None, ami_id=None, keys_path=None, puppet_env=None):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            if ami_id is None: 
                raise Exception("missing parameter: ami_id")
            self.user_data["puppet"]["environment"] = puppet_env
            self.global_architecture = instance_create(self.c, csv, self.global_architecture, ami_id, self.user_data, keys_path, self.global_tags)
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the instances creation, check logs")

    def create_peering(self, csv=None):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = peering_create(self.c, csv, self.global_architecture, self.global_tags)
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
            self.global_architecture = rt_create(self.c, csv, self.global_architecture, self.global_tags)
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the route tables creation, check logs")

    def create_routes(self, csv=None):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = route_create(self.c, csv, self.global_architecture, self.global_tags)
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
            self.global_architecture = sg_create(self.c, csv, self.global_architecture, self.global_tags)
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the security groups creation, check logs")   

    def create_subnets(self, csv=None):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = subnet_create(self.c, csv, self.global_architecture, self.global_tags)
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the subnets creation, check logs")             
            
    def create_vpcs(self, csv=None):
        try: 
            if csv is None: 
                raise Exception("missing parameter: csv path")
            self.global_architecture = vpc_create(self.c, csv, self.global_architecture, self.global_tags)
            logger.info("the current architecture is "+str(self.global_architecture))                
            return self       
        except Exception, e:
            logger.error(e)
            logger.error("the current architecture is "+str(self.global_architecture))
            raise Exception("Error in the vpcs creation, check logs")            
            
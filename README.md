Name
=====
                          _______             __  ___           __                 
                         / ___/ /__  __ _____/ / / _ \___ ___  / /__  __ _____ ____
                        / /__/ / _ \/ // / _  / / // / -_) _ \/ / _ \/ // / -_) __/
                        \___/_/\___/\_,_/\_,_/ /____/\__/ .__/_/\___/\_, /\__/_/   
                                                       /_/          /___/         
                                                       
                                                       
                                                       
Description
========= 

Cloud Deployer is a python library used to spawn entire cloud architectures based on descriptional csv files.


Table of Contents
==============

* [Name](#name)
* [Description](#description)
* [Status](#status)
* [Synopsis](#synopsis)
* [Installation](#installation)
* [Functions](#functions)
  * [create_vpcs](#create_vpcs)
  * [create_igws](#create_igws)
  * [create_peering](#create_peering)
  * [create_route_tables](#create_route_tables)
  * [create_subnets](#create_subnets)
  * [create_security_groups](#create_security_groups)
  * [create_instances](#create_instances)
  * [create_ebs](#create_ebs)
  * [create_routes](#create_routes)
  * [create_elbs](#create_elbs)
  * [create_acls](#create_acls)
  * [create_acl_associations](#create_acl_associations)
* [Use Case](#use-case)
* [TODO](#todo)
* [Copyright and License](#copyright-and-license)


Synopsis
=======
for an AWS deployment:

```python
from  cloud_deployer.aws import AWS  
aws = AWS("us-east-1", aws_access_key_id="******", aws_secret_access_key="********", global_tags = {}, global_architecture = {})
aws = aws.create_vpcs("/home/me/input_files_samples/vpcs.csv")
```

for an openstack deployment:

```python
from cloud_deployer.openstack import Openstack   
os = Openstack(username="admin",password="****",tenant_name="admin",auth_url="http://192.168.228.240:5000/v2.0", global_architecture = {})
os = os.create_vpcs("/home/me/input_files_samples/vpcs.csv",external_pool = "external")
```
[Back to TOC](#table-of-contents)

Installation
=========
first of all to prepare the environment, install the packages:
```shell
apt-get install -y python-pip python-dev
```
then to avoid some openstack-clients errors in latest version:
```shell
pip install -U setuptools
```
after that just install:

```shell
python cloud-deployer/setup.py install
```

[Back to TOC](#table-of-contents)

Functions
=========

create_vpcs
------------------

 - **AWS:**
```python
aws = aws.create_vpcs("/home/me/input_files_samples/vpcs.csv")
```
creates aws vpcs from csv files.

 - **Openstack:**
```python
os = os.create_vpcs("/home/me/input_files_samples/vpcs.csv",external_pool = "external")
```

creates openstack projects, assigns them specified user with admin role, and updates their quotas, and add external pool the architecture description dictionary.
`external_pool:`  the public network pool defined in openstack.

 **parameters indicated in the csv file:**
`vpc:` vpc name.
`cidr:` CIDR range associated with the vpc.
`ENV,Group:` tags to be added to the created resources (AWS only).

[Back to TOC](#table-of-contents)

create_igws
-----------------

 - **AWS:**
```python
aws = aws.create_igws("/home/me/input_files_samples/igws.csv")
```
creates aws internet gateways from csv files.

 - **Openstack:**
```python
os = os.create_igws("/home/me/input_files_samples/igws.csv",external_pool = "external")
```

creates an openstack external router, assigns the external network for the external gateway info.
`external_pool:` the public network pool defined in openstack.

 **parameters indicated in the csv file:**
`vpc:` vpc group associated with it.

[Back to TOC](#table-of-contents)

create_peering
--------------------

 - **AWS:**
```python
aws = aws.create_peering("/home/me/input_files_samples/peerings.csv")
```
creates aws vpc peering connections  from csv files.

 - **Openstack:**
***Not Implemented YET ( due to openstack VPNaaS Issues )

 **parameters indicated in the csv file:**
`peering:` vpc group associated with it.
`vpc:` vpc group associated with it (peering source).
`vpc_peer:` vpc group  (peering destination, that needs manual approval).

[Back to TOC](#table-of-contents)

create_route_tables
---------------------------

 - **AWS:**
```python
aws = aws.create_route_tables("/home/me/input_files_samples/route-tables.csv")
```
creates aws empty route tables.

 - **Openstack:**
```python
os = os.create_route_tables("/home/me/input_files_samples/route-tables.csv")
```
adds csv file content to the architecture description dictionary, for laster use.

 **parameters indicated in the csv file:**
  (csv file used for create_routes function too)
`route_table:` route table name.
`vpc:` vpc group associated with it.
`route_type:` defines the route type, could be "peering" / "instances" .
`route:` route name , could be peering route (ex: "VPC_PEERING"), an instance (ex: "nat.vpc1").
`cidr:` network cidr to route to.

[Back to TOC](#table-of-contents)

create_subnets
---------------------

 - **AWS:**
```python
aws = aws.create_subnets("/home/me/input_files_samples/subnets.csv")
```
creates aws subnet and associate it to corresponding route table.

 - **Openstack:**
```python
os = os.create_subnets("/home/me/input_files_samples/subnets.csv", dns_servers = {'vpc1':'8.8.8.8','vpc2':'8.8.4.4'})
```
creates openstack network , creates subnet with DNS nameservers and associated to the created network, create internal router for communication inter subnets, and then creates routes.
`dns_servers :`dictionary dfines associated dns server to each vpc.

 **parameters indicated in the csv file:**
`subnet:` subnet name.
`acl:` netwrk acl to attach to.
`vpc:` vpc group associated with it.
`cidr:` subnet cidr .
`availability_zone:` availability zone to create in.
`instances:` instances associated with (optional description).
`route_table:` which route table to associate to.
`description:` (optional description field).

[Back to TOC](#table-of-contents)

create_security_groups
--------------------------------

 - **AWS:**
```python
aws = aws.create_security_groups("/home/me/input_files_samples/sgs.csv")
```
creates aws security groups and security group rules in each group.

 - **Openstack:**
```python
os = os.create_security_groups("/home/me/input_files_samples/sgs.csv")
```
creates openstack security groups and security group rules in each group.
***egress rules not yet implemented (openstack api/ client doesn't have this feature yet).

 **parameters indicated in the csv file:**
 `security_group:` security group name.
`acl:` netwrk acl to attach to.
`sg_description:` security group description.
`vpc:` vpc group associated with it.
`ingress/egress:` "ingress" or "egress" rule .
`src/dst:` source or destination machine/group of machines targeted (optional description).
`cidr:` CIDR  targeted to allow in this rule.
`from:` starting point of port range(included).
`to:` ending point of port range(included).
`tcp:` if tcp port, this field to be marked with an "*".
`udp:` if udp port, this field to be marked with an "*".
`icmp:` if icmp port, this field to be marked with an "*".
`description:` (optional description field).

[Back to TOC](#table-of-contents)

create_instances
-----------------------

 - **AWS:**
```python
aws = aws.create_instances(csv="/home/me/input_files_samples/instances.csv", ami_id="ami-12345678", keys_path="/home/me/keys")
```
creates aws key pair if non existing, creates instance with all corresponding parameters including user-data defined in config file, and roles in csv file, then allocate and associate an elastic ip address if instructed.
`ami_id :`the image id to use in creating the instance.
`keys_path :`a local folder path where to store generated ssh keys if non existing.

 - **Openstack:**
```python
os = os.create_instances(csv="/home/me/input_files_samples/instances.csv", ami_id="ami-12345678", keys_path="/home/me/keys",external_pool = "external")
```
creates openstack  key pair if non existing, creates instance with all corresponding parameters including user-data defined in config file, and roles in csv file, then allocate and associate a public ip address if instructed.
`ami_id :`the image id to use in creating the instance.
`keys_path :`a local folder path where to store generated ssh keys if non existing.
`external_pool :` the public network pool defined in openstack.
 
 **parameters indicated in the csv file:**
`instance:` instance name.
`security_groups:` security groups to assoicate with.
`subnet:` subnet to create in.
`vpc:` vpc group associated with it.
`access_key_name:` ssh access key (created only if non existing) .
`ip:` ip address to affect to the instance within the subnet range.
`public_ip:` mark with "YES" if want to associate it with a public ip.
`type:` instance type/flavor from existing catalogue.
`roles:` roles to pass within userdata (optional element).
`run:` mark "YES" if want to spawn this instance.

[Back to TOC](#table-of-contents)

create_dhcps
-------------------

 - **AWS:**
```python
aws = aws.create_dhcps(csv="/home/me/input_files_samples/dhcps.csv")
```
creates aws dhcp options set in the specified vpc.

 - **Openstack:**
***Not Implemented YET ( non existing service on openstack, already simulated with injected DNS values in subnets , and changing `/etc/neutron/dnsmasq-neutron.conf` to associate a cidr with default internal domain name ).
 
 **parameters indicated in the csv file:**
`dhcp:` dhcp options set name.
`vpc:` vpc group associated with it.
`domain_name:` default domain name to associate with the indicated vpc .
`domain_server:` DNS server fqdn to turn to when contacting dhcp (ex: "dns.vpc1").

[Back to TOC](#table-of-contents)

create_ebs
----------------

 - **AWS:**
```python
aws = aws.create_ebs(csv="/home/me/input_files_samples/ebs.csv")
```
creates aws ebs and attaches it to indicated instance.

 - **Openstack:**
```python
os = os.create_ebs(csv="/home/me/input_files_samples/ebs.csv")
```
creates openstack volume and attaches it to indicated instance.

 **parameters indicated in the csv file:**
`ebs:` ebs name.
`size:` size in Gbs.
`vpc:` vpc group associated with it.
`zone:` availability zone to create in.
`instance:` instance fqdn to associate with (ex:"machine1.vpc1")
`description:` (optional description field)
`run:` mark "YES" if want to spawn this instance.

[Back to TOC](#table-of-contents)

create_routes
-------------------

 - **AWS:**
```python
aws = aws.create_routes(csv="/home/me/input_files_samples/route-tables.csv")
```
creates aws "peering"/ "instances" route types.

 - **Openstack:**
```python
os = os.create_routes(csv="/home/me/input_files_samples/route-tables.csv")
```
creates openstack  "instances" route types (no peering for the moment in openstack) by adding static routes to internal router.
 
 **parameters indicated in the csv file:**
  (csv file used for create_routes function too)
`route_table:` route table name.
`vpc:` vpc group associated with it.
`route_type:` defines the route type, could be "peering" / "instances" .
`route:` route name , could be peering route (ex: "VPC_PEERING"), an instance (ex: "nat.vpc1").
`cidr:` network cidr to route to.

[Back to TOC](#table-of-contents)

create_elbs
----------------

 - **AWS:**
```python
aws = aws.create_elbs(csv="/home/me/input_files_samples/elbs.csv")
```
creates aws elb, registers instances in this elb, creates an elb policy, and set the policy for this elb.

 - **Openstack:**
```python
os = os.create_elbs(csv="/home/me/input_files_samples/elbs.csv")
```
creates openstack  pool, creates health monitors, and asscociates them to this pool, then creates vip, cerates and associates a floating ip with the vip, then attaches instances to ths pool by creating openstack members
 
 **parameters indicated in the csv file:**
  (csv file used for create_routes function too)
`elb:` elb name.
`vpc:` vpc group associated with it.
`subnets:` subnets where the elb creates its proxies.
`security_groups:` security groups to associate with the elb.
`listeners:` listeners definition port/protocol.
`servers:` instances fqdn to regsiter with the elb (ex: "nat.vpc1").
`policy_name:` elb policy name to create.
`policy_type:` elb policy type to create.
`attributes:` network cidr to route to.
`ports:` instances open ports to serve to.

[Back to TOC](#table-of-contents)

create_acls
----------------

 - **AWS:**
```python
aws = aws.create_acls(csv="/home/me/input_files_samples/acls.csv")
```
creates aws acls with their acl rules.

 - **Openstack:**
***Not Implemented YET ( due to openstack FWaaS Issues )

 **parameters indicated in the csv file:**
 `security_group:` security group name.
`acl:` netwrk acl to attach to.
`sg_description:` security group description.
`vpc:` vpc group associated with it.
`ingress/egress:` "ingress" or "egress" rule .
`src/dst:` source or destination machine/group of machines targeted (optional description).
`cidr:` CIDR  targeted to allow in this rule.
`from:` starting point of port range(included).
`to:` ending point of port range(included).
`tcp:` if tcp port, this field to be marked with an "*".
`udp:` if udp port, this field to be marked with an "*".
`icmp:` if icmp port, this field to be marked with an "*".
`description:` (optional description field).

[Back to TOC](#table-of-contents)

create_acl_associations
---------------------------------

 - **AWS:**
```python
aws = aws.create_acl_associations(csv="/home/me/input_files_samples/subnets.csv")
```
associates aws network acls with their corresponding subnets.

 - **Openstack:**
***Not Implemented YET ( due to openstack FWaaS Issues )

 **parameters indicated in the csv file:**
`subnet:` subnet name.
`acl:` netwrk acl to attach to.
`vpc:` vpc group associated with it.
`cidr:` subnet cidr .
`availability_zone:` availability zone to create in.
`instances:` instances associated with (optional description).
`route_table:` which route table to associate to.
`description:` (optional description field).

[Back to TOC](#table-of-contents)


Use Case
=======
this is a real use case to create a whole aws architecture from the ground up.

```python
from  cloud_deployer.aws import AWS  
aws = AWS("us-east-1", aws_access_key_id="******", aws_secret_access_key="********", global_tags = {}, global_architecture = {})
aws = aws.create_vpcs("/home/me/input_files_samples/vpcs.csv")
aws = aws.create_igws("/home/me/input_files_samples/igws.csv")
aws = aws.create_peering("/home/me/input_files_samples/peerings.csv")
aws = aws.create_route_tables("/home/me/input_files_samples/route-tables.csv")
aws = aws.create_subnets("/home/me/input_files_samples/subnets.csv")
aws = aws.create_security_groups("/home/me/input_files_samples/sgs.csv")
aws = aws.create_instances(csv="/home/me/input_files_samples/instances1.csv", ami_id="ami-12345678", keys_path="/home/me/keys")
aws = aws.create_dhcps("/home/me/input_files_samples/dhcps.csv")
aws = aws.create_instances(csv="/home/me/input_files_samples/instances2.csv", ami_id="ami-12345678", keys_path="/home/me/keys")
aws = aws.create_ebs("/home/me/input_files_samples/ebs.csv")
aws = aws.create_routes("/home/me/input_files_samples/route-tables.csv")
aws = aws.create_elbs("/home/me/input_files_samples/elbs.csv")
aws = aws.create_acls("/home/me/input_files_samples/acl.csv")
aws = aws.create_acl_associations("/home/me/input_files_samples/subnets.csv")
```

then you can dump architecture description dictionary, in order to have an archi-state.

```python
import json
my_dump=open('/home/me/architecture.txt','a')
my_dump.write('\n\n##################################\n\n')
my_dump.write(json.dumps(os.global_architecture, ensure_ascii=False))
my_dump.write('\n\n##################################\n\n')
my_dump.close()
```
[Back to TOC](#table-of-contents)


TODO
=====

[Back to TOC](#table-of-contents)


Copyright and License
==================
This packge is licensed under the MIT license.
For more info , refer to the license file in the main repository.

[Back to TOC](#table-of-contents)
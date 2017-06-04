#!/usr/bin/env python
"""
Collin M. 2017

Collect the running admin nodes from fuel-devops 2.9 and correlate them to the state in libvirt.
"""

from devops.models import Environment
from socket import gethostname
import xml.etree.ElementTree as ET
import json
import libvirt
from datetime import datetime

def libvirt_vm_state(name):
    """
    Expect a libvirt connection to be available at conn
    Return True of the VM is online
    Return False otherwise
    """
    try:
        res = conn.lookupByName(name).state()[0]
        if res == 1:
            state = True
        else:
            state = False
    except:
        state = False

    return state

def node_interfaces(node):
    return dict([(interface.network.name,interface.addresses[0].ip_address) for
     interface in node.interfaces])

def env_nodes(env, admin_only=False):
    nodes=[]
    for node in env.get_nodes():
        if node.name =='admin' or not admin_only:
            nd={'env':env.name,
                'node': node.name,
                'interfaces': node_interfaces(node),
                'state': libvirt_vm_state("{}_{}".format(env.name,node.name))}
            nodes.append(nd)
    return nodes

import sys
if len(sys.argv) > 1:
    output_file = sys.argv[1]
else:
    output_file = '/dev/stdout'

conn=libvirt.openReadOnly(None)
results=[]
for env in Environment.list_all():
    # nodes=env_nodes(env, admin_only=True)
    nodes=env_nodes(env, admin_only=False)
    if len(nodes) >0:
        results.append(nodes)


with open(output_file, 'w') as f:
    json.dump({'lab': gethostname(),
               'updated': datetime.utcnow().isoformat(),
               'environments': results}
              ,f)
    

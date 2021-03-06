from flask import Flask
from flask import render_template
import requests
import yaml
import os
import logging

app = Flask(__name__)

@app.context_processor
def utility_processor():

    def state_to_friendly(state):
        if state == True:
            return "Up"
        else:
            return "Down"
    return dict(state_to_friendly=state_to_friendly)

def read_conf(conf='conf.yaml'):
    full_p =  os.path.join(app.root_path, conf)
    if os.path.isfile(conf):
        conf=conf
    elif os.path.isfile(full_p):
        conf = full_p
    else:
        conf = '/var/www/lab-web/conf.yaml'
        logging.warning('Falling back to hard-coded config file {}'.format(conf))
                    
    with open(conf) as f:
        conf_items = yaml.load(f)
    return conf_items

@app.route('/')
def labs():
    all_envs = []
    unavailable = []
    sources = [x for x in read_conf()['platforms'] if x['platform_type'] == 'fuel-devops-http' and x['enabled'] == True]
    for platform in sources:
        try:
            req = requests.get(platform['url'])
            if req.status_code == 200:
                platform_req = req.json()['environments']
                [n.update({'platform': platform['name']}) for e in platform_req for n in e]        
                all_envs = all_envs + platform_req
        except:
            unavailable.append(platform['name'])

    # req_envs = [x for y in r.json()['environments']+r2.json()['environments'] for x in y if x['node'] == 'admin']
    req_envs = [x for y in all_envs for x in y if x['node'] == 'admin']
    envss = [{'name':x['env'], 'state':x['state'],'ip':x['interfaces']['admin'], 'url':"http://{}/".format(x['interfaces']['admin']), 'platform': x['platform']} for x in req_envs]
    envs = sorted(envss, key= lambda x: x['name'])
    return render_template('lab-web.html.j2', envs=envs, somevar='nope', unavailable=unavailable)
    

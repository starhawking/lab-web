from flask import Flask
from flask import render_template
import requests
app = Flask(__name__)

@app.context_processor
def utility_processor():

    def state_to_friendly(state):
        if state == True:
            return "Up"
        else:
            return "Down"
    return dict(state_to_friendly=state_to_friendly)

@app.route('/')
def labs():
    r = requests.get('http://172.19.17.6/env.json')
    r2 = requests.get('http://172.19.17.7/env.json')
    sources = {'suplab01':'http://172.19.17.6/env.json',
               'suplab02':'http://172.19.17.7/env.json',}
    {'nopelab01': 'localhost',
     'nopelab02': 'localhost'}

    all_envs = []
    unavailable = []
    for platform, url in sources.items():
        try:
            req = requests.get(url)
            if req.status_code == 200:
                platform_req = req.json()['environments']
                [n.update({'platform': platform}) for e in platform_req for n in e]        
                all_envs = all_envs + platform_req
        except:
            unavailable.append(platform)

    # req_envs = [x for y in r.json()['environments']+r2.json()['environments'] for x in y if x['node'] == 'admin']
    req_envs = [x for y in all_envs for x in y if x['node'] == 'admin']
    envss = [{'name':x['env'], 'state':x['state'],'ip':x['interfaces']['admin'], 'url':"http://{}/".format(x['interfaces']['admin']), 'platform': x['platform']} for x in req_envs]
    envs = sorted(envss, key= lambda x: x['name'])
    return render_template('lab-web.html.j2', envs=envs, somevar='nope', unavailable=unavailable)
    

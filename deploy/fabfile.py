from fabric.contrib.files import exists, append, sed 
from fabric.api import cd, run, local
import json
#import random

'''
Helper Functions
'''

def _read_json_data_fromfile(filename):
    with open(file=filename, mode='r') as json_data:
        read_data = json.load(json_data,) 
    return read_data

def _install_nginx_and_gunicorn():
    run('sudo apt install nginx')
    run('sudo systemctl start nginx')
    run('pip3 install gunicorn')

def _reload_nginx():
    run('sudo systemctl reload nginx')

def _reload_gunicorn(server_secrets):
    run("sudo systemctl daemon-reload")
    run(f'sudo systemctl restart gunicorn-{server_secrets["site_name"]}')

def _config_nginx(server_secrets):
    domain = server_secrets["domain"]
    env_user = server_secrets["env_user"]

    # nginx has some problems running on virtual machines, like ec2 instances or virtualbox
    # the issue is caused by faulty caching. The best way to resolve this
    # is to enter the nginx.conf file and change 'sendfile on;' to 'sendfile off;'
    run('sudo sed -i.bak -r -e "s/sendfile .+$/sendfile off;/g" "$(echo /etc/nginx/nginx.conf)"') # for some reason, Sed command wouldn't work

    # sed -i.bak -r -e 's/sendfile .+$;/sendfile off;/g' "$(echo /etc/nginx/nginx.conf)"

    if exists('/etc/nginx/sites-enabled/default'):
        run('sudo rm /etc/nginx/sites-enabled/default')
   
    if exists(f'/etc/nginx/sites-available/{domain}'):      # delete the site config file if needed
        run(f'sudo rm /etc/nginx/sites-available/{domain}')

    run(f'sudo touch /etc/nginx/sites-available/{domain}')

    nginx_listener = f"""
server {{
    listen 80;
    server_name {domain};  

    location /static {{
        alias /home/{env_user}/sites/static;        
    }}

    location / {{
        proxy_pass http://localhost:8000;   
    }}
}}
    """
    append(f'/etc/nginx/sites-available/{domain}', nginx_listener, use_sudo=True)

    # nginx has a sites-available folder and a sites_enabled folder. We'll create a symbolic link so that sites-enabled references sites-avaiable
    if exists(f'/etc/nginx/sites-enabled/{domain}'):        # delete any old symbolic link if needed
        run(f'sudo rm /etc/nginx/sites-enabled/{domain}')
    run(f'sudo ln /etc/nginx/sites-available/{domain} /etc/nginx/sites-enabled/{domain}')

def _get_latest_source_from_git(server_secrets, site_folder):
    '''
    Used for both initial deployment and ongoing deployment, this will pull down the source from the remote repo and run git reset --hard
    '''
    if exists('.git'):  # check if it's a git repo already. 
        run('git fetch')  
    else:
        run(f'git clone {server_secrets["github_repo_location"]} .')  

    # troubleshooting note, if this fails - have you pushed your latest commit? This next line runs a local command to find the latest commit
    current_commit = local("git log -n 1 --format=%H", capture=True)  
    run(f'git reset --hard {current_commit}')      
    
def _install_project_dependancies():
    run('sudo -H pip3 install -r requirements.txt')
    
def _alter_django_settings_py(server_secrets):
    site_name = server_secrets['domain']    
    remote_home_folder = server_secrets['remote_home_folder']
    settings_file = remote_home_folder + "/" + server_secrets['default_app_name'] + '/settings.py'

    # for this application, we'll skip the step for rerolling. Our public key was never accessible to the public. Also, this code was modified without testing, be sure to debug this code.
    #chars  = 'abcdefghijklmnopqrstuvwxyz0123456789'           # used as array of usable characters
    #key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))   # generate a 50 char string of random letters from the list of usable characters
    #print(f'key:  {key}')
    #run(f'sed -i.bak -r -e "s/SECRET_KEY = \'.+\'/SECRET_KEY = \'{key}\'/g" "$(echo {remote_home_folder}{default_app_directory}/settings.py)"')  # normally, we'd use the sed command, however this gets really confused with single quotes. To get around this, we've just run sed ourselves and run everything in double quotes

    # alter debug= and allowed_hosts=
    sed(settings_file, "DEBUG = True", "DEBUG = False")
    sed(settings_file, 
        'ALLOWED_HOSTS = .+$', 
        f'ALLOWED_HOSTS = ["127.0.0.1", "localhost", "{site_name}"]'
    )

    # remove the line that allows users to browser the API. Just comment it out. Again, SED has issues with single quotes unless run from CLI
    #sed(settings_file, "'rest_framework.renderers.BrowsableAPIRenderer',", "#'rest_framework.renderers.BrowsableAPIRenderer',")
    #run(f'sed -i.bak -r -e "s/\'rest_framework.renderers.BrowsableAPIRenderer\',/#\'rest_framework.renderers.BrowsableAPIRenderer\',/g" "$(echo /home/ubuntu/sites/dosgamesfinder/restapp/settings.py)"')  # normally, we'd use the sed command, however this gets really confused with single quotes. To get around this, we've just run sed ourselves and run everything in double quotes

def _run_database_migration():
    run('python3 manage.py migrate')
    
def _run_unit_tests(server_secrets):
    app_name = server_secrets["app_name"]
    run(f'python3 manage.py test {app_name}')

def _collect_static(site_folder):
    run(f'mkdir -p {site_folder}/static')
    run('python3 manage.py collectstatic --noinput')

def _minify_js_and_css_static(site_folder):
    static_folder = site_folder + '/../static/'
    # maybe a bit risky, but minification occurs by overwriting the original js and css files
    # /home/ubuntu/sites/bookmarks/../static/css/
    run(f"yui-compressor -o '.css$:.css' {static_folder}css/*.css")
    #run(f"yui-compressor -o '.js$:.js' {static_folder}js/*.js") # throws an error

def _delete_unneeded_files():
    # eg delete the deploy folder on the server
    run(f'rm -rf deploy/')

def _config_server_to_load_gunicorn_on_startup(server_secrets):   # ensures the server will load gunicorn on boot and ensure it reloads on crash
    site_name = server_secrets['site_name']
    env_user = server_secrets['env_user']
    remote_home_folder = server_secrets['remote_home_folder']
    default_app_name = server_secrets['default_app_name']

    service_name = f'gunicorn-{site_name}'

    if exists(f'/etc/systemd/system/{service_name}.service'):
        run(f'sudo rm /etc/systemd/system/{service_name}.service')

    run(f'sudo touch /etc/systemd/system/{service_name}.service')
    systemd_config = f"""
[Unit]
Description=Gunicorn server for {site_name}

[Service]
Restart=on-failure  
User={env_user}  
WorkingDirectory={remote_home_folder}  
ExecStart=/home/ubuntu/.local/bin/gunicorn {default_app_name}.wsgi:application

[Install]
WantedBy=multi-user.target 
    """

    append(f"/etc/systemd/system/{service_name}.service", systemd_config, use_sudo=True)
    run('sudo systemctl daemon-reload')
    run(f'sudo systemctl enable {service_name}')  
    run(f'sudo systemctl start {service_name}')      # To manually run gunicorn $ gunicorn restapp.wsgi:application

def _backup_dbase(server_secrets):
    '''
    A copy of the database will be saved as an SQL file, stored on the remote server in the home directory
    '''
    dbase_location = server_secrets['remote_home_folder'] 
    backup_location = '/home/ubuntu/db_backup'
    run(f'mkdir -p {backup_location}')    
    run(f'cp {dbase_location}/db.sqlite3 {backup_location}/db_backup.sqlite3')

'''

Fabric Methods

'''

def initial_config():
    # pull in server_secrets JSON file to set environment variables 
    server_secrets = _read_json_data_fromfile('server_secrets.json')
    site_folder = server_secrets['remote_home_folder']  
    run(f'mkdir -p {site_folder}')  

    with cd(site_folder):
        run('sudo apt-get update')
        run('sudo apt-get upgrade')
        run('sudo apt install python3')        # todo - add in creating symbolic links so that commands can be run just by typing python, not needing to type python3
        run('sudo apt install python3-pip')    # todo - same as above but with pip
        run('sudo apt install git')
        run('sudo apt-get install yui-compressor') # install a minifier to run on deployment
        _install_nginx_and_gunicorn()
        _config_nginx(server_secrets) 
        _reload_nginx()
        _config_server_to_load_gunicorn_on_startup(server_secrets)

def deploy():
    server_secrets = _read_json_data_fromfile('server_secrets.json')
    site_folder = server_secrets['remote_home_folder'] 
    
    with cd(site_folder):
        _backup_dbase(server_secrets)
        _get_latest_source_from_git(server_secrets, site_folder)
        _alter_django_settings_py(server_secrets)
        _install_project_dependancies()     
        _run_database_migration()
        _collect_static(site_folder)
        _minify_js_and_css_static(site_folder)
        _delete_unneeded_files()
        _reload_nginx()
        _reload_gunicorn(server_secrets)


from fabric.api import run, settings, env, cd, lcd, prompt, local, prefix
from fabric.contrib.console import confirm
import getpass

# prompt for project dirs
proj_path = prompt("enter the full base path this project will live in:")
proj_dir = filter(None, [w.strip() for w in proj_path.split('/')]).pop()  # removes trailing slash

full_path = (proj_path + '/' + proj_dir).replace('//','/')

def start_flask_project():
    with lcd(proj_path):
        local('git clone git@github.com:basilleaf/base_flask_redis_app.git')
        local('rm -rf base_flask_redis_app/.git')
        local('mv base_flask_redis_app %s;' % proj_dir)

    with lcd(full_path):
        activate = 'source venv/bin/activate'
        local('virtualenv venv --distribute')
        with prefix(activate):
            local('pip install -r requirements.txt')
            local('git init; git add .; git commit -m"init"')

            # heroku
            local('heroku create; git push heroku master; ')
            local('heroku open')

            print("finished! now you may want to: \n cd %s" % full_path)

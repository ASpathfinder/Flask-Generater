import os
import jinja2
import subprocess

def template_loader(template_name):
    tmplt_loader = jinja2.FileSystemLoader('./templates')
    tmplt_env = jinja2.Environment(loader=tmplt_loader)
    template = tmplt_env.get_template(template_name)
    return template

class FlaskGenerater:
    def __init__(self, **kwargs):
        self.root = kwargs.get('root', None)
        self.blueprint_names = kwargs.get('blueprint_names', [])
        self.app_path = None
        self.blueprint_path = {}
        self.static_path = None
        self.template_path = None
        self.instance_path = None

    def tracing_makedirs(self, *args):
        path = os.path.join(*args)
        os.makedirs(path)
        return path

    def generate_dir_tree(self):
        self.app_path = self.tracing_makedirs(self.root, 'app')
        for blp_name in self.blueprint_names:
            self.blueprint_path[blp_name] = self.tracing_makedirs(self.app_path, blp_name)
        self.static_path = self.tracing_makedirs(self.app_path, 'static')
        self.tracing_makedirs(self.static_path, 'js')
        self.tracing_makedirs(self.static_path, 'css')
        self.template_path = self.tracing_makedirs(self.app_path, 'templates')
        for blp_name in self.blueprint_names:
            self.tracing_makedirs(self.template_path, blp_name)
        self.instance_path = self.tracing_makedirs(self.root, 'instance')

    def generate_files(self):
        project_manage_tmplt = template_loader('project_manage.txt')
        project_dotenv_tmplt = template_loader('project_dotenv.txt')
        project_venv_activate_tmplt = template_loader('project_venv_activate.bat')
        project_requirements_tmplt = template_loader('project_requirements.txt')
        app_init_tmplt = template_loader('app__init__.txt')
        app_config_tmplt = template_loader('app_config.txt')
        app_model_tmplt = template_loader('app_model.txt')
        app_base_template_tmplt = template_loader('template_base.html')
        blueprint_init_tmplt = template_loader('blueprint__init__.txt')
        blueprint_view_tmplt = template_loader('blueprint_view.txt')

        with open(os.path.join(self.root, 'manage.py'), 'w+') as f:
            f.write(project_manage_tmplt.render())

        with open(os.path.join(self.root, '.env'), 'w+') as f:
            f.write(project_dotenv_tmplt.render())

        with open(os.path.join(self.root, 'activate.bat'), 'w+') as f:
            f.write(project_venv_activate_tmplt.render(root_path=self.root))

        with open(os.path.join(self.root, 'requirements.txt'), 'w+') as f:
            f.write(project_requirements_tmplt.render())

        with open(os.path.join(self.app_path, '__init__.py'), 'w+') as f:
            f.write(app_init_tmplt.render(blueprint_names=self.blueprint_names))

        with open(os.path.join(self.app_path, 'config.py'), 'w+') as f:
            f.write(app_config_tmplt.render())

        with open(os.path.join(self.app_path, 'model.py'), 'w+') as f:
            f.write(app_model_tmplt.render())

        with open(os.path.join(self.template_path, 'base.html'), 'w+') as f:
            f.write(app_base_template_tmplt.render())

        for name in self.blueprint_path:
            with open(os.path.join(self.blueprint_path[name], '__init__.py'), 'w+') as f:
                f.write(blueprint_init_tmplt.render(name=name))
            with open(os.path.join(self.blueprint_path[name], 'view.py'), 'w+') as f:
                f.write(blueprint_view_tmplt.render(name=name))
        print('Project Files Generated')

    def create_venv(self):
        print('Create venv')
        os.chdir(self.root)
        subprocess.run(['python', '-m', 'venv', 'venv'], capture_output=False)
        print('Venv created')

    def install_requirements(self):
        print('Install requirements')
        os.chdir(self.root)
        subprocess.run(['activate.bat'], capture_output=False)
        print('Requirements installed')

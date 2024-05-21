import os
import subprocess
import venv

class ExtendedEnvBuilder(venv.EnvBuilder):
    """
    This builder installs Django and Django REST Framework
    into the created virtual environment.
    """

    def __init__(self, *args, **kwargs):
        self.nodist = kwargs.pop('nodist', False)
        self.nopip = kwargs.pop('nopip', False)
        self.progress = kwargs.pop('progress', None)
        self.verbose = kwargs.pop('verbose', False)
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        self.context = context  # Saving context to be used in other methods
        os.environ['VIRTUAL_ENV'] = self.context.env_dir
        bin_dir = 'Scripts' if os.name == 'nt' else 'bin'
        self.pip_path = os.path.join(self.context.env_dir, bin_dir, 'pip')
        if not self.nodist and not self.nopip:
            self.install_django()
            self.install_djangorestframework()

    def install_django(self):
        subprocess.call([self.pip_path, 'install', 'Django'])

    def install_djangorestframework(self):
        subprocess.call([self.pip_path, 'install', 'djangorestframework'])

def create_project_and_app(project_name, app_name):
    # Create the project directory
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)

    # Create the virtual environment inside the project directory
    builder = ExtendedEnvBuilder(with_pip=True)
    builder.create('env')

    # Activate the virtual environment
    bin_dir = 'Scripts' if os.name == 'nt' else 'bin'
    activate_script = os.path.join('env', bin_dir, 'activate')
    activate_command = f"source {activate_script}" if os.name != 'nt' else activate_script
    subprocess.run(activate_command, shell=True)

    # Install Django and Django REST framework
    subprocess.run(f"pip install django djangorestframework", shell=True)

    # Create Django project
    subprocess.run(f"django-admin startproject {project_name} .", shell=True)

    # Navigate into the project directory
    os.chdir(project_name)

    # Create the Django app
    subprocess.run(f"django-admin startapp {app_name}", shell=True)

def main():
    # Obtain project and app names
    project_name = input("Enter the name of the Django project: ")
    app_name = input("Enter the name of the Django app: ")

    # Create the project and app
    create_project_and_app(project_name, app_name)

if __name__ == "__main__":
    main()

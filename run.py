from main import FlaskGenerater
import sys
import os

if __name__ == '__main__':
    project_root = sys.argv[1]
    if not os.path.exists(project_root):
        os.makedirs(project_root)
    gen = FlaskGenerater(root=project_root, blueprint_names=sys.argv[2:])
    gen.generate_dir_tree()
    gen.generate_files()
    gen.create_venv()
    gen.install_requirements()
'''
Script that replicates and environment for a python data science project
author: Andreu Mora (andreu.mora@gmail.com), Tobias Guggenmoser (t.guggenmoser@gmail.com)
'''

import os
import getpass
import json
import sys
import shutil
import argparse

DEBUG = True
WGPATH = os.path.dirname(os.path.realpath(__file__))

class ConfigVar(object):
    """
    Handle a single configuration variable.
    """


    def __init__(self, name, f_default=None, description="", prompt=""):
        self.name = name
        self.description = description
        self.prompt = prompt
        if f_default is None:
            f_default = lambda setup: None
        self.default = f_default

    def __repr__(self):
        return "ConfigVar {0}".format(self.name)

    def __hash__(self):
        return hash(self.name)


class Config(object):
    """
    Handle collection of ConfigVar`s.
    """


    def __init__(self, interact=True):
        self.variables = []
        self.interact = interact

    def add_variable(self, var):
        assert all((var.name != v.name for v in self.variables))
        self.variables.append(var)

    def evaluate(self, dct):
        values = LoggableContainer({}, debug=DEBUG)
        for v in self.variables:
            val = None
            if v.name in dct:
                val = dct[v.name]
            else:
                val = v.default(values)
                if self.interact:
                    val = prompt_var(v, default=val)
            if val is None:
                raise RuntimeError("No value given for variable {0}".format(v.name))
            values[v] = val
        return values


def prompt_var(v, default=None):
    """
    Get user input for ConfigVar v.
    """

    p = v.prompt
    if not p:
        p = v.name

    s = "Enter {0}".format(p)
    if default is not None:
        s = " ".join([s, "[{0}]".format(default)])
    s = " ".join([s, ":"])

    val = input(s)
    if not val:
        val = default

    return val



class LoggableContainer(object):
    """
    Wrapper with optional debug output for .__getitem__().
    """

    def __init__(self, wrap, debug=False):
        self._wrapped = wrap
        self.debug = debug

    @property
    def wrapped(self):
        return self._wrapped

    def __getitem__(self, key):
        return self.wrapped[key]

    def __setitem__(self, key, value):
        if self.debug:
            print("DEBUG: {0} = {1}".format(key, value))
        self.wrapped[key] = value

    def __getattr__(self, name):
        return getattr(self.wrapped, name)


CONFIG = Config()
CONFIG.add_variable(ConfigVar("PROJECT_NAME", prompt="project's name"))
CONFIG.add_variable(ConfigVar("AUTHOR_NAME", prompt="author's name"))
CONFIG.add_variable(ConfigVar("AUTHOR_MAIL", prompt="author's email"))
CONFIG.add_variable(ConfigVar("DESCRIPTION", prompt="project description"))

fpyver = lambda vals: "{0}.{1}".format(*sys.version_info[:2])
CONFIG.add_variable(ConfigVar("PYTHON_VER", prompt="Python version",
                              f_default=fpyver))

home = os.path.expanduser("~")
defdir = lambda vals: os.path.join(home, "Documents", vals["PROJECT_NAME"])

CONFIG.add_variable(ConfigVar("PROJECT_DIR", prompt="project directory", f_default=defdir))
CONFIG.add_variable(ConfigVar("PYPATH", prompt="additional search paths (comma sep)"))


def create_project_tree(var_dict):

    root = var_dict["PROJECT_DIR"]
    if os.path.exists(root):
        raise ValueError("Directory {0} already exists. Aborting.".format(root))

    tree = {
        'figures': {},
        'notebook': {},
        'output': {},
        'config': {
            'scripts': {},
            },
        'data': {
            'in': {},
            'out': {},
            'tmp': {},
            },
        'src': {},
        }

    def mktree(tr, base=root):
        for subtr_name, subtr in tr.items():
            subtr_path = os.path.join(base, subtr_name)
            print("Creating directory {0}...".format(subtr_path))
            os.mkdir(subtr_path)
            mktree(subtr, base=subtr_path)

    mktree(tree)



def main(args):
    print("Welcome to Wet Gremlin, a utility to create project environments.")

    dct = {}
    if args.f:
        if not os.path.exists(args.f):
            raise ValueError("Invalid config file: {0}".format(args.f))
        with open(args.f) as fp:
            exec(fp.read(), dct)

    var_dict = CONFIG.evaluate(dct)

    create_project_tree(var_dict["PROJECT_DIR"])

    conda_cmd = " ".join(["conda create",
                          "--name", var_dict["PROJECT_NAME"],
                          "--python", var_dict["PYTHON_VER"]])
    ret_conda = os.system(conda_cmd)
    if ret_conda:
        raise RuntimeError("Conda environment could not be created, see log for errors")

    shutil.copy(os.path.join(WGPATH, "support", "template", "__init__.py"),
                os.path.join(var_dict["PROJECT_DIR"], "src"))

    PYTHONPATH_LIST = [os.path.join(var_dict["PROJECT_DIR"], "src")]
    PYTHONPATH_LIST.extend(var_dict["PYPATH"].split(','))

    print ("External codebases can be added later on to PYTHONPATH manager in project_vars.json")

    def install(src, dst):
        src = src.split("/")
        dst = dst.split("/")
        shutil.copy(os.path.join(WGPATH, "support", *src),
                    os.path.join(var_dict["PROJECT_DIR"], *dst))

    install("template/conda_setup.json", "config")
    install("template/.gitignore", ".")
    install("template/wiki.md", "wiki")

    scripts = ["setenv.py", "get_env_name.py", "get_env_dir.py", "get_env_pythonpath.py"]
    for script in scripts:
        install("scripts/{0}".format(script), "config/scripts")
    install("scripts/setenv.sh", ".")

    with open(os.path.join(PROJECT_DIR, "README.md"), 'w') as text_file:

        def writeln(s=""):
            text_file.write(s.format(**var_dict) + "\n")

        writeln("## Project {PROJECT_NAME}")
        writeln("{DESCRIPTION}")
        writeln()
        writeln()
        writeln("Author: {AUTHOR_NAME} <{AUTHOR_MAIL}>")
        writeln("## Dependencies")
        writeln("* Needs python 3 to execute the installation script")
        writeln("* Needs conda to manage virtual environments")
        writeln("* Virtual environment dependencies can be found in config/conda_setup.json")
        writeln("Project template created with Wet Gremlin (https://github.com/drublackberry/wet-gremlin)")

        # Store the environment variables in a json file
        with open(os.path.join(PROJECT_DIR,'config', 'project_vars.json'), 'w') as fp:
            json.dump(var_dict.wrapped, fp, indent=4, sort_keys=True)

            # Configure git
        try:
            os.chdir(var_dict["PROJECT_DIR"])
            print(os.getcwd())
            os.system("git init")
            os.system("git add .")
            os.system("git commit -m \"First commit from project creation \"")
            REMOTE_GIT_ADD = input("Add remote git repository? ([y]/n): ")
            if REMOTE_GIT_ADD.lower() == 'y' or REMOTE_GIT_ADD == '':
                REMOTE_GIT = input("Enter remote address: ")
                os.system("git remote add origin "+REMOTE_GIT)
                os.system("git push -u origin master")
        except:
            raise RuntimeError("Git not installed or not configured. Try manually.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", default="", type=str, help="configuration file")
    args = parser.parse_args()
    main(args)

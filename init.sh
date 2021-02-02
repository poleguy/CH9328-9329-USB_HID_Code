#!/bin/bash
# use:
#  source ./init.sh
#
# running this directly without source will not effect the active environment
# https://stackoverflow.com/questions/496702/can-a-shell-script-set-environment-variables-of-the-calling-shell

# .bashrc should be updated by running
# conda init bash
# conda config --set auto_activate_base false
# conda config --set env_prompt '({name})'

conda env create --prefix ./cenv -f environment.yml
# if ./cenv already exists, the line above will error out with "CondaValueError: prefix already exists". The update line below will make sure it's up-to-date.
conda env update --prefix ./cenv -f environment.yml

# this will create a clean ./cenv if it does not exist
# it will run a quick update if it does, for interactive use.

# for debug
conda env list

# activate
conda activate ./cenv

# other helpful commands:
# conda deactivate
# conda env remove --prefix ./env
# conda env remove --name test-env


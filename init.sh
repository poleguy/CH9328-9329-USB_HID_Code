#!/bin/bash
# use:
#  source ./init.sh
#
# running this directly without source will not effect the active environment
#
# https://stackoverflow.com/questions/496702/can-a-shell-script-set-environment-variables-of-the-calling-shell

# this will create a clean ./cenv if it does not exist
# it will run a quick update if it does, for interactive use.


# .bashrc should be updated by running
# conda init bash
# conda config --set auto_activate_base false
# conda config --set env_prompt '({name})'

# using || true to avoid erroring out if environment isn't happy

conda env create --prefix ./cenv -f environment.yml || true
# if ./cenv already exists, the line above will error out with "CondaValueError: prefix already exists". The update line below will make sure it's up-to-date.

# update won't work if it's not already activated?
conda env update --prefix ./cenv -f environment.yml || true
# 
# https://stackoverflow.com/questions/45510430/install-packages-into-existing-conda-environment-specified-in-environment-yml
#Unfortunately if you have an environment name in environment.yml the update/install will happen to that named environment.


# for debug
echo "conda environments:"
conda env list

# activate
conda activate ./cenv || true


# other helpful commands:
# conda deactivate
# conda env remove --prefix ./env
# conda env remove --name test-env
echo "init.sh done"

#!/bin/bash
# use:
#  source ./init.sh
#
# running this directly without source will not effect the active environment
#
# https://stackoverflow.com/questions/496702/can-a-shell-script-set-environment-variables-of-the-calling-shell

# this will create a clean ./cenv if it does not exist
# it will run a quick update if it does, for interactive use.

# https://serverfault.com/questions/146745/how-can-i-check-in-bash-if-a-shell-is-running-in-interactive-mode
if [[ $- == *i* ]]
then
    echo $-
    echo shell is interactive
else
    echo $-
    echo shell is not interactive
fi

# .bashrc should be updated by running
# conda init bash
# conda config --set auto_activate_base false
# conda config --set env_prompt '({name})'

# to get this to run in a noninteractive script (which doesn't source /etc/profile.d/conda.sh)
# https://stackoverflow.com/questions/52779016/conda-command-working-in-command-prompt-but-not-in-bash-script
# https://github.com/conda/conda/issues/7980
# https://stackoverflow.com/questions/55507519/python-activate-conda-env-through-shell-script
eval "$(command conda 'shell.bash' 'hook' 2> /dev/null)"
# note: jenkins sources this environment only when the agent is started!
# restart the agent if you need to pull in fresh environment settings

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
export root_dir=`pwd`
export PYTHONPATH=${root_dir}:${root_dir}/
echo "setup_python done"

#!/bin/bash

##########################################################
#  General Configuration
#  Adjust these parameters before you run the script
#
##########################################################
CONFIG_FILE=configs/config_10_Local_Testing.ini
INTERVALS_FILE=configs/intervals.csv

##########################################################
#
#   End of inputs
#
##########################################################

# Read Configs.ini
source <(grep = ${CONFIG_FILE} | sed 's/ *= */=/g')
echo 'Ignore above warnings :)'
echo '--------------------'
echo 'Testing if link to config works (should not be empty):'
echo $exportDirectoryPathString
echo 'If the line above is empty, you have errors and not warnings :D'
echo '--------------------'
# works
# Wrapper function to print the command being run
function run {
    # shellcheck disable=SC2145
    echo "$ $@"
    "$@"
    echo '####################'
}

# First the ones with 2 modes (second is)
if [[ $1 == 'ini' && $2 == 'intervals' ]]; then
    echo "Running Sensor-Data-Sync with other config file and other intervals."
    echo 'Config File:' $CONFIG_FILE
    echo 'Intervals File:' $INTERVALS_FILE
    echo '--------------------'
    run python __main__.py --inifile=${CONFIG_FILE} \
        --intervals=${INTERVALS_FILE}

elif [[ $1 == 'ini' && $2 == 'special' ]]; then
    echo "Not supported yet."
    echo '--------------------'

# Then the ones with only 1 mode (no second mode given)
elif [[ $1 == 'ini' ]]; then
    echo "No 2nd argument passed. Only '$1':"
    echo "Running Sensor-Data-Sync with other config file."
    echo 'Config File:' $CONFIG_FILE
    echo '--------------------'
    run python __main__.py --inifile=${CONFIG_FILE}

else
    echo "No arguments passed."
    echo '--------------------'
    run python __main__.py
fi

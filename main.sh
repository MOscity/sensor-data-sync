#!/bin/bash

##########################################################
#  General Configuration
#  Adjust these parameters before you run the script with any argument
#
##########################################################
CONFIG_FILE=configs/config_template_local_testing.ini
INTERVALS_FILE=configs/intervals.csv
EXPORT_DIR="/mnt/d/FHNW/2021_ComPAS/Path_With_No_Spaces/"

##########################################################

#   End of inputs
#
##########################################################

##########################################################
#
#   # Examples:
#
#   # Run the script with the config file as defined in __main__.py:
#   ./main.sh
#
#   # Run the script with the config file as here defined above:
#   ./main.sh ini
#
#   # Run the script with the config file and intervals file as defined here above:
#   ./main.sh ini csv_intervals
#
#   # Run the script using the config file, but other time intervals.
#   # Use with --inifile, (--csv_intervals) or (--interval and --units), --export_dir
#   # If no options specified, it executes the same code as ./main.shs
#   ./main.sh kwargs [options]
#
#   # Examples:
#   ./main.sh kwargs --interval=3
#   ./main.sh kwargs --interval 2 --units 'min'
#   ./main.sh kwargs --interval 1 --units 'min' --export_dir='C:/mypath'
#   ./main.sh kwargs --units 'hours' --export_dir 'C:/mypath'
#   ./main.sh kwargs --interval 3 --export_dir 'C:/mypath'
#   ./main.sh kwargs --export_dir='C:/mypath'
#   ./main.sh kwargs --csv_intervals='configs/intervals.csv' --export_dir='C:/mypath'
#
##########################################################

echo '##########+---------------+##########'
# works
# Wrapper function to print the command being run
function run {
    # shellcheck disable=SC2145
    echo "$ $@"s
    "$@"
    echo '##########+---------------+##########'
}

# First the ones with 2 modes (second is)
if [[ $1 == 'ini' && $2 == 'csv_intervals' ]]; then
    echo "Running Sensor-Data-Sync with other config file and other intervals."
    # Read Configs.ini
    source <(grep = ${CONFIG_FILE} | sed 's/ *= */=/g')
    echo 'Ignore above warnings :)'
    echo 'Test if link to config file works (this should not be empty):'
    echo '+++++++++++'
    echo 'Export File Name is:' $exportFileNameString
    echo '+++++++++++'
    echo 'If export file name is empty, you will have errors. Maybe check your path.'
    echo '>>'
    echo '  Selected Config File:' $CONFIG_FILE
    echo '  Selected Intervals CSV File:' $INTERVALS_FILE
    echo '--'
    run python __main__.py --inifile=${CONFIG_FILE} \
        --csv_intervals=${INTERVALS_FILE}

elif [[ $1 == 'ini' && $2 == 'special' ]]; then
    echo "Not supported yet. Create your own. :)"
    echo '--'

# Then the ones with only 1 mode (no second mode given)
elif [[ $1 == 'ini' ]]; then
    echo "Running Sensor-Data-Sync with other config file."
    # Read Configs.ini
    source <(grep = ${CONFIG_FILE} | sed 's/ *= */=/g')
    echo 'Ignore above warnings :)'
    echo 'Test if link to config file works (this should not be empty):'
    echo '+++++++++++'
    echo 'Export File Name is:' $exportFileNameString
    echo '+++++++++++'
    echo 'If export file name is empty, you will have errors. Maybe check your path.'
    echo '>>'
    echo '  Selected Config File:' $CONFIG_FILE
    echo '--'
    run python __main__.py --inifile=${CONFIG_FILE}

elif [[ $1 == 'kwargs' ]]; then
    echo "Running Sensor-Data-Sync, passing custom arguments."
    echo '--'
    run python __main__.py --custom_args ${@:2}

else
    echo "No arguments passed."
    echo '--'
    run python __main__.py
fi

#!/bin/bash

function print_green(){
    echo -e "\033[32m$1\033[39m"
}

INSTALL_SYSTEM_DEPENDENCIES=true
INSTALL_PIP=true
INSTALL_BOWER=true
INSTALL_NPM=true
TRANSLATE=true
while getopts “napb” OPTION
do
    case $OPTION in
        a)
             print_green "only install aptitude"
             INSTALL_SYSTEM_DEPENDENCIES=true
             INSTALL_PIP=false
             INSTALL_BOWER=false
             INSTALL_NPM=false
             TRANSLATE=false
             ;;
        p)
             print_green "only pip install"
             INSTALL_SYSTEM_DEPENDENCIES=false
             INSTALL_PIP=true
             INSTALL_BOWER=false
             INSTALL_NPM=false
             TRANSLATE=false
             ;;
        b)
             print_green "only bower install"
             INSTALL_SYSTEM_DEPENDENCIES=false
             INSTALL_PIP=false
             INSTALL_BOWER=true
             INSTALL_NPM=false
             TRANSLATE=false
             ;;
        n)
             print_green "only node install"
             INSTALL_SYSTEM_DEPENDENCIES=false
             INSTALL_PIP=false
             INSTALL_BOWER=false
             INSTALL_NPM=true
             TRANSLATE=false
             ;;
        ?)
             print_green "fail"
             exit
             ;;
     esac
done

if  $INSTALL_SYSTEM_DEPENDENCIES ; then
    if [ "$OS" == "Darwin" ] ; then
        brew install libmagic
    else
        print_green "Installing aptitude dependencies"

        # Install base packages
        sudo apt-get -y install python-pip python-virtualenv python-dev build-essential

        print_green "Installing image libraries"
        # Install image libs
        sudo apt-get -y install libjpeg-dev zlib1g-dev zlib1g-dev

        print_green "Installing translation libraries"
        sudo apt-get -y install gettext


        if [[ $(which wkhtmltopdf | grep 'not found' | wc -l) > 0 ]]
        then
        print_green "Installing wkhtmltopdf"
        sudo aptitude -y install fontconfig xfonts-75dpi xfonts-base libxrender1
        wget https://bitbucket.org/wkhtmltopdf/wkhtmltopdf/downloads/wkhtmltox-0.13.0-alpha-7b36694_linux-trusty-amd64.deb
        sudo dpkg -i wkhtmltox-0.13.0-alpha-7b36694_linux-trusty-amd64.deb
        rm  wkhtmltox-0.13.0-alpha-7b36694_linux-trusty-amd64.deb
        fi

        print_green "Are you going to use postgre for your database? [Y/n]"
        read INSTALL_POSTGRE

        if [[ "$INSTALL_POSTGRE" == "Y" ||  "$INSTALL_POSTGRE" == "y" ||  "$INSTALL_POSTGRE" == "" ]]
        then
            INSTALL_POSTGRE=true
            ./install/postgres.sh
        else
            print_green "Are you going to use mysql for your database? [N/y]"
            read INSTALL_MYSQL

            if [[ "$INSTALL_MYSQL" == "y" ]]
            then
                # Install mysql related packages
                sudo apt-get -y install libmysqlclient-dev python-mysqldb
            fi
        fi
    fi


    # set a new virtual environment
    virtualenv .env
fi
if  $INSTALL_PIP ; then
    
    # activate the environment
    source .env/bin/activate

    # install setuptools
    pip install --upgrade setuptools

    # upgrade pip
    pip install --upgrade pip

    # install pip requiredments in the virtual environment
    .env/bin/pip install --requirement requirements.txt

    if [[ "$INSTALL_MYSQL" == "y" ]] ; then 
        pip install mysql-python
    fi

    if [[ "$INSTALL_POSTGRE" ]]
    then
        pip install psycopg2
    fi

fi

# update pip database requirements
source .env/bin/activate
if [[ "$INSTALL_MYSQL" == "y" ]]
then
    pip install MySQL-python
elif [[ "$INSTALL_POSTGRE" == "y" ]]
then
    pip install psycopg2
fi


# create the local_settings file if it does not exist
if [ ! -f ./project/settings/local_settings.py ] ; then
    cp project/settings/local_settings.py.default project/settings/local_settings.py

    if [ INSTALL_POSTGRE ] ; then 
        EXP="s/database-name/${PWD##*/}/g"
        print_green $i|sed -i $EXP project/settings/local_settings.py
        
        print_green "remember to configure in project/local_setings.py your database"
    else
        EXP="s/postgresql_psycopg2/sqlite3/g"
        print_green $i|sed -i $EXP project/settings/local_settings.py

        EXP="s/database-name/\/tmp/${PWD##*/}.sql/g"
        print_green $i|sed -i $EXP project/settings/local_settings.py
    fi
fi

# Change the project/settings/__init__.py file it contains the CHANGE ME string
if grep -q "CHANGE ME" "project/settings/__init__.py"; then
    print_green "Generate secret key"
    # change the SECRET_KEY value on project settings
    python manage.py generatesecretkey
fi


if  $INSTALL_NPM ; then
    # package.json modification
    EXP="s/NAME/${PWD##*/}/g"
    print_green $i|sed -i $EXP package.json
    EXP="s/HOMEPAGE/https:\/\/bitbucket.org\/magnet-cl\/${PWD##*/}/g"
    print_green $i|sed -i $EXP package.json

    npm install
fi

if  $INSTALL_BOWER ; then
    # bower.json modification
    EXP="s/NAME/${PWD##*/}/g"
    print_green $i|sed -i $EXP bower.json
    EXP="s/HOMEPAGE/https:\/\/bitbucket.org\/magnet-cl\/${PWD##*/}/g"
    print_green $i|sed -i $EXP bower.json

    ./node_modules/bower/bin/bower install
fi
 
if $TRANSLATE ; then 
    ./translate.sh -c
fi

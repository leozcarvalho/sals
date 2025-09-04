#!/bin/bash

if [ -z "$1" ]; then
    echo "command params:";
    echo "1st param:"
    echo "server-docker - run server on docker";
    echo "refresh - pull master/develop"
else
    CMD_RUN=$1

    if [ "$CMD_RUN" = "server-docker" ]; then
        echo "Install dependencies"
        npm install
        echo "Start server"
        npm run dev

    elif [ "$CMD_RUN" = "refresh" ]; then
        git checkout develop
        git pull
        git checkout master
        git pull
        git checkout develop
        git merge master
        git pull

    elif [ "$CMD_RUN" = "static" ]; then
        npm install
        npm run build

    else
        echo "nothing to do";

    fi
fi

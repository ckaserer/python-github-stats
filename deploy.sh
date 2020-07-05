#!/bin/bash

set -euo pipefail

# Make sure these values are correct for your environment
resourceGroup="github-api"
appName="gepardec-github-api"
location="eastus2" 

# Change this if you are using your own github repository
gitSource="https://github.com/ckaserer/python-github-stats.git"

az group create \
    -n $resourceGroup \
    -l $location

az appservice plan create \
    -g $resourceGroup \
    -n "linux-plan" \
    --sku B1 \
    --is-linux

az webapp create \
    -g $resourceGroup \
    -n $appName \
    --plan 'linux-plan' \
    --runtime 'PYTHON|3.8' \
    --deployment-source-url $gitSource \
    --deployment-source-branch master

az webapp config appsettings set \
    -g $resourceGroup \
    -n $appName \
    --settings GITHUB_ORG="$GITHUB_ORG" \
      GITHUB_TOKEN="$GITHUB_TOKEN" \
      SUBSCRIPTION_ID="$SUBSCRIPTION_ID" \
      DB_SERVER="$DB_SERVER" \
      DB_NAME="$DB_NAME" \
      WWIF="$WWIF"
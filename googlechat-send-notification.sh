#!/bin/bash

if [ ${TRAVIS_TEST_RESULT} -eq 0 ]; then
  IMAGE_URL=https://github.com/ckaserer/docker-travis-cli/raw/master/.images/build-success.png
else
  IMAGE_URL=https://github.com/ckaserer/docker-travis-cli/raw/master/.images/build-fail.png
fi

curl -d "
{
  'cards': [
    {
      'header': {
        'title': '${TRAVIS_REPO_SLUG}',
        'subtitle': 'Build Nr: ${TRAVIS_BUILD_NUMBER}',
        'imageUrl': '${IMAGE_URL}'
      },
      'sections': [
        {
          'widgets': [
              {
                'keyValue': {
                  'topLabel': 'Build',
                  'content': '${TRAVIS_BUILD_NUMBER}'
                }
              },{
                'keyValue': {
                  'topLabel': 'Hash',
                  'content': '$(git rev-parse --short ${TRAVIS_COMMIT})'
                }
              },
              {
                'keyValue': {
                  'topLabel': 'Message.',
                  'content': '${TRAVIS_COMMIT_MESSAGE}'
                  }
              },
              {
                'keyValue': {
                  'topLabel': 'Author',
                  'content': '$(git show -s --format='%an')'
                }
              }
          ]
        },
        {
          'widgets': [
              {
                  'buttons': [
                    {
                      'textButton': {
                        'text': 'OPEN LOGS',
                        'onClick': {
                          'openLink': {
                            'url': '${TRAVIS_BUILD_WEB_URL}'
                          }
                        }
                      }
                    }
                  ]
              }
          ]
        },
        {
          'widgets': [
              {
                  'buttons': [
                    {
                      'textButton': {
                        'text': 'SHOW DIFF',
                        'onClick': {
                          'openLink': {
                            'url': 'https://github.com/${TRAVIS_REPO_SLUG}/commit/${TRAVIS_COMMIT}'
                          }
                        }
                      }
                    }
                  ]
              }
          ]
        }
      ]
    }
  ]
}" -H "Content-Type:application/json" -X POST "${GOOGLECHAT_WEBHOOK}"

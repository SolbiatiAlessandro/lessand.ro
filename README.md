# lessand.ro
<p>This is the public repo for my personal website, currently deployed at http://lessand.ro/</p>

[![Build Status](https://travis-ci.com/SolbiatiAlessandro/lessand.ro.svg?branch=master)](https://travis-ci.com/SolbiatiAlessandro/lessand.ro)
[![codecov](https://codecov.io/gh/SolbiatiAlessandro/lessand.ro/branch/master/graph/badge.svg)](https://codecov.io/gh/SolbiatiAlessandro/lessand.ro)

my website is actually a full-stack web-app deployed on Heroku built with Flask and Postgresql, I will try to follow best practices in TDD, unit-testing and CICD and eventually even using SLOs and SLIs

To run locally tests and coverage run
```
pytest tests --cov=./ --cov-report html
open htmlcov/index.html
```

You should also export a local variable with the location of the local PostrgreSQL database with the following syntax
```
export DATABASE_URL="dbname='localdb'"
```

First Iteration
===============

- [X] design of the website
- [X] UI/UX prototype
- [X] system design
- [X] deployment on my local machine of the backbone
- [X] deployment on heroku of the backbone
- [X] set up CICD routines
- [X] integrate UI/UX on the backbone
- [X] clean up the github repo
- [X] finish first iteration deploying website and start write content


Second Iteration
================

- [X] manke jinja render html so I can write html here 
- [X] fix [Issue #1](https://github.com/SolbiatiAlessandro/lessand.ro/issues/1)
- [X] fix styling on the left and also fonts/dimensions/buttons 
- [X] write an about page 
- [X] add social links and add twitter 
- [X] add email
- [ ] make https work 
- [ ] make base domain without www
- [X] fix on SAFARI there is no sticky and rendered badly 
- [X] fix mobile version
- [x] figure out how to manage images for blog posts (ugly)
- [ ] **build/integrate Google analytics**
- [x] set up template from https://github.com/gfidente/pelican-svbhack
- [ ] add meta-descriptions and title to articles



These apps are configured to run on fly.io. Most assumptions about configuration have been put in `.env`, but deploying as a docker image is not tested.

## Overview

The webhook server is currently a demo function for automating volunteer group administration in EZ Texting. The demo will:
- accept forwarded SMS that are replies to a signup request
- parse out the days of the week that respondents want to sign up for
- add them to contact groups bucketed by weekday, and
- send a confirmation SMS back. 

The oauth server continuously presents a fresh token over an http interface at the `/generate_token` route. This design decision enables a deployment mode such that, for access control, the oauth server is deployed separately from the webhook server, so that webhook development can proceed without access to the account username/password. The webhook developer should not have access to the `.env` used to deploy the oauth server, there is a guardrail in .gitignore to avoid commiting these secrets 

# webhook_server
## Deployment instructions
cd into `./webhook_server`. Run `setup.py`. This will load any available environment variables in .env, then confirm if they are accurate. Any required variables not provided, or any innacurate variables, will be written.

run `fly launch`. Do accept the existing `fly.toml` if prompted. DO NOT overwrite Dockerfile if prompted. 
```
why? fly.io currently attempts to interpret this Flask project as Django, and inserts 'RUN manage.py' into the Dockerfile -- we adapt by removing that directive 
```
Once built, run `fly deploy` and you're good to go 

# oauth_server
## Deployment instructions 
cd into `./oauth_server`. Run `fly launch`. Do accept the existing `fly.toml` if prompted. DO NOT overwrite Dockerfile if prompted. Once built, run `fly deploy` and you're good to go 

# Other configuration
EZ Texting authenticates forwarded SMS by signing the requests with an `X-Signature` header, which is an hmacSHA1 hash of the message body. This hash is signed by a shared secret, which needs to be added to the user interface in EZ Texting when creating the webhook. It should also be added to `.env`
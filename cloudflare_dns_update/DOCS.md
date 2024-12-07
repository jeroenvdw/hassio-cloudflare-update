# Home Assistant Add-on: Cloudflare DNS Update

This add-on will update a DNS record within Cloudflare, with your personal IP address.


## Installation

1. Install the add-on
1. Open the config tab and be sure the set the following:
    - `api_token`: Follow these steps to create an API Token:
        - Head to https://dash.cloudflare.com/profile/api-tokens
        - Click the button "Create Token"
        - Go with the "Edit Zone DNS" template
    - `zone_id`: The Zone ID can be found on the Overview page of your website within your Cloudflare Dashboard
    - `domain`: The subdomain you'll be using. Be sure to define the subdomain first:
        - Go to the DNS page in your dashboard
        - Add an "A" record for a new subdomain
    - `sleep_time`: The number of seconds between two update intervals
1. Start the add-on


## Current status

This is my first add-on for Home Assistant.
I did not spend too much time on it, but it does work.

Improve logging and documentation is still on the to do list. 

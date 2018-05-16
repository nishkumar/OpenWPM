from __future__ import absolute_import
from automation import TaskManager, CommandSequence
from six.moves import range
import requests
from fake_useragent import UserAgent

ua = UserAgent()
urls_to_browse = ["https://www.google.com/search?q=women%27s+winter+boots",
    "https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=womens+winter+boots",
    "https://www.zappos.com/womens-winter-boots",
    "https://www.amazon.com/Timberland-Womens-Kenniston-Winter-Medium/dp/B01MT7WTDX/",
    "https://www.ebay.com/itm/Timberland-Womens-14-Inch-Premium-Side-Zip-Lace-Waterproof-Black-Boots-8632A/162719687948"]

# Visit URLs before checking sites for ads
headers = {'User-Agent': ua.firefox}
for url in urls_to_browse:
    try:
        response = requests.get(url, headers = headers)
        print "Site Visitied:", response.url
    except:
        print "Could not visit site"

The list of sites that we wish to crawl
NUM_BROWSERS = 1
sites = [   "http://www.dictionary.com/",
            "https://www.yahoo.com/",
            "http://www.rediff.com/",
            "https://www.reddit.com/",
            "https://www.recode.net/"]

# sites = urls_to_browse + sites

# Loads the manager preference and 3 copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in range(NUM_BROWSERS):
    # Record HTTP Requests and Responses
    browser_params[i]['http_instrument'] = True
    # Enable flash for all three browsers
    browser_params[i]['disable_flash'] = False
    #Save all content from Responses
    browser_params[i]['save_all_content'] = True
    #Activating DO NOT TRACK
    browser_params[i]['donottrack'] = True

browser_params[0]['headless'] = True  # Launch only browser 0 headless

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/Desktop/OpenWPM/'
manager_params['log_directory'] = '~/Desktop/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites with all browsers simultaneously
for site in sites:
    command_sequence = CommandSequence.CommandSequence(site)

    # Start by visiting the page
    command_sequence.get(sleep=0, timeout=60)
    command_sequence.dump_page_source()
    # dump_profile_cookies/dump_flash_cookies closes the current tab.
    command_sequence.dump_profile_cookies(120)



    # index='**' synchronizes visits between the three browsers
    manager.execute_command_sequence(command_sequence, index='**')

# Shuts down the browsers and waits for the data to finish logging
manager.close()

from __future__ import absolute_import
from automation import TaskManager, CommandSequence
from six.moves import range
import requests
from fake_useragent import UserAgent

ua = UserAgent()
urls_to_browse = ['https://www.allbirds.com/products/mens-wool-runners?variant=22238492551&utm_source=google&utm_medium=cpc&utm_campaign=Shopping+%2F%2F+US+%2F%2F+Non-Brand+Desktop+%28%29&utm_content=222861857964_46805152276&utm_term=_pla-375613546025&gclid=EAIaIQobChMI9vTh2KGI2wIV01mGCh0X-QkYEAQYASABEgITlfD_BwE',
                    'https://www.adidas.com/us/nmd_r2-shoes/BY3014.html?cm_mmc=AdieSEM_Feeds-_-GoogleProductAds-_-NA-_-BY3014&cm_mmca1=US&cm_mmca2=NA&kpid=BY3014&gclid=EAIaIQobChMI9vTh2KGI2wIV01mGCh0X-QkYEAQYAyABEgIWwPD_BwE&gclsrc=aw.ds&dclid=CNenhN-hiNsCFcm8swodBUYPEQ',
                    'https://www.adidas.com/us/nmd_r2-shoes/BY3014.html?cm_mmc=AdieSEM_Feeds-_-GoogleProductAds-_-NA-_-BY3014&cm_mmca1=US&cm_mmca2=NA&kpid=BY3014&gclid=EAIaIQobChMI9vTh2KGI2wIV01mGCh0X-QkYEAQYAyABEgIWwPD_BwE&gclsrc=aw.ds&dclid=CNenhN-hiNsCFcm8swodBUYPEQ',
                    'https://www.allbirds.com/products/mens-wool-runners?variant=22238492551&utm_source=google&utm_medium=cpc&utm_campaign=Shopping+%2F%2F+US+%2F%2F+Non-Brand+Desktop+%28%29&utm_content=222861857964_46805152276&utm_term=_pla-375613546025&gclid=EAIaIQobChMI9vTh2KGI2wIV01mGCh0X-QkYEAQYASABEgITlfD_BwE']

headers = {'User-Agent': ua.firefox}
for url in urls_to_browse:
    try:
        response = requests.get(url, headers = headers)
        print "Site Visitied:", response.url
    except:
        print "Could not visit site"

# The list of sites that we wish to crawl
NUM_BROWSERS = 1
sites = ['https://www.yahoo.com']

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
browser_params[0]['headless'] = True  # Launch only browser 0 headless

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/Desktop/OpenWPM'
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

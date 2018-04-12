from facebookads.api import FacebookAdsApi
from facebookads import adobjects

## Importing samples
from ads_reporting import AdsReportingSample
from carousel_ad import CarouselAdSample

## Importing Ad objects
from facebookads.adobjects.campaign import Campaign
from facebookads.adobjects.adset import AdSet
from facebookads.adobjects.targeting import Targeting

my_app_id = '<APP_ID>'
my_app_secret = '<APP_SECRET>'
my_access_token = '<ACCESS_TOKEN>'
proxies = {'http': '<HTTP_PROXY>', 'https': '<HTTPS_PROXY>'} # add proxies if needed
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

ad_account_id = 'act_<AD_ACCOUNT_ID>'
page_id = '<PAGE_ID>'


'''
# Reporting Sample

report_sample = AdsReportingSample()
values = report_sample.get_ads_insight(ad_account_id, '2018-04-11')
print(values)
'''

'''

# Create Carousel Ad Sample

carousel_sample = CarouselAdSample()
products = [
	{
		'image_path': '<LOCAL_PATH_TO_SOME_IMAGE_FILE>',
		'link': 'https://www.example.com/product_1',
		'name': 'Product 1',
		'description': 'This is Product 1'
	},
	{
		'image_path': '<LOCAL_PATH_TO_SOME_IMAGE_FILE>',
		'link': 'https://www.example.com/product_2',
		'name': 'Product 2',
		'description': 'This is Product 2'
	},
	{
		'image_path': '<LOCAL_PATH_TO_SOME_IMAGE_FILE>',
		'link': 'https://www.example.com/product_3',
		'name': 'Product 3',
		'description': 'This is Product 3'
	}
]

result = carousel_sample.create_carousel_ad(ad_account_id, page_id, 
	'https://www.example.com', 'https://www.facebook.com', 'hello message', 
	AdSet.OptimizationGoal.link_clicks, 
	AdSet.BillingEvent.impressions, 
	2, 
	'Auto Campaign',
	{
        Targeting.Field.geo_locations: {
            'countries': ['TW']
      	}
    },
    products
    )


print(result)
'''







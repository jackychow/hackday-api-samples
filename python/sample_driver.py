from facebookads.api import FacebookAdsApi
from facebookads import adobjects
from ads_reporting import AdsReportingSample

my_app_id = '<APP_ID>'
my_app_secret = '<APP_SECRET>'
my_access_token = '<ACCESS_TOKEN>'
proxies = {'http': '<HTTP_PROXY>', 'https': '<HTTPS_PROXY>'} # add proxies if needed
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)


'''
# Reporting Sample

report_sample = AdsReportingSample()
values = report_sample.get_ads_insight('act_<AD_ACCOUNT_ID>', '2018-04-11')
print(values)
'''







# Copyright (c) 2016-present, Facebook, Inc. All rights reserved.
#
# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.
#
# As with any software that integrates with the Facebook platform, your use of
# this software is subject to the Facebook Developer Principles and Policies
# [http://developers.facebook.com/policy/]. This copyright notice shall be
# included in all copies or substantial portions of the software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
# Custom Audiences Analyse

## Analysing performance of Ad Sets used custom audience.

***

This sample shows how to use the Custom Audiences API to analyse

## References:

* [Custom Audiences API doc][1]

[1]: https://developers.facebook.com/docs/marketing-api/reference/custom-audience/
"""
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.customaudience import CustomAudience
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adsinsights import AdsInsights


class CustomAudienceAnalyseSample:
    """
    The main sample class contains sub methods do each step of analysis.
    """
    def get_custom_audiences(
            self,
            account_id
    ):
        """
        retrieve custom audience under the ad account.
        """
        ad_act = AdAccount(account_id)
        result = ad_act.get_custom_audiences([
            CustomAudience.Field.name,
            CustomAudience.Field.data_source,
            CustomAudience.Field.subtype,
            CustomAudience.Field.approximate_count
        ])

        return result

    def get_ad_sets_for_custom_audience(
            self,
            ca_id
    ):
        """
        retrieve adsets which refer the custom audience
        """
        custom_audience = CustomAudience(ca_id)
        result = custom_audience.get_ads([Ad.Field.adset_id])
        adset_ids = []
        for ad in result:
            if ad[Ad.Field.adset_id] not in adset_ids:
                adset_ids.append(ad[Ad.Field.adset_id])
        return adset_ids

    def get_insights_for_ad_set(
            self,
            adset_id,
            date_preset=Ad.DatePreset.lifetime,
            limit=300
    ):
        """
        retrieve performance insight for each adset.
        """

        params = {
            'date_preset': date_preset,
            'action_attribution_windows': [
                AdsInsights.ActionAttributionWindows.value_default,
                AdsInsights.ActionAttributionWindows.value_1d_click,
                AdsInsights.ActionAttributionWindows.value_7d_click
            ],
            'level': AdsInsights.Level.adset,
            'limit': limit
        }

        adset = AdSet(adset_id)
        insights = adset.get_insights(
            [
                AdsInsights.Field.adset_name,
                AdsInsights.Field.adset_id,
                AdsInsights.Field.cpc,
                AdsInsights.Field.cpm,
                AdsInsights.Field.ctr,
                AdsInsights.Field.spend,
                AdsInsights.Field.clicks,
                AdsInsights.Field.impressions,
                AdsInsights.Field.reach,
                AdsInsights.Field.actions,
                AdsInsights.Field.action_values
            ],
            params
        )
        return insights

    def get_account_analyse(
        self,
        account_id,
        date_preset=Ad.DatePreset.lifetime,
        limit=300
    ):
        """
        retrieve account level insight for all campaigns under the ad account.
        """
        ad_account = AdAccount(account_id)

        params = {
            'date_preset': date_preset,
            'action_attribution_windows': [
                AdsInsights.ActionAttributionWindows.value_default,
                AdsInsights.ActionAttributionWindows.value_1d_click,
                AdsInsights.ActionAttributionWindows.value_7d_click
            ],
            'level': AdsInsights.Level.account,
            'limit': limit
        }
        insight = ad_account.get_insights(
            [
                AdsInsights.Field.cpc,
                AdsInsights.Field.cpm,
                AdsInsights.Field.ctr,
                AdsInsights.Field.spend,
                AdsInsights.Field.clicks,
                AdsInsights.Field.impressions,
                AdsInsights.Field.reach,
                AdsInsights.Field.actions,
                AdsInsights.Field.action_values
            ],
            params
        )
        purchase_insight = self.extract_purchase(insight[0])
        results = {
            "insight": insight,
            "purchase": purchase_insight
        }
        return results

    def get_custom_audience_analyse(
        self,
        account_id
    ):
        """
        composite logic to retieve metrics for custom audience based adsets.
        """
        results = []
        cache = {}
        caa = CustomAudienceAnalyseSample()
        custom_audience_list = caa.get_custom_audiences(account_id)

        for custom_audience in custom_audience_list:
            ca_level_result = {
                "id": custom_audience[CustomAudience.Field.id],
                "custom_audience": custom_audience
            }

            adsets = caa.get_ad_sets_for_custom_audience(
                custom_audience[CustomAudience.Field.id]
            )

            adset_level_result = []
            for adset_id in adsets:
                """
                skip api call if cache exist for the adset_id
                """
                if adset_id in cache:
                    insight = cache.get(adset_id)
                else:
                    insight = caa.get_insights_for_ad_set(adset_id)
                    cache[adset_id] = insight
                purchase_insight = {}
                if len(insight) > 0:
                    purchase_insight = self.extract_purchase(insight[0])
                adset_level_result.append(
                    {
                        "insight": insight,
                        "purchase": purchase_insight
                    }
                )
            ca_level_result["adsets"] = adset_level_result
            results.append(ca_level_result)
        return results

    def extract_purchase(
        self,
        insight
    ):
        """
        extract numbers from insight to handle easily in presentation.
        """
        data = {
            "cpm": float(insight[AdsInsights.Field.cpm]),
            "cpc": float(insight[AdsInsights.Field.cpc]),
            "ctr": float(insight[AdsInsights.Field.ctr]),
            "num": 0,
            "value": 0,
            "roas": None,
            "1d_click_num": 0,
            "1d_click_value": 0,
            "1d_click_roas": None,
            "7d_click_num": 0,
            "7d_click_value": 0,
            "7d_click_roas": None,
            "registration": None,
            "1d_click_registration": None,
            "7d_click_registration": None
        }

        for action in insight.get(AdsInsights.Field.actions, []):
            '''
            for mobile and web purchase
            '''
            if action["action_type"].find("purchase") != -1:
                data["num"] += int(action["value"])
                data["1d_click_num"] += int(action.get("1d_click", 0))
                data["7d_click_num"] += int(action.get("7d_click", 0))
            '''
            for mobile and web registration
            '''
            if action["action_type"].find("complete_registration") != -1:
                data["registration"] = int(action["value"])
                data["1d_click_registration"] = int(action.get("1d_click", 0))
                data["7d_click_registration"] = int(action.get("7d_click", 0))
                data["cpr"] = self.get_cpa(
                    action.get("value", 0),
                    insight[AdsInsights.Field.spend]
                )
                data["1d_click_cpr"] = self.get_cpa(
                    action.get("1d_click", 0),
                    insight[AdsInsights.Field.spend]
                )
                data["7d_click_cpr"] = self.get_cpa(
                    action.get("7d_click", 0),
                    insight[AdsInsights.Field.spend]
                )

        '''
        for purcahsed value
        '''
        for value in insight.get("action_values", []):
            if value["action_type"].find("purchase") != -1:
                data["value"] += float(value["value"])
                data["1d_click_value"] += float(value.get("1d_click", 0))
                data["7d_click_value"] += float(value.get("7d_click", 0))
                data["roas"] = self.get_roas(
                    data["value"],
                    insight[AdsInsights.Field.spend]
                )
                data["1d_click_roas"] = self.get_roas(
                    data["1d_click_value"],
                    insight[AdsInsights.Field.spend]
                )
                data["7d_click_roas"] = self.get_roas(
                    data["7d_click_value"],
                    insight[AdsInsights.Field.spend]
                )
        return data

    def get_roas(
        self,
        purchase_value,
        spend
    ):
        """
        calcluate return of ad spend for presentation.
        """
        roas = None
        if purchase_value > 0:
            roas = float(purchase_value) / float(spend) * 100
        return roas

    def get_cpa(
        self,
        count,
        spend
    ):
        """
        calculate cost per action for presentation.
        """
        cpa = None
        if count > 0:
            cpa = float(spend) / float(count)
        return cpa

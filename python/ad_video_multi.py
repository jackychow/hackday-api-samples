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
# Video multiple Upload

## uploading video under the ad account at once

***

## References:

* [Graph API Reference: Ad Account advideos][1]
* [Graph API Reference: Ad Video][2]

[1]: https://developers.facebook.com/docs/marketing-api/reference/ad-account/advideos
[2]: https://developers.facebook.com/docs/marketing-api/advideo/
"""

from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.advideo import AdVideo


class AdVideoMultiSample:
    """
    This class provides function to upload multiple video to
    ad account's assets.
    """

    def create_multiple_videos(
        self,
        accountid,
        video_urls,
    ):
        my_account = AdAccount(fbid=accountid)
        videos_created = []

        for video_url in video_urls:
            params = {
                'name': video_url,
                'file_url': video_url,
            }
            video = my_account.create_ad_video(
                params=params,
            )
            """
            instantiate AdVideo object from id.
            """
            video.Field = AdVideo.Field
            videos_created.append(AdVideo(fbid=video.get_id))

        return videos_created

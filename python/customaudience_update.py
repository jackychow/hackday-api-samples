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
# Custom Audiences Update

## Updating existing custom audiences with data

***

This sample shows how to use the Custom Audiences API to update a existing
 custom audience with specific data.

Using data from your CRM system, you can find your existing customers on
Facebook. You can then run campaigns to re-target those customers and/or
campaigns that target new customers and exclude existing ones.

## References:

* [Custom Audiences Users API doc][1]

[1]: https://developers.facebook.com/docs/marketing-api/reference/custom-audience/users/
"""
from facebook_business.adobjects.customaudience import CustomAudience


class CustomAudienceUpdateSample:
    """
    The main sample class.
    """
    def upload_users_to_audience(
            self,
            audienceid,
            users,
            schema=CustomAudience.Schema.email_hash):
        """
          Adds user emails to an existing audience. The SDK automatically hashes
          the emails. Only the hash is sent to Facebook.
        """
        audience = CustomAudience(audienceid)
        return audience.add_users(schema, users)

    def delete_users_from_audience(
            self,
            audienceid,
            users,
            schema=CustomAudience.Schema.email_hash):
        """
          Deletes user emails from an existing audience. The SDK automatically
          hashes the emails. Only the hash is sent to Facebook.
        """
        audience = CustomAudience(audienceid)
        return audience.remove_users(schema, users)

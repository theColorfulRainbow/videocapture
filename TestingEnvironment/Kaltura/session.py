# creates a Kaltura session

## cpde taken from https://developer.kaltura.com/workflows/Generate_API_Sessions/Authentication;step=4


from KalturaClient import *
from KalturaClient.Plugins.Core import *

config = KalturaConfiguration(2010302)
config.serviceUrl = "https://www.kaltura.com/"
client = KalturaClient(config)

# gets account info which contains Partner_ID, user_secret...
def get_account_info():
    partner_filter = KalturaPartnerFilter()
    pager = KalturaFilterPager()

    account_info = client.partner.listPartnersForUser(partner_filter, pager)
    print(account_info)
    return account_info # returns JSON containing info about account

## -- 1st way to log in --
def log_in():
    # Can be found by using kaltura credentials at https://kmc.kaltura.com/index.php/kmcng/settings/integrationSettings
    PARTNER_ID = 2010302
    SUB_PARTNER_ID = 201030200
    USER_ID = "mhopper@exseed.ed.ac.uk"
    USER_SECRET = "a5bfb183352b5163b7c3c9c1b658e82d"
    ADMIN_SECRET = "e277fb00c8bf67fadbc10320dc6e7d60"
    EXPIRY = 86400 # taken from the example (connect tutorial) they give, dont know what it means??
    KalturaSessionType_ADMIN = 2 #? https://raw.githubusercontent.com/kaltura/KalturaGeneratedAPIClientsPython/6e4a6a1f2650ec5bd02a89f31e95814f43b756b2/KalturaClient/Plugins/Core.py

    ks = client.session.start(ADMIN_SECRET, USER_ID, KalturaSessionType.ADMIN, 2010302, 86400)
    client.setKs(ks)
    return client
    # get_account_info()
## -- 1st way to log in --

## -- 2nd way to log in: doesnt seem to be best way hence use log in 1--
def log_in_2():
    login_id = "mhopper@exseed.ed.ac.uk"
    password = "changeme1%"
    partner_id = PARTNER_ID
    expiry = 86400
    privileges = "*"
    otp = ""

    result = client.user.loginByLoginId(login_id, password, partner_id, expiry, privileges, otp)
    print(result)
    get_account_info()
## -- 2nd way to log in --

def main():
    log_in()

if __name__ == "__main__":
    main()

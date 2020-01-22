from KalturaClient import *
from KalturaClient.Plugins.Core import *
from session import log_in

config = KalturaConfiguration(2010302)
config.serviceUrl = "https://www.kaltura.com/"
client = log_in()

def create_channel(name,description):
    return

def list_channels():
    filter = KalturaCategoryFilter()
    pager = KalturaFilterPager()

    result = client.category.list(filter, pager)
    for category in result.objects:
        print("ID: {}, FullName: {}".format(category.id, category.fullName))
    #print(result.objects)

def get_category(id):
    id = 35782132
    result = client.category.get(id)
    print(result.fullName)

def main():
    name = "James Channel"
    description = "Automated Python"
    list_channels()
    get_category(None)


if __name__ == "__main__":
    main()

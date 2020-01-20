from session import log_in
from KalturaClient import *
from KalturaClient.Plugins.Core import *

config = KalturaConfiguration(2010302)
config.serviceUrl = "https://www.kaltura.com/"
client = log_in()

def upload(video, name, description, category_id=None):
    upload_token = KalturaUploadToken()
    token = client.uploadToken.add(upload_token)
    token_id = token.id # seen from https://developer.kaltura.com/api-docs/General_Objects/Objects/KalturaUploadToken
    print("Token ID: {}".format(token.id))

    # creates video (object) to be uploaded
    upload_token_id = token_id
    file_data = open(video, 'rb')
    resume = False
    final_chunk = True
    resume_at = -1
    create_result = client.uploadToken.upload(upload_token_id, file_data, resume, final_chunk, resume_at)

    # uploads and adds media to https://kmc.kaltura.com/index.php/kmcng/content/entries/list
    entry = KalturaMediaEntry()
    entry.mediaType = KalturaMediaType.VIDEO
    entry.name = name
    entry.description = description
    upload_result = client.media.add(entry) # this result tells us info about entitledUsers e.g. entitledUsersEdit


    entry_id = upload_result.id
    print("Entry ID: {}".format(entry_id))
    resource = KalturaUploadedFileTokenResource()
    resource.token = token_id   #upload_token_id
    add_result = client.media.addContent(entry_id, resource)

    # for addeding to category
    #media_entry = KalturaMediaEntry()
    #media_entry.categoriesIds = category_id
    #update_category = client.media.update(entry_id, media_entry)

def main():
    video = "/afs/inf.ed.ac.uk/user/s16/s1645821/lecture_recording/TestingEnvironment/Kaltura/Kaltura_Logo_Animation.flv"
    name = "test upload"
    description = "testing upload from python script"
    upload(video, name, description)

if __name__ == "__main__":
    main()

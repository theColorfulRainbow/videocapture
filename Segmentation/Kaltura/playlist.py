from KalturaClient import *
from KalturaClient.Plugins.Core import *
from session import log_in

config = KalturaConfiguration(2010302)
config.serviceUrl = "https://www.kaltura.com/"
client = log_in()

def create_empty_playlist(name, description):
    playlist = KalturaPlaylist()
    playlist.playlistType = KalturaPlaylistType.STATIC_LIST
    playlist.description = description
    playlist.licenseType = KalturaLicenseType.COPYRIGHTED
    playlist.name = name
    update_stats = False
    playlist_update_result = client.playlist.add(playlist, update_stats)
    return playlist_update_result

# video ids
def create_filled_playlist(name, description, video_ids):
    # e.g. of adding content to playlist: playlist.playlistContent = "1_x6der17j,1_rynnrmrc" # id of the video to be added
    playlist = KalturaPlaylist()
    # converts list of strings into comma seperated string
    playlist.playlistContent = ','.join(map(str, video_ids))  # id of the video to be added e.g. "1_x6der17j,1_rynnrmrc"
    playlist.playlistType = KalturaPlaylistType.STATIC_LIST
    playlist.description = description
    playlist.licenseType = KalturaLicenseType.COPYRIGHTED   #copyright type
    playlist.name = name
    # playlist.categoriesIds = "1_egufe122" IDs for categories (channels) this playlist belongs to
    update_stats = False
    playlist_update_result = client.playlist.add(playlist, update_stats)
    return playlist_update_result   #probably want to save id e.g. playlist_update_result.id

def main():
    video_ids = ["1_x6der17j","1_rynnrmrc"] #ids of videos to add to playlist

    #create_empty_playlist("Empty Playlist","Description for empty playlist")
    create_filled_playlist("Filled Playlist","Description for empty playlist",video_ids)


if __name__ == "__main__":
    main()

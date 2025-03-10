import json
import urllib.request
import urllib.error
from urllib.parse import urlencode


class Subsonic(object):
    def __init__(self, baseUrl, apiKey, port, apiVersion, appName, serverPath):
        self._baseUrl = baseUrl
        self._apiKey = apiKey
        self._port = port
        self._apiVersion = apiVersion
        self._appName = appName
        self._serverPath = serverPath.strip('/')


    def getPlaylists(self, username=None):
        """
        since: 1.0.0

        Returns the ID and name of all saved playlists
        The "username" option was added in 1.8.0.

        username:str        If specified, return playlists for this user
                            rather than for the authenticated user.  The
                            authenticated user must have admin role
                            if this parameter is used

        Returns a dict like the following:

        {u'playlists': {u'playlist': [{u'id': u'62656174732e6d3375',
                               u'name': u'beats'},
                              {u'id': u'766172696574792e6d3375',
                               u'name': u'variety'}]},
         u'status': u'ok',
         u'version': u'1.5.0',
         u'xmlns': u'http://subsonic.org/restapi'}
        """
        methodName = 'getPlaylists'
        viewName = '%s.view' % methodName

        q = self._getQueryDict({'username': username})

        req = self._getRequest(viewName=viewName, query=q)
        res = self._doInfoReq(req)
        self._checkStatus(res)
        return res

    def getPlaylist(self, pid):
        """
        since: 1.0.0

        Returns a listing of files in a saved playlist

        pid:str      The ID of the playlist as returned in getPlaylists()

        Returns a dict like the following:

        {u'playlist': {u'entry': {u'album': u'The Essential Bob Dylan',
                          u'artist': u'Bob Dylan',
                          u'bitRate': 32,
                          u'contentType': u'audio/mpeg',
                          u'coverArt': u'2983478293',
                          u'duration': 984,
                          u'genre': u'Classic Rock',
                          u'id': u'982739428',
                          u'isDir': False,
                          u'isVideo': False,
                          u'parent': u'98327428974',
                          u'path': u"Bob Dylan/Essential Bob Dylan Disc 1/Bob Dylan - The Essential Bob Dylan - 03 - The Times They Are A-Changin'.mp3",
                          u'size': 3921899,
                          u'suffix': u'mp3',
                          u'title': u"The Times They Are A-Changin'",
                          u'track': 3},
               u'id': u'44796c616e2e6d3375',
               u'name': u'Dylan'},
         u'status': u'ok',
         u'version': u'1.5.0',
         u'xmlns': u'http://subsonic.org/restapi'}
        """
        methodName = 'getPlaylist'
        viewName = '%s.view' % methodName

        req = self._getRequest(viewName=viewName, query={'id': pid})
        res = self._doInfoReq(req)
        self._checkStatus(res)
        return res

    def createPlaylist(self, playlistId=None, name=None, songIds=[]):
        """
        since: 1.2.0

        Creates OR updates a playlist.  If updating the list, the
        playlistId is required.  If creating a list, the name is required.

        playlistId:str      The ID of the playlist to UPDATE
        name:str            The name of the playlist to CREATE
        songIds:list        The list of songIds to populate the list with in
                            either create or update mode.  Note that this
                            list will replace the existing list if updating

        Returns a dict like the following:

        {u'status': u'ok',
         u'version': u'1.5.0',
         u'xmlns': u'http://subsonic.org/restapi'}
        """
        methodName = 'createPlaylist'
        viewName = '%s.view' % methodName

        if playlistId == name == None:
            print ('You must supply either a playlistId or a name')
        if playlistId is not None and name is not None:
            print ('You can only supply either a playlistId '
                 'OR a name, not both')

        q = self._getQueryDict({'playlistId': playlistId, 'name': name})

        req = self._getRequest(viewName=viewName, listKey='songId', listValues=songIds, query=q)
        res = self._doInfoReq(req)
        self._checkStatus(res)
        return res

    def deletePlaylist(self, pid):
        """
        since: 1.2.0

        Deletes a saved playlist

        pid:str     ID of the playlist to delete, as obtained by getPlaylists

        Returns a dict like the following:

        """
        methodName = 'deletePlaylist'
        viewName = '%s.view' % methodName

        req = self._getRequest(viewName=viewName, query={'id': pid})
        res = self._doInfoReq(req)
        self._checkStatus(res)
        return res


    def search(self, query, artistCount=20, artistOffset=0, albumCount=20,
            albumOffset=0, songCount=20, songOffset=0, musicFolderId=None):
        """
        since: 1.4.0

        Returns albums, artists and songs matching the given search criteria.
        Supports paging through the result.

        query:str           The search query
        artistCount:int     Max number of artists to return [default: 20]
        artistOffset:int    Search offset for artists (for paging) [default: 0]
        albumCount:int      Max number of albums to return [default: 20]
        albumOffset:int     Search offset for albums (for paging) [default: 0]
        songCount:int       Max number of songs to return [default: 20]
        songOffset:int      Search offset for songs (for paging) [default: 0]
        musicFolderId:int   Only return results from the music folder
                            with the given ID. See getMusicFolders

        Returns a dict like the following:

        {u'searchResult2': {u'album': [{u'artist': u'A Tribe Called Quest',
                                u'coverArt': u'289347',
                                u'id': u'32487298',
                                u'isDir': True,
                                u'parent': u'98374289',
                                u'title': u'The Love Movement'}],
                    u'artist': [{u'id': u'2947839',
                                 u'name': u'A Tribe Called Quest'},
                                {u'id': u'239847239',
                                 u'name': u'Tribe'}],
                    u'song': [{u'album': u'Beats, Rhymes And Life',
                               u'artist': u'A Tribe Called Quest',
                               u'bitRate': 224,
                               u'contentType': u'audio/mpeg',
                               u'coverArt': u'329847',
                               u'duration': 148,
                               u'genre': u'default',
                               u'id': u'3928472893',
                               u'isDir': False,
                               u'isVideo': False,
                               u'parent': u'23984728394',
                               u'path': u'A Tribe Called Quest/Beats, Rhymes And Life/A Tribe Called Quest - Beats, Rhymes And Life - 03 - Motivators.mp3',
                               u'size': 4171913,
                               u'suffix': u'mp3',
                               u'title': u'Motivators',
                               u'track': 3}]},
         u'status': u'ok',
         u'version': u'1.5.0',
         u'xmlns': u'http://subsonic.org/restapi'}
        """
        methodName = 'search2'
        viewName = '%s.view' % methodName

        q = self._getQueryDict({'query': query, 'artistCount': artistCount,
            'artistOffset': artistOffset, 'albumCount': albumCount,
            'albumOffset': albumOffset, 'songCount': songCount,
            'songOffset': songOffset, 'musicFolderId': musicFolderId})

        req = self._getRequest(viewName=viewName, query=q)
        res = self._doInfoReq(req)
        self._checkStatus(res)
        return res

    def startScan(self):
        """
        since: 1.15.0

        Initiates a rescan of the media libraries.
        Takes no extra parameters.

        returns a dict like the following:

        {'status': 'ok', 'version': '1.15.0',
        'scanstatus': {'scanning': true, 'count': 0}}

        'scanning' changes to false when a scan is complete
        'count' starts a 0 and ends at the total number of items scanned

        """
        methodName = 'startScan'
        viewName = '%s.view' % methodName

        req = self._getRequest(viewName=viewName)
        res = self._doInfoReq(req)
        self._checkStatus(res)
        return res

    def _getQueryDict(self, d):
        """
        Given a dictionary, it cleans out all the values set to None
        """
        for k, v in list(d.items()):
            if v is None:
                del d[k]
        return d

    def _checkStatus(self, result):
        if result['status'] == 'ok':
            return True

    def _getRequest(self, viewName, listKey=None, listValues=None, query={}):
        """
        since: 1.0.0

        Create a urllib.request.Request object for the given viewName and query

        viewName: str       The name of the view to request
        listKey: str        The key for the list of values
        listValues: list    The list of values to include in the query
        query: dict         A dictionary of query parameters to include in the request

        Returns a urllib.request.Request object
        """
        qdict = {
            'apiKey': self._apiKey,
            'v': self._apiVersion,
            'c': self._appName,
            'f': 'json',
        }
        qdict.update(query)

        # Add the list values to the query dictionary if they exist
        if listKey and listValues:
            for value in listValues:
                qdict.setdefault(listKey, []).append(value)

        url = '%s:%d/%s/%s' % (self._baseUrl, self._port, self._serverPath, viewName)
        url += '?%s' % urlencode(qdict, doseq=True)
        req = urllib.request.Request(url)

        return req

    def _doInfoReq(self, req):
        """
        since: 1.0.0
        
        Try to open the request and return the result as a parsed dictionary

        req:urllib2.Request     The request to open

        Returns a parsed dictionary version of the result
        """
        _opener = urllib.request.build_opener()
        try:
            res = _opener.open(req)
            dres = json.loads(res.read().decode('utf-8'))
            return dres['subsonic-response']
        except urllib.error.HTTPError as e:
            print(f'HTTPError: {e.code} - {e.reason}')
            return None
        except Exception as e:
            print(f'Error: {e}')
            return None

    def ping(self):
        """
        since: 1.0.0

        Test the connection to the server

        Returns a boolean True if the server is alive, False otherwise
        """
        methodName = 'ping'
        viewName = '%s.view' % methodName

        req = self._getRequest(viewName=viewName)
        res = self._doInfoReq(req)
        if res and res.get('status') == 'ok':
            return True
        return False


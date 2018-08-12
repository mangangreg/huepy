import requests
import urllib.parse as parse
import json
import sys
sys.path.insert(0, '../lyric-colour')

import lycol
'''
This code is conforming to the Spotify API authorization guide, specifically the 'Authorization Code Flow'.
For more, see here:
https://developer.spotify.com/documentation/general/guides/authorization-guide/

'''
scope = 'user-read-currently-playing'
auth_url = 'https://accounts.spotify.com/api/authorize/'
access_url = 'https://accounts.spotify.com/api/token'


# Load your auth file
with open('auth.json', 'r') as rfile:
    auth=json.load(rfile)


def sp_authorize(client_id):
	'''
	Authorize the spotify app.

	Input: credentials
	Output: code
	'''
	auth_data = {'client_id':client_id,'response_type':'code', \
	             'redirect_uri':'https://github.com/mangangreg',\
	            'scope':scope,\
	            'grant_type':'client_credentials'}

	qstr = parse.urlencode(auth_data)

	# Build the url with the query string
	auth_req = auth_url +'?' + qstr
	
	# Print the URL to terminal, explain link, request user input
	print(auth_req,'\n')
	print("Follow the above link and if prompted log in to Spotify. NOTE: Don't use CTRL+C, it will fuck everything up.\n")
	redirect_url = input('When redirected to github.com/.... copy and the url and paste it in here:\n')
	print('\n')
	
	# Parse the response, save as a dictionary
	auth_response = parse.urlsplit(redirect_url)
	auth_response.query
	auth_dict = parse.parse_qs(auth_response.query)
	
	return auth_dict['code'][0] # Code returning as a singleton list for some reason, use [0]


def sp_access(code, client_id, client_secret):
		'''
		Request an access token from Spotify API using an authorization code.

		Input: Spotify API auth code and client ID and secret.
		Output: Spotify API access token
		'''
		post_data = {\
		"scope": scope,\
		 'client_id':client_id, \
		 'client_secret':client_secret,\
		 'redirect_uri':'https://github.com/mangangreg',\
		 'grant_type':'authorization_code',\
		 'code':code}

		# Post to the API endpoint using the data
		access_response = requests.post(access_url, data = post_data)

		# Save the response as a dictionary
		response_dict = (access_response.json())
		return response_dict['access_token']
		

def get_currently_playing(token):
	'''
	Make a GET request to Spotify API to find the currently playing track.

	Input: A spotify API access token.
	Output: A spotify response dict.
	'''
	data_response = requests.get('https://api.spotify.com/v1/me/player/currently-playing',headers = {'Authorization ':'Bearer '+token})

	if data_response.status_code != 200:
		# Should probably do something about that...
		pass

	return data_response.json()



class Track:
	'''
	A spotify track. Takes a spotify response dict as an input.
	'''

	def __init__(self,meta):
		self.json = meta
		self.artist = meta['item']['artists'][0]['name']
		self.track = meta['item']['name']

	def __str__(self):
		return 'Artist is {0} and track is {1}' .format(self.artist,self.track)

	def get_lyrics(self):
		pass

	def output(filepath):
		with open(filepath,'w') as outfile:
			json.dump(outfile)

# Script Sequence
code = sp_authorize(auth['id'])
token = sp_access(code, auth['id'], auth['secret'])
meta =get_currently_playing(token)
now = Track(meta)

print("You're currently listening to: ",now,'\n')

genius_url = lycol.genius_query_url(now.artist + '' + now.track)
lyrics = lycol.pull_genius(genius_url)
colours = lycol.colour_counter(lyrics)
print(colours)



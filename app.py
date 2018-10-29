import os
from flask import Flask,request,render_template,flash,redirect,url_for,session
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
DEVELOPER_KEY = "AIzaSyAvA6sL43AWqftNfVqx6Sl1Lz0JK2exFfY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(q,cat, max_results=50,order="relevance", token=None, location=None, location_radius=None ):

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet", # Part signifies the different types of data you want 
    maxResults=max_results,
    location=location,
    locationRadius=location_radius).execute()

    #print(search_response)
    title = []
    channelId = []
    channelTitle = []
    categoryId = []
    videoId = []
    viewCount = []
    likeCount = []
    dislikeCount = []
    commentCount = []
    favoriteCount = []
    category = []
    tags = []
    videos = []
    
    for search_result in search_response.get("items", []):
    	if search_result["id"]["kind"] == "youtube#video":

            title.append(search_result['snippet']['title']) 

            videoId.append(search_result['id']['videoId'])

            response = youtube.videos().list(
                part='statistics, snippet',
                id=search_result['id']['videoId']).execute()

            channelId.append(response['items'][0]['snippet']['channelId'])
            channelTitle.append(response['items'][0]['snippet']['channelTitle'])
            categoryId.append(response['items'][0]['snippet']['categoryId'])
            favoriteCount.append(response['items'][0]['statistics']['favoriteCount'])
            viewCount.append(response['items'][0]['statistics']['viewCount'])
            #likeCount.append(response['items'][0]['statistics']['likeCount'])
            if 'likeCount' in response['items'][0]['statistics'].keys():
                likeCount.append(response['items'][0]['statistics']['likeCount'])
            else:
                likeCount.append([])

            if 'dislikeCount' in response['items'][0]['statistics'].keys():
                dislikeCount.append(response['items'][0]['statistics']['likeCount'])
            else:
                dislikeCount.append([])    
            #dislikeCount.append(response['items'][0]['statistics']['dislikeCount'])
 
            if 'commentCount' in response['items'][0]['statistics'].keys():
                commentCount.append(response['items'][0]['statistics']['commentCount'])
            else:
                commentCount.append([])

            if 'tags' in response['items'][0]['snippet'].keys():
                tags.append(response['items'][0]['snippet']['tags'])
            else:
                tags.append([])

    youtube_dict = {'tags':tags,'channelId': channelId,'channelTitle': channelTitle,'categoryId':categoryId,'title':title,'videoId':videoId,'viewCount':viewCount,'likeCount':likeCount,'dislikeCount':dislikeCount,'commentCount':commentCount,'favoriteCount':favoriteCount}
    #print(viewCount.index(max(viewCount)))
    if cat=="View":
        return title[viewCount.index(max(viewCount))]
    elif cat=="Liked":
        return title[likeCount.index(max(likeCount))] 
    elif cat=="Disliked":
        return title[dislikeCount.index(max(dislikeCount))] 
    elif cat=="Comments":
        return title[commentCount.index(max(commentCount))]      


app = Flask(__name__, static_url_path="", static_folder="static")

app.secret_key = os.urandom(12)

@app.route('/')

@app.route('/index',methods=['GET','POST'])
def index():
	if request.method=="GET":
		return render_template("index0.html",result=None)
	else:
		v={}
		v["query"]=request.form["query"]
		v["cat"]=request.form["cat"]

		result=youtube_search(v["query"],v["cat"])
		return render_template("index0.html" , result=result)

if __name__ == "__main__":
	app.run(host = "0.0.0.0",debug=True, port=8080)

import json
import urllib
import urllib.request
import requests
import math
import collections
import pandas as pd
import matplotlib.pyplot as plot

APIKEY = "37YaqEVuiyY34g6h";
TO_URL = "https://api.songkick.com/api/3.0/search/artists.json?apikey={your_api_key}&query={artist_name}"
PAST_URL = "https://api.songkick.com/api/3.0/artists/{artist_id}/gigography.json?apikey={your_api_key}"
NUM_PAGES = 0

def get_artistID(artist):
    '''
    Obtain artist ID 

    '''

    url = TO_URL.replace("{your_api_key}", APIKEY)
    url = url.replace("{artist_name}", artist)
    
    data = requests.get(url)
    json_data = data.json()
    artist_data = json_data['resultsPage']['results']['artist'][0]
    artist_id = artist_data['id']
    print("Artist ID: " + str(artist_id))

    return str(artist_id), artist

def get_past_events(artist_id):
    
    events_url = PAST_URL.replace("{artist_id}", artist_id)
    events_url = events_url.replace("{your_api_key}", APIKEY)
    print("Artist past events url: " + events_url)
    print()

    data = requests.get(events_url)
    pastevents = data.json()
    return pastevents, events_url
    
def artist_event_dict(pastevents, events_url,artist):
   
    totalEntries = pastevents["resultsPage"]['totalEntries']
    perpage = pastevents["resultsPage"]['perPage']
    numpages = math.ceil(totalEntries / perpage) 
    # &page=
    to_num_pgs = 1
    add_and_pgs = events_url + '&page='
    past_events_url = add_and_pgs + str(to_num_pgs)

    event_in_US = dict()
    event_in_other = dict()
    lst = []



    while(to_num_pgs != numpages):
      
        data = requests.get(past_events_url)
        events = data.json()
        
        data = events['resultsPage']['results']['event']
        
        for event in data:
            country = event['venue']['metroArea']['country']['displayName']
           
            if(country == "US"):
                state = event['venue']['metroArea']['state']['displayName']
                lst.append(state)
                if(not state in event_in_US.keys()):
                    event_in_US[state] =1 
                    
                else:
                    event_in_US[state] +=1 
                    

            else:
                if(not country in event_in_other.keys()):
                    event_in_other[country] =1 
                    
                else:
                    event_in_other[country] +=1 
            
        to_num_pgs += 1
       # print(to_num_pgs)
        
        if(to_num_pgs >= 11):
            past_events_url = past_events_url[:-2] + str(to_num_pgs)
        else:
            past_events_url = past_events_url[:-1] + str(to_num_pgs)
        
    artist_event_in_US = {}
    artist_event_in_US[artist] = event_in_US

   # artist_event_in_other = {}
    #artist_event_in_other[artist] = event_in_other
    
    return artist_event_in_US#, artist_event_in_other
     
def location_guesser():
    
    aliana_lst = ['Nothing But Thieves','Phoebe Bridgers','Young The Giant'] #'bbno$', 'Angie McMahon', 'The Japanese House', 'Japanese Breakfast', 'Oliver Tree', 'Ramin Djawadi', 'Des Rocs','Sara Bareilles','Harry Styles','Liza Anne', 'Wallows', 'Lady Gaga','Mitiski','Kane Brown','Goth Babe','Max Richter', 'Conan Gray']
    nour_lst = ['The Vaccines', 'Radiohead', 'Led Zepplin']
    david_lst= ['Miguel', 'SAINt JHN', 'Bad Bunny', 'Frank Ocean', '6LACK']
    shravani_lst = ['Billie Eilish', 'Ariana Grande','Drake']
    where_to_live = {}

    for artist in aliana_lst:
        print(artist)
        try:
            artist_id,artist = get_artistID(artist)
        
            pastevents, events_url = get_past_events(artist_id)
        except KeyError:
            continue
        
        
        artist_event_in_US = artist_event_dict(pastevents, events_url,artist)
        artist_values = artist_event_in_US[artist]
        for state, num in artist_values.items():
            if(state in where_to_live.keys()):
                where_to_live[state] += num
            else:
                where_to_live[state] = num
    
    sorted_where_to_live = sorted(where_to_live.items(), key=lambda x: x[1], reverse=True)
    return sorted_where_to_live
    
def organize_data(where_to_live):
    top_10 = []
    bottom_10 = []
    for i in range(10):
        top_10.append(where_to_live[i])
    
    for i in range(1,11):
        bottom_10.append(where_to_live[-i])

    return top_10, bottom_10

def top_locations_bar(top_10):
 
    df_top = pd.DataFrame(top_10, columns =['State', 'Num']) 

    ax = df_top.plot.bar(x = 'State', y = 'Num', rot = 0, color=['darkslategrey','teal','orange','darkorange','indianred'])
    ax.set_title('Top 10 Locations')
    plot.show()

def bottom_locations_bar(bottom_10):
    df_bottom = pd.DataFrame(bottom_10, columns =['State', 'Num']) 
    ax2 = df_bottom.plot.bar(x = 'State', y = 'Num', rot = 0, color=['darkslategrey','teal','orange','darkorange','indianred'])
    ax2.set_title("Bottom 10 Locations")
    plot.show()
  
def top_locations_line(top_10):
    df_top = pd.DataFrame(top_10, columns =['State', 'Num']) 
    plot.plot(df_top['State'], df_top['Num'])
    plot.show()
    

def bottom_location_line(bottom_10):
    df_bottom = pd.DataFrame(bottom_10, columns =['State', 'Num']) 
    plot.plot(df_bottom['State'], df_bottom['Num'])
    plot.show()


def main():
    sorted_where_to_live = location_guesser()
    top_10,bottom_10 = organize_data(sorted_where_to_live)
    top_locations_bar(top_10)
    bottom_locations_bar(bottom_10)
   # top_locations_line(top_10)
    #bottom_location_line(bottom_10)

main()
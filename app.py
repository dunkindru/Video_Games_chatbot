from recommender import recommend
## INTENT AND RESPONSES

import re
from nltk.corpus import wordnet

# Building a list of Keywords
def list_word(word):
    global list_words 
    list_words.append(word)
    global list_syn
    for word in list_words:
        synonyms=[]
        for syn in wordnet.synsets(word):
            for lem in syn.lemmas():
                # Remove any special characters from synonym strings
                lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
                synonyms.append(lem_name)
        list_syn[word]=set(synonyms)
    global keywords
    # Defining a new key in the keywords dictionary
    keywords[word]=[]
    # Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
    for synonym in list(list_syn[word]):
        keywords[word].append('.*\\b'+synonym+'\\b.*')
    keywords[word].append('.*\\b'+word+'\\b.*')

def fun_keywords_dict():
    global keywords
    global keywords_dict
    for intent, keys in keywords.items():
        # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
        keywords_dict[intent]=re.compile('|'.join(keys))

#https://www.kaggle.com/nikdavis/steam-store-games?select=steam_media_data.csv
import pandas as pd 
df=pd.read_csv('steam_util.csv')

#request via api
import steamspypi
def query_in_api(request,intent=None):
    names=list()
    data_request = dict()
    data_request['request'] = request

    if intent!=None :
        data_request[request] = intent
    data = steamspypi.download(data_request)
    for key in data:
        names.append(data[key]['name'])
    return names[:10]

def top_by_column(intent):
    match=df.loc[df[intent]==1.0,:]
    match.rating.sort_values()
    result=match[0:10].name.values
    return result

#request via dataset
def query_in_dataset(name,intent):
    result=df.loc[df['name'] == name, intent].values[0]
    return result

# global variable initialized  in init_response
responses={}
list_words=[]
list_syn={}
keywords={}
keywords_dict={}
#we set Counter-Strike as default game 
name='Counter-Strike'
def init_response(name):
    # Building a dictionary of responses
    global responses
    responses={
        'hello':'Hello! I am a VideoGames ChatBot 🎮🤖\n    I have 3 skills:\n    1️⃣ Tell me the exact name of a game to get infos about it. (>VideoGames ideas< if you need)\n    2️⃣ Ask for a list of game with conditions about genre, platform... (>help< for more infos)\n    3️⃣ I can >recommend< a game that you might like 😁 ',
        'quit':'Thank you for visiting 👋',
        'fallback':'I dont quite understand.\n -Start by saying hello \n -If you need >help< just say it :)',
        #help and ideas 
        'help': 'I am a VideoGames ChatBot 🎮🤖 \n\n 1️⃣ I can give you informations about a video game as :\n \n-release date\n-platforms\n-required age\n-categories\n-genres\n-average playtime\n-number of owners\n-price\n-header image\n-general informations\n\n 2️⃣ You can also ask for a list of games with conditions about \n\ngenre as: Action, Soccer, Military... \ntype: fps, local, SteamVR... \nplatform: linux, mac, winfows',
        'ideas':'Here is a sample of some VideoGames ideas:'+'\n\n--- COPY PASTE THE GAME YOU WANT TO GET INFO ABOUT ---\n\n'+'\n'.join(df.sample(frac=1).name[0:10].values)+'\n\n--- COPY PASTE THE GAME YOU WANT TO GET INFO ABOUT ---',
        'bye': 'Thank you for your visit ! Have a good day 👋',
        #on one game
        'date': name+' was released on : '+query_in_dataset(name,'release_date'),
        'platforms':name+' is available on : '+query_in_dataset(name,'platforms'),
        'age': name+' require to be older than %d years old'%query_in_dataset(name,'required_age'),
        'genres':name+' is a %s game'%query_in_dataset(name,'genres'),
        'categories':name+' is categorized as '+query_in_dataset(name,'categories'),
        'playtime':name+' has an average playtime of %d minutes.'%query_in_dataset(name,'average_playtime'),
        'owners':name+' has %s owners.'%query_in_dataset(name,'owners'),
        'price': name+' costs %d $.'%query_in_dataset(name,'price'),
        'image': query_in_dataset(name,'header_image'),
        'informations':name+' '+query_in_dataset(name,'header_image')+' \ncosts %d $.'%query_in_dataset(name,'price')
        +'\nIs available on : '+query_in_dataset(name,'platforms')+'\nIs categorized as '+query_in_dataset(name,'categories')+' game'
        +'\n'+name+'require to be older than %d years old.'%query_in_dataset(name,'required_age'),

        #search with conditions via api
        'top':'Top 10 games on last 2 weeks: \n\n'+'\n'.join(query_in_api('top100in2weeks')),
        'action':'Some action games: \n\n'+'\n'.join(query_in_api('genre','Action')),
        'local':'Some local games: \n\n'+'\n'.join(query_in_api('tag','local')),

        #'recommend':"Based on your search we recommend you these games \n\n"+'\n'.join(recommend(user_memory))
    }
    for key in responses:
        list_word(key)
        fun_keywords_dict()



#user memory save all intents from user query in a list
user_memory=['hello']
def intent_response(user_query):

    global user_memory
    global name

    # Takes the user input and converts all characters to lowercase
    user_input = user_query.lower()

    # recommender system
    if 'recommend' in user_query:
        return "Based on your search we recommend you these games \n\n"+'\n'.join(recommend(user_memory))

    #else we go throught the intent entities
    matched_intent = None 

    for intent,pattern in keywords_dict.items():
        # Using the regular expression search function to look for keywords in user input
        if re.search(pattern, user_input): 
            # if a keyword matches, select the corresponding intent from the keywords_dict dictionary
            matched_intent=intent  
    # The fallback intent is selected by default
    key='fallback' 

    if matched_intent in responses:
        # If a keyword matches, the fallback intent is replaced by the matched intent as the key for the responses dictionary
        key = matched_intent
        #if bye we reset the user memory
        if key=='bye':
            user_memory=['hello']
        user_memory.append(key)
        # The chatbot return the response that matches the selected intent
        return (responses[key]) 

    #if there is no match in intents we try to see if there is the name of a game in the user query
    else:
        # set game's name
        if user_query.lower() not in list(responses.keys()):
            temp=df['name'].str.lower()
            a=temp[temp.str.contains(user_query.lower(),na=False)]
            if len(a)>0:
                name=df.iloc[a.index[0]]['name']
                user_memory.append(user_query)
                init_response(name)
                res='Ok let s switch to '+name+'\nWhat do you want to know ? (>help< if you want some ideas)\n'+query_in_dataset(name,'header_image')
                return res

        if user_query in df.name.values:
            #global name
            name=user_query
            user_memory.append(user_query)
            init_response(name)
            res='Ok let s switch to '+name+'\nWhat do you want to know ? (>help< if you want some ideas)\n'+query_in_dataset(name,'header_image')
            return res

    # if any column name of the dataset in the user query then we deliver a top of the games of the category
    user_query_list=user_query.split(' ')
    inter=list(set(user_query_list) & set(df.columns.values))
    if len(inter)!=0:
        user_memory.append(inter[0])
        res='\n'.join(top_by_column(inter[0]))
        return res


# ## CHATBOT DISCORD
# ### link for the discord bot 
# https://discord.com/oauth2/authorize?client_id=951418595987050597&scope=bot&permissions=8
import os
import discord
from dotenv import load_dotenv
load_dotenv(dotenv_path="config")
import json 

class MyClient(discord.Client):
    def __init__(self, model_name):
        super().__init__()
      
    async def on_ready(self):
        # print out information when the bot wakes up
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        #initialisation of the responses dict 
        init_response(name)
        print("bot is ready !")
        print('https://discord.com/oauth2/authorize?client_id=951418595987050597&scope=bot&permissions=8')

        #await message.channel.send("satrt by saying hello")

    async def on_message(self, message):
        """
        this function is called whenever the bot sees a message in a channel
        """
        # ignore the message if it comes from the bot itself
        if message.author.id == self.user.id:
            return
        #entities
        if message.content != "None": 
            #init_response(name)
            bot_response=intent_response(message.content)
            
        # if there is a problem
        if not bot_response:
           bot_response = 'Hmm... something is not right 🧐\nTry to say Hi 👋 '

        # send the model's response to the Discord channel
        if bot_response!= None:
            await message.channel.send(bot_response) 
            print(user_memory)

def main():
    client = MyClient("VideoGamesBot")
    client.run(os.getenv("DISCORD_TOKEN"))

if __name__ == '__main__':
  main()


# Video Games ChatBot 

Chatbot and Recommender System final project in ESILV A4 in 2022.
This project is a python application, developed by Daniel Lévy and Joshua Jeyaratnam.

⚠️THE TOKEN IS NOT THE GOOD ONE BECAUSE DISCORD DONT ALLOW TO PUBLISH IT ONLINE⚠️ 
ask for the token by email

Github:

https://github.com/dunkindru/Video_Games_chatbot

Videos:

running the app guide: https://youtu.be/lBvjEsJ7M5k

chatbot guide : https://www.youtube.com/watch?v=-L3_apstqfA

Link to connect the chatbot you have to invite it in a discord server:

https://discord.com/oauth2/authorizeclient_id=951418595987050597&scope=bot&permissions=8
 
There are here two projects in one ( **chatbot** + **recommender system**). 

A **chatbot** that has 3 main capabilities: 
 1. Give information about a game  
 2. Give a list of games according to criteria (platform, genre, type)
 3. recommend a list of games that you might like.
 
**Recommender System**:
During your exchanges the bot gets to know you and thanks to a database containing a list of players and their tastes an algorithm is able to propose a list of games that suits you.

## How to launch the application

 1. **Download** CHATBOTproject (unzip if needed)
 2. Open a **terminal**. 
 3. enter the folder >**cd** *your path for* /CHATBOTproject<  
 4. install the libraries via **Requirements.txt**. 
 5. launch the app with the command >**python app.py**< in the terminal
 
Each time you launch python app.py the user memory will be re-initialized and the recommender system will consider you as a different user (as well when you say bye).


# Files
In CHATBOTproject you will find :
|type| files | |
|--|--|--|
| **python** | app. py | recommender. py |
| **datasets** | steam_util.csv | steam_reco.csv |
| **configuration** | config | Requirements.txt |

## Configuration
**config** contain discord token to connect the chatbot. 

THE TOKEN IS NOT THE GOOD ONE BECAUSE DISCORD DONT ALLOW TO PUBLISH IT ONLINE

**Requirements.txt** contain the needed librairies to run the app

## Python
app. py is our discord chatbot 
recommender.py is our recommender system 

## Datasets

This is the link to our datasets :
https://www.kaggle.com/nikdavis/steam-store-games?select=steam_media_data.csv 

[[https://www.kaggle.com/nikdavis/steam-store-games?select=steam_media_data.csv](https://www.kaggle.com/nikdavis/steam-store-games?select=steam_media_data.csv)]

Columns in our dataset:
- name ( of games)
- release_date
- developer
- publisher
- platforms
- required_age
- categories
- genres
- steamspy_tags
- achievements
- positive_ratings
- negative_ratings
- average_playtime
- median_playtime
- owners  
- price

We used this dataset in order to respond to our user. Before using them we had to cleen these datasets. Data processing was a big part of this project. Because we removed all rows with na values but also columns that is not necessary for implementing our chatbot. We also merge and create new columns in order to have ratings values or others meaningfull values.

We have created a new rating column which is the average of the positive and negative ratings that we multiply by 10 to get a score out of 10.

## API
https://pypi.org/project/steamspypi/
We connected our chatbot to an API named steamspypi. We used this api to send us requests about games. We used the librarie steamspypi on Python in order to get results of requests. For instance if the user want some games given a certain genre. The API will return returns all games in a given genre.

# How it works :
Link to connect the chatbot you have to invite it in a discord server 
https://discord.com/oauth2/authorizeclient_id=951418595987050597&scope=bot&permissions=8
 

## Scenario

### scenario 1 : Ask for informations about a game  (ideas for games ideas if you need)

- Hello
- >Hello! I am a VideoGames ChatBot ....
- Give me some video games ideas?
- >Here is a sample of some VideoGames ideas: 
--- COPY PASTE THE GAME YOU WANT TO GET INFO ABOUT --- 
WIDE CROSS 
Neon Force Pushers 
Stellar Tactics
...
- WIDE CROSS 
- >Ok let s switch to WIDE CROSS What do you want to know ? (>help< if you want some ideas)
- at what age I can play this game
- >WIDE CROSS require to be older than 0 years old
- can I get information about this game
- >WIDE CROSS costs 0 $. 
Is available on : windows 
Is categorized as Single-player;Multi-player;Online Multi-Player;Co-op;Online Co-op;Cross-Platform Multiplayer;In-App Purchases game 
WIDE CROSSrequire to be older than 0 years old.

### scenario 2 : Ask for a list of game with conditions about genre, platform... (>help< for more infos)

- Hello

- >Hello! I am a VideoGames ChatBot ....

- Can i have some action games?

- > Some action games: Dota 2 Counter-Strike: Global Offensive ...

- Can i have some games I can play on linux  ?

- > Some linux games : Counter-Strike Team Fortress Classic Day of ....

### scenario 3: recommendation

After scnario 1 and 2 we can ask some recommendation based on your search

- Can you recommand me some games?

- > Based on your search we recommand you these games : Counter-Strike, Garry's Mod, Iron Snout....

- Ok thanks bye !

- > Thank you for your visit ! Have a good day

# Chatbot

We start by creating a dictionary that contains intent and responses for example 

hello': 'Hello! I am a VideoGames ChatBot...

then thanks to the nltk library we have created a dictionary which contains the list of synonyms associated to the key in this example we will have 

'hello': re.compile('.*\\bhowdy\\b.*|.*\\bhi\\b.*|.*\\bhullo\\b.*|.*\\bhello\\b.*|.*\\bhow do you do\\b.*|.*\\bhello\\b.*')

when adding the synonym we add the matchmaker regex form thanks to the creation of this intermediate dictionary the chatbot will be able to understand a large spectrum of words to better target the user's request.

We used the discord library to create our chatbot. 

The token for the discord bot is in the config file. On the GitHub we put the example of a token you will find the right config file in the mail we sent you.

When we launch the Bot we initialize the answers to save time when sending messages.

Then when the bot receives a message it just scans the dictionary for a matching key if it is not the case it looks if the user has not tried to say the name of a game.
If there is no match we have defined a default answer

When the user asks for an information or a list of games we call functions defined above (top_by_column,query_in_dataset,query_in_api) depending on the request we make a query via the api or in the dataset we have imported.



# Recommandation System
 
In this part we will discuss about our choice in order to design the best recommandation system.

Each time the user communicates with the bot we save what the user asks. We save the user's intents and entities. With the intents and entities our chatbot can in fact recommend 10 games that are related to his research.

We designed our solution with Python. Indeed our recommendation system uses the user's research on a game, the genre of a game or according to a platform. With this information our system will make a ranking with the best rated games while filtering the information on its preferences. The ranking gives the most played games according to the search. The recommendation system will not return a game that was already searched by the user.

We tried to model some machine learning model. We have tested to add 1 and 0 to our input with 302 columns containing each genres, type of plateforms etc..  We used a knn model with a k=5 and in output we had the 5 video games that were the most similar in terms of genres, platform types, and liked games. But the result was not relevant.

We designed our solution with Python.

# Conclusion

So we realized our Bot on discord. But we had a problem is that on Discord we did not find an API like [Wit.ai](http://Wit.ai) for facebook. So to treat the case of intents/entities we had to do otherwise. Despite this problem our Chatbot is complete. This project was very interesting and motivating. We decided to make a bot on Discord to learn new things. Indeed, in class we saw how to create a Chatbot with messengers. We wanted a challenge and to acquire new skills. We thank you for the advice and the quality of your teaching. We wish you all the best

import pandas as pd

def Ratings_best(data):
  data1=data.sort_values(by=['rating','average_playtime',	'owners'], ascending=False)
  return data1


def Add_genres(steam_data,user_query):
  query_user1=user_query
  for i in user_query:
    temp=steam_data[steam_data['name']==str(i)]
    if(len(temp)>0): 
      data=temp
      for index,row in data.iterrows():
        query_user1.append(row['genres'])  
  return query_user1

def Add_plateform(steam_data,user_query):
  plat=['windows;mac;linux', 'windows;mac', 'windows', 'windows;linux',
       'mac', 'mac;linux', 'linux']
  platform_name=''
  for i in user_query:
    if(i in plat):
      platform_name=i
  if(len(platform_name)<3):
    return steam_data[:30]
  else:
      temp=steam_data[steam_data['platforms'].str.contains(platform_name,na=False)]
      return temp[:30]

def recommend(user_query,steam_data=pd.read_csv("steam_reco.csv")):
  query_user=[x.lower() for x in user_query]

  genres_list=list()
  list_g=list()
  list_name=list()
  list_rat=list()
  list_own=list()
  list_hours=list()
  ##steam_data=Ratings(steam_data)
  steam_data=Ratings_best(steam_data)
  user_query=Add_genres(steam_data,user_query)
  for i in user_query:
    temp=steam_data[steam_data['genres'].str.contains(i,na=False)]
    
    if(len(temp)>3): 
      data=Add_plateform(steam_data,user_query)
      for index, row in data.iterrows():
        if(row["name"].lower() not in query_user):
          list_name.append(row["name"])
          list_g.append(row["genres"])
          list_rat.append(row['rating'])
          list_own.append(row['owners'])
          list_hours.append(row['average_playtime'])
  df = pd.DataFrame(list(list_name),
                columns =['Name'])
  df['Genres']=list_g
  df['Rating']=list_rat
  df['Owners']=list_own
  df['Play_time']=list_hours

  df=df.sort_values(by=['Rating','Play_time',	'Owners'], ascending=False)
  df=df['Name'].unique()
  return df[:10]
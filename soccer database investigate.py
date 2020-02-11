#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Project: Investigate the Soccer Database

# # Introduction
# Data set chose: Soccer Database
# This soccer database comes from Kaggle, it contains data for soccer matches, players, and teams from several European countries from 2008 to 2016. in this dataset, we have tables: Country, League, Match, Player, Player_Attributes, Team, Team_Attributes. The table Match is the biggest with 25979 records and 100 columns or variables. 
# For this project, we will work with 4 tables: Player, Player_Attributes, Team, Team_Attributes. We will conduct two separated analysis on the Teams and Players. For the purposes of the project, we will drop some variables from Player_Attributes and Team_Attributes. the following questions will be considered, while our investigation will go beyond:
# 1.	What teams improved the most over the time period? 
# 2.	Which players had the most penalties? 
# 3.	What team attributes lead to the most victories?

# ## Data Wrangling-interacting with database
# Before starting with the analysis we need to get our data ready for. the first step will be to connect with the database, using Python's built-in sqlalchemy and create_engine function :

# In[2]:


from sqlalchemy import create_engine
engine=create_engine("sqlite:///database.sqlite")
print(engine.table_names())


# ## reading of tables: Team, Team_Attributes,Player, Player_Attributes
# to do so we will use query"""     """

# # read and explore the Team table

# In[3]:


query="""
SELECT * FROM 'Team';
"""
Team=pd.read_sql(query,engine)
print(Team.head())


# In[21]:


Team.dtypes
Team.info()
Team.shape
Team.nunique
for i,v in enumerate(Team.columns):
    print(i,v)


# # Cleaning process ('Team' table)
# The table Team has 299 records and 5 colums or variables. We have some missing values for team_fifa_api_id, but we cannot fill them since it's about id, the fillna() using mean cannot be applied.

# # What teams improved the most over the time period? 
# The variables we will consider to evaluate the improvement of a team over the time are the Class variables: buildUpPlaySpeedClass,buildUpPlayDribblingClass,buildUpPlayPassingClass. From the table Team, we don't have any variables which can help to answer this question. We suggest to join through an inner join the two tables 'Team' and 'Team_Attributes'. We will start by reading the table 'Team_Attributes' for data wrangling and make it tidy.

# # read and explore the Team_Attributes table

# In[11]:


query="""
SELECT * FROM 'Team_Attributes';
"""
Team_Attribute=pd.read_sql(query,engine)
print(Team_Attribute.head())


# In[12]:


Team_Attribute.info()


# ## Cleaning process for this table
# In this table, there are too much missing data for the variable 'BuildUpPlayDribbling', then we will drop it. 

# #### Dropping of 'buildUpPlayDribbling'

# In[16]:


Team_Attribute.drop(['buildUpPlayDribbling'],axis=1,inplace=True)


# #### Inner Join and Tidyness
# For analysis purpose we need the name of the teams and specific variables, we will join the two tables 'Team' and 'Team_Attribute' through an Inner Join and keep the following variables: team_api_id, team_fifa_api_id,team_long_name,date,buildUpPlaySpeedClass,buildUpPlayDribblingClass,buildUpPlayPassingClass,buildUpPlayPositioningClass. The table will be tidy

# In[17]:


query="""
select team_long_name,Team_Attributes.team_fifa_api_id,Team_Attributes.team_api_id,Team_Attributes.date,Team_Attributes.buildUpPlaySpeed,Team_Attributes.buildUpPlayPassing
from Team
inner join Team_Attributes
using(team_api_id)
;"""
Team_Attributes=pd.read_sql(query,engine)
Team_Attributes
Team_Attributes.describe()


# In[25]:


Team_Attributes.groupby('team_long_name')['buildUpPlaySpeed'].mean().plot(kind='box')


# In[28]:


Team_Attributes.groupby('team_long_name')['buildUpPlayPassing'].mean().plot(kind='box')


# based on this boxplot, we can consider all the teams for which the buildUpPlaySpeed is > 70 and the buildUpPlayPassing is >=70 as teams which are improved over the period

# In[30]:


Team_Attributes[Team_Attributes['buildUpPlaySpeed']>70]


# #### The teams which are improved:
# Standard de Liège, West Ham United, Stoke City

# ## What team attributes lead to the most victories?

# To answer this question we will calculate the correlation between the variables :buildUpPlaySpeed, buildUpPlayPassing,chanceCreationPassing,chanceCreationCrossing,chanceCreationShooting,defencePressure,defenceAggression

#  ### Creation of numpy array with the above cited variables

# In[32]:


query="""
select buildUpPlaySpeed,buildUpPlayPassing,chanceCreationPassing,chanceCreationCrossing,chanceCreationShooting,defencePressure,defenceAggression
from Team_Attributes
;"""
Team_Attributes=pd.read_sql(query,engine)
arr1=np.array(Team_Attributes)


# #### Creation of a pearson correlation function

# In[36]:


def corr(V1,V2):
    "V1 and V2 should be numpy array"
    mean1=V1.mean()
    mean2=V2.mean()
    std1=V1.std()
    std2=V2.std()
    corr=((V1*V2).mean()-mean1*mean2)/(std1*std2)
    return corr


# In[47]:


corr(Team_Attributes.buildUpPlaySpeed,Team_Attributes.buildUpPlayPassing)


# In[48]:


Team_Attributes.corr()


# As a conclusion, we might say that buildUpPlaySpeed and buildUpPlayPassing are the Team Attributes which lead most to victories.

# # second part, in this part we will analyze the Players and Players_Attribute tables

# ## read and explore the Player table

# In[52]:


query="""
SELECT * FROM 'Player';
"""
Player=pd.read_sql(query,engine)
print(Player.head())


# In[53]:


Player.info()


# #### There's no missing data, datatypes are good

# ## read and explore the Player table

# In[50]:


query="""
SELECT * FROM 'Player_Attributes';
"""
Player_Attribute=pd.read_sql(query,engine)
print(Player_Attribute.head())


# In[51]:


Player_Attribute.info()


# There are a lot of missing data. For the purpose of the project, we will fill the missing values for the following variables:
# overall_rating, crossing, finishing, heading_accuracy,volleys,dribbling,ball_control,acceleration,sprint_speed,penalties,marking.

# #### Filling the missing values

# In[ ]:


Player_Attributes['overall_rating'].fillna(mean,inplace=True)


# In[ ]:


Player_Attribute.info()


# ## joining table
# Player and Player_Attribute

# In[ ]:


query="""
select Player.player_name,Player.height,Player_Attributes.player_fifa_api_id,Player_Attributes.overall_rating,Player_Attributes.crossing,Player_Attributes.finishing,Player_Attributes.heading_accuracy,
Player_Attributes.volleys,Player_Attributes.ball_control,Player_Attributes.acceleration,Player_Attributes.sprint_speed,Player_Attributes.penalties
, Player_Attributes.marking from Player
inner join Player_Attributes
using(player_fifa_api_id);
"""
Players=pd.read_sql(query,engine)
Players.head()


# In[28]:


query="""
select Player.player_name,Player_Attributes.penalties
from Player
inner join Player_Attributes
using(player_fifa_api_id);
"""
Player=pd.read_sql(query,engine)
Player.describe()


# ## Which players have the most penalities?

# In[38]:


query="""
select distinct Player.player_name,Player_Attributes.penalties,Player_Attributes.attacking_work_rate,Player_Attributes.overall_rating,Player_Attributes.ball_control,Player_Attributes.sprint_speed
from Player
inner join Player_Attributes
using(player_fifa_api_id)
group by player_name
order by penalties desc;
"""
Player=pd.read_sql(query,engine)
Player.head(20)


# ## is there a link between Attacking_work_rate and Penalties, overall_rating,ball_control,sprint_speed

# In[49]:


query="""
select avg(penalties),attacking_work_rate,avg(overall_rating),avg(ball_control),avg(sprint_speed)
from Player_Attributes
group by attacking_work_rate
order by penalties desc;
"""
attack=pd.read_sql(query,engine)
attack.head()


# ## link between penalties and sprint_speed

# In[56]:


query="""
select penalties,sprint_speed
from Player_Attributes
;
"""
Player=pd.read_sql(query,engine)
Player.plot(kind='scatter',x='penalties',y='sprint_speed')
plt.title('link between penalties and sprint_speed')
plt.show()


# there's a link between speed and penalties, more your sprint_speed is high the higher is the chance that you score on penalties.

# # Conclusions

# to analyse such a dataset you need to have a clear description of each variable. Due to the large amount of records and variables, we have to use classification mwthode or component principal analysis to go through. Analysis could have been conducted within group and between groups. 
# 
# For the team table, the parameter date for period made the analysis difficult, since the periods of time are not the same for the teams, data have been collected for day of match, it could have been good to have a single way to present the period, for instance we could have used the year. The period made it difficult to conduct univariate analysis.
# 
# As a large data set with few possibilities to go through all the records, it was important to refer to aggregate functions like mean or standard deviation. 

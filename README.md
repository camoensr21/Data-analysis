# Data-analysis-soccer database investigation
in this project I chose to work with a SQLite database. To read the tables I had to download DB Browser for SQLite.

# Data description
This soccer database comes from Kaggle, it contains data for soccer matches, players, and teams from several European countries from 2008 to 2016. in this dataset, we have tables: Country, League, Match, Player, Player_Attributes, Team, Team_Attributes. The table Match is the biggest with 25979 records and 100 columns or variables. For this project, we will work with 4 tables: Player, Player_Attributes, Team, Team_Attributes. We will conduct two separated analysis on the Teams and Players. For the purposes of the project, we will drop some variables from Player_Attributes and Team_Attributes. the following questions will be considered, while our investigation will go beyond:
What teams improved the most over the time period? 
Which players had the most penalties? 
What team attributes lead to the most victories?

# Coding stages
For this project, I wrote codes for the following stages:
## Data Wrangling-interacting with database¶
Before starting with the analysis we need to get our data ready for. the first step will be to connect with the database, using Python's built-in sqlalchemy and create_engine function 

## reading of tables: Team, Team_Attributes,Player, Player_Attributes¶
to do so we will use query""" """

## Cleaning process ('Team' table)¶
The table Team has 299 records and 5 colums or variables. We have some missing values for team_fifa_api_id, but we cannot fill them since it's about id, the fillna() using mean cannot be applied.

## What teams improved the most over the time period?
The variables we will consider to evaluate the improvement of a team over the time are the Class variables: buildUpPlaySpeedClass,buildUpPlayDribblingClass,buildUpPlayPassingClass. From the table Team, we don't have any variables which can help to answer this question. We suggest to join through an inner join the two tables 'Team' and 'Team_Attributes'. We will start by reading the table 'Team_Attributes' for data wrangling and make it tidy.

# second part, in this part we will analyze the Players and Players_Attribute tables

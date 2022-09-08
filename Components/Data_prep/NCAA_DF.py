import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import collections
import openpyxl
#https://www.rotowire.com/cbasketball/injury-report.php website for injury report

def NCAA_DF():
    #To process how long the code takes to run
    start_time = datetime.now()

    #School years to use
    years = range(2010,2022)
    headings_teams = [] # Headings for the file
    all_rows_teams = [] # will be a list for list for all rows

    for year in years:
        url = 'https://www.sports-reference.com/cbb/seasons/'+str(year)+'-school-stats.html'
        teams_name = requests.get(url)
        teams_names = teams_name.content
        soup = BeautifulSoup(teams_names, 'html.parser')


        Team_Names = soup.find_all("table", attrs={'id':'basic_school_stats'})
        table = Team_Names[0]
        body = table.find_all('tr')
        head = body[1]
        body_rows = body[2:]

        for item in head.find_all("th"): # loop through all th elements
    # convert the th elements to text and strip "\n"
            item = (item.text).rstrip("\n")
        # append the clean column name to headings
            headings_teams.append(item)
        #To insert year
        headings_teams.insert(39, 'Year')
        
            #print(body_rows[0])
        for row_num in range(len(body_rows)): # A row at a time
            row = [] # this will hold entries for one row
            for row_item in body_rows[row_num].find_all("td"): #loop through all row entries
    # row_item.text removes the tags from the entries
    # the following regex is to remove \xa0 and \n and comma from row_item.text
    # xa0 encodes the flag, \n is the newline and comma separates thousands in numbers
                aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
    #append aa to row - note one row entry is being appended
                row.append(aa)
        # append one row to all_rows
            row.append(year)
            all_rows_teams.append(row)    

    #Adding the team name to the beginning of the data frame
    NCAA_Teams1 = pd.DataFrame(data=all_rows_teams,columns=headings_teams[1:39])  
    NCAA_Teams1['NCAA Check?'] = NCAA_Teams1['School'].str.find('NCAA')
    NCAA_Teams1['School'] = NCAA_Teams1['School'].where(NCAA_Teams1['NCAA Check?']>0)
    NCAA_Teams1 = NCAA_Teams1.dropna()
    NCAA_Teams1.drop_duplicates(subset=['School', 'Year'], keep= 'first')
    NCAA_Teams1['School'] = NCAA_Teams1['School'].str.replace('NCAA', '')
    NCAA_Teams1.pop('NCAA Check?')
    NCAA_Teams1['Year'] = NCAA_Teams1['Year'].astype(int)
    NCAA_Teams1.columns = ['School', 'G', 'W', 'L', 'W-L%', 'SRS', 'SOS', ' ', 'Con-W', 'Con-L', ' ', 'Home-W', 'Home-L', ' ', 'Away-W', 'Away-L', ' ', 'Team Points', 'Opp. Points', ' ', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Year']

    headings_stats = [] # Headings for the file
    headings_stats.append('Year')
    headings_stats.append('School')
    all_rows_teams1 = [] # will be a list for list for all rows

    for index, row in NCAA_Teams1.iterrows():
        url1 = 'https://www.sports-reference.com/cbb/schools/'+row['School'].lower().\
            replace('uab','alabama-birmingham').\
                replace('utep','texas-el-paso').replace(' ', r'-').replace('(', '').replace(')', '').\
                    replace('&', '').replace("\'", '').replace('uc-', 'california-').replace('.', '').\
                        replace('university-of-california','california').\
                            replace('little-rock', 'arkansas-little-rock').\
                                replace('cal-state-long-beach', 'long-beach-state').\
                                    replace('louisiana', 'louisiana-lafayette').\
                                        replace('louisiana-lafayette-state', 'louisiana-state').\
                                            replace('unc-asheville', 'north-carolina-asheville').replace('utsa','texas-san-antonio').\
                                                replace('nc-state','north-carolina-state').replace('unc-wilmington','north-carolina-wilmington').\
                                                    replace('unc-greensboro','north-carolina-greensboro').replace('tcu','texas-christian')+'/'+str(row['Year'])+'.html'
        teams_name1 = requests.get(url1)
        teams_names1 = teams_name1.content
        soup1 = BeautifulSoup(teams_names1, 'html.parser')

        PG_Table = soup1.find_all("table", attrs={'id':'per_game'})
        table_stats = PG_Table[0]
        body1 = table_stats.find_all('tr')
        head1 = body1[0]
        body_rows1 = body1[1:]

        for item in head1.find_all("th"): # loop through all th elements
    # convert the th elements to text and strip "\n"
            item = (item.text).rstrip("\n")
        # append the clean column name to headings
            headings_stats.append(item)
        
            #print(body_rows[0])
        for row_num in range(len(body_rows1)): # A row at a time
            row1 = [] # this will hold entries for one row
            row1.insert(0,row['School'])
            row1.insert(0,row['Year'])
            for row_item in body_rows1[row_num].find_all("td"): #loop through all row entries
    # row_item.text removes the tags from the entries
    # the following regex is to remove \xa0 and \n and comma from row_item.text
    # xa0 encodes the flag, \n is the newline and comma separates thousands in numbers
                aa1 = re.sub("(\xa0)|(\n)|,","",row_item.text)
    #append aa to row - note one row entry is being appended
                row1.append(aa1)
        # append one row to all_rows
            all_rows_teams1.append(row1) 

    headings_stats.pop(2)
    NCAA_Stats = pd.DataFrame(data=all_rows_teams1,columns=headings_stats[0:27])

    #Changing values to float
    for num in headings_stats[4:27]:
        NCAA_Stats[str(num)] = pd.to_numeric(NCAA_Stats[str(num)], downcast='float')
        
    #Filling NAs
    NCAA_Stats.fillna(0, inplace=True)
    NCAA_Stats.pop('G')
    NCAA_Stats.pop('GS')
    NCAA_Stats.set_index('Year')
    NCAA_Stats.drop(index=(2020))

    #Adding in features for wins by round - to fix this. The variable is a local but needs to be a global. Make a list then append that list
    for i in range(1,7):
        exec("NCAA_Stats['Round_%d'] = 0" % i)

    for year in years:
        exec("NCAA_Stats%d = NCAA_Stats[NCAA_Stats['Year']== %d]" % (year, year))
        exec("NCAA_Stats1 = NCAA_Stats[NCAA_Stats['Year'] != %d]" % year)

        url_target = 'https://www.sports-reference.com/cbb/postseason/'+str(year)+'-ncaa.html'
        t = requests.get(url_target)
        t1 = t.content
        soup_t = BeautifulSoup(t1, 'html.parser')
        t_names = soup_t.find_all("div",  {'class': 'winner'})

        exec('t_list%d = []' % year)
        exec('round1%d = []' % year)
        exec('round2%d = []' % year)
        exec('round3%d = []' % year)
        exec('round4%d = []' % year)
        exec('round5%d = []' % year)
        exec('round6%d = []' % year)
    
        for winner in t_names:
            txt = str((winner.find('a')))
            txt1 = txt.split('>')
            txt2 = txt1[1].split('<')
            exec('t_list%d.append(txt2[0])' % year)
        
        if year == 2021:
            exec("t_list%d.append('Oregon')" % year)

    #creating round1 through round6

        exec("round1%d = [item for item, count in collections.Counter(t_list%d).items() if count > 0]" % (year, year))
        exec("round2%d = [item for item, count in collections.Counter(t_list%d).items() if count > 1]" % (year, year))
        exec("round3%d = [item for item, count in collections.Counter(t_list%d).items() if count > 2]" % (year, year))
        exec("round4%d = [item for item, count in collections.Counter(t_list%d).items() if count > 3]" % (year, year))
        exec("round5%d = [item for item, count in collections.Counter(t_list%d).items() if count > 4]" % (year, year))
        exec("round6%d = [item for item, count in collections.Counter(t_list%d).items() if count > 5]" % (year, year))
        
        for i in range(1,7):
            exec("lookup%d = NCAA_Stats%d['School'].isin(round%d%d) == True " % (i, year, i, year))
            exec("NCAA_Stats%d.loc[lookup%d, 'Round_%d'] = 1" % (year, i, i))

    for i in range(1,7):
        exec("NCAA_Stats = pd.concat([NCAA_Stats, NCAA_Stats%d])" % year)
    """
    #Entering in the injury report
    print('What is the name of the file your using for the injury report?')
    IR_file = (str(input())+'.csv')
    print('Where is the file?')
    file_path = str(input())
    os.chdir(file_path)

    Injury_report = pd.DataFrame(pd.read_csv(IR_file))
    player_list = Injury_report['Player'].to_list()
    IR_indicator = []

    #Removing injuried players from our dataframe
    for ir, row in NCAA_Stats.iterrows():
        if row['Year'] == 2022:
            if row['Player'] in player_list:
                IR_indicator.append(1)
            else:
                IR_indicator.append(0)
        else:
            IR_indicator.append(0)

    NCAA_Stats['IR Indicator'] = IR_indicator

    for person, row in NCAA_Stats.iterrows():
        if row['IR Indicator'] == 1:
            row.pop()
    """
    #Combining the per player data by team
    Bracket_Data = NCAA_Stats.groupby(['School', 'Year'], as_index=False).agg(
        {'MP':'sum',
        'FG':'sum',
        'FGA':'sum',
        'FG%':'mean',
        '2P':'sum',
        '2PA':'sum',
        '2P%':'mean',
        '3P':'sum',
        '3PA':'sum',
        '3P%':'mean',
        'FT':'sum',
        'FTA':'sum',
        'FT%':'mean',
        'ORB':'sum',
        'DRB':'sum',
        'TRB':'sum',
        'AST':'sum',
        'STL':'sum',
        'BLK':'sum',
        'TOV':'sum',
        'PF':'sum',
        'PTS':'sum',
        'Round_1': 'sum',
        'Round_2': 'sum',
        'Round_3': 'sum',
        'Round_4': 'sum',
        'Round_5': 'sum',
        'Round_6': 'sum',}
    )

    #Adding in SRS, SOS, OFF and DEF rating
    SOS_SRS = NCAA_Teams1[['Year', 'School','SRS', 'SOS', 'W', 'L', 'W-L%', 'Con-W', 'Con-L', 'Home-W', 'Home-L','Away-W', 'Away-L','Team Points', 'Opp. Points']].copy()
    Bracket_Data_Final = pd.merge(Bracket_Data, SOS_SRS, on=['School', 'Year'])
    cols = ['SRS', 'SOS', 'W', 'L', 'W-L%', 'Con-W', 'Con-L', 'Home-W', 'Home-L','Away-W', 'Away-L','Team Points', 'Opp. Points']
    Bracket_Data_Final[cols] = Bracket_Data_Final[cols].apply(pd.to_numeric, errors='coerce', axis=1)
    #In the future, it may be better to calculate a per play OFF and DEF rating to better assess the impact of injury
    OFF_rating = []
    DEF_rating = []
    Con_Per = []
    Home_Per = []
    Away_Per = []

    #Calculating columns to add in features
    for new, row in Bracket_Data_Final.iterrows():
        OFF = ((100) * ((row['Team Points']/(row['W']+row['L']))) / ((row['FGA']) - (row['ORB']) + (row['TOV']) + ((0.4) * (row['FTA']))))
        OFF_rating.append(OFF)
        DEF = ((100) * ((row['Opp. Points']/(row['W']+row['L']))) / ((row['FGA']) - (row['ORB']) + (row['TOV']) + ((0.4) * (row['FTA']))))
        DEF_rating.append(DEF)
        Con = ((row['Con-W']) / ((row['Con-W']+row['Con-L'])))
        Con_Per.append(Con)
        Home = ((row['Home-W']) / (((row['Home-W']+row['Home-L']))))
        Home_Per.append(Home)
        Away = ((row['Away-W'])/ (((row['Away-W']+row['Away-L']))))
        Away_Per.append(Away)

    Bracket_Data_Final['Offensive Rating'] = OFF_rating
    Bracket_Data_Final['Defensive Rating'] = DEF_rating
    Bracket_Data_Final['Con-W/L%'] = Con_Per
    Bracket_Data_Final['Home-W/L%'] = Home_Per
    Bracket_Data_Final['Away-W/L%'] = Away_Per

    return Bracket_Data_Final
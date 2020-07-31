# In[1]:
import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index)
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()

# In[3]:

def answer_one():
    return df['Gold'].idxmax()

answer_one()

# In[4]:

def answer_two():
    df['Gold_Diff'] = (df['Gold'] - df['Gold.1']).abs()
    return df['Gold_Diff'].idxmax()

answer_two()


# In[5]:

def answer_three():
    df['Gold_Rel'] = ((df['Gold'] - df['Gold.1']).abs())/df['Gold.2']
    only_gold = df[(df['Gold']>0) & (df['Gold.1']>0)]
    return only_gold['Gold_Rel'].idxmax()

answer_three()

# In[6]:

def answer_four():
    df['Points'] = df['Gold.2']*3 + df['Silver.2']*2 + df['Bronze.2']*1
    return df['Points']

answer_four()

# In[7]:

census_df = pd.read_csv('census.csv')
census_df.head()

# In[8]:

def answer_five():
    state = census_df['STNAME'].unique()
    x = 0
    s = ''
    for n in state:
        if x < len(census_df[(census_df['SUMLEV'] == 50) & (census_df['STNAME'] == n)]):
            x = len(census_df[(census_df['SUMLEV'] == 50) & (census_df['STNAME'] == n)])
            s = n
    return s

answer_five()

def answer_six():
    census_top = census_df[census_df['SUMLEV'] == 50].groupby('STNAME')['CENSUS2010POP'].nlargest(3).sum(level=0)
    return census_top.nlargest(3).index.values.tolist()

answer_six()

def answer_seven():
    column_keep = ['CTYNAME','POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']
    census_diff = census_df[census_df['SUMLEV'] == 50][column_keep].set_index('CTYNAME')
    census_diff['Change'] = census_diff.max(axis=1) - census_diff.min(axis=1)
    return census_diff['Change'].idxmax()

answer_seven()

# In[11]:

def answer_eight():
    column_keep2 = ['STNAME','CTYNAME']
    census_12 = census_df[((census_df['REGION'] == 1)|(census_df['REGION'] == 2)) & (census_df['POPESTIMATE2015']> census_df['POPESTIMATE2014']) & (census_df['CTYNAME'].str.startswith('Washington'))][column_keep2]
    return census_12.sort_index()
answer_eight()

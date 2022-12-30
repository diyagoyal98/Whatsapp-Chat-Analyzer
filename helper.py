from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter
exract=URLExtract()

def fetch_stats(selected_user,df):

    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    # 1 -> Fetching total number of messages
    num_messages = df.shape[0]
    # 2 -> Number of words
    words = []
    for msg in df['message']:
        words.extend(msg.split())
    # 3 -> count number of media file shared
    num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]

    # 4 -> counting urls
    links=[]
    for msg in df['message']:
        links.extend(exract.find_urls(msg))


    return num_messages,len(words),num_media_messages,len(links)



def most_active_user(df):
    x = df['user'].value_counts().head()
    df1 = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    df1.rename(columns={'index': 'name', 'user': 'percent'})
    return x,df1

def create_word_cloud(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    tmp = df[df['user'] != 'group_notification']
    tmp = tmp[tmp['message'] != '<Media omitted>\n']
    tmp = tmp[tmp['message'] != 'This message was deleted\n']

    f = open('all_stop_words.txt', 'r')
    stop_words = f.read()

    def remove_stop_words(message):
        words = []
        for wrd in message.lower().split():
            if wrd not in stop_words:
                words.append(wrd)

        return " ".join(words)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    tmp['message']=tmp['message'].apply(remove_stop_words)
    df_wc=wc.generate(tmp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    tmp = df[df['user'] != 'group_notification']
    tmp = tmp[tmp['message'] != '<Media omitted>\n']
    tmp = tmp[tmp['message'] != 'This message was deleted\n']

    f = open('all_stop_words.txt', 'r')
    stop_words = f.read()

    words = []
    for msg in tmp["message"]:
        for wrd in msg.lower().split():
            if wrd not in stop_words:
                words.append(wrd)

    return pd.DataFrame(Counter(words).most_common(25))


def emoji_analysis(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    em_t = []
    for i in range(emoji_df.shape[0]):
        em_t.append(emoji.demojize(emoji_df[0][i], delimiters=(" ", " ")))

    emoji_df['emoji_name'] = em_t

    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    timeline = df.groupby(['year', 'month_number', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time']=time
    return timeline


def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    return df['day_name'].value_counts()


def monthly_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    activity_heat=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return activity_heat





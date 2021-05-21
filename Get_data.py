import pandas as pd
import praw
import os
from dotenv import load_dotenv


#constant variables
envpath = ".env"
load_dotenv(envpath)


# def connect(clientid, secretid, userid):
#     """
#     This function will connect to the reddit api
#
#     returns:
#         This function will return a connection to the reddit api
#     """
#     connection = None
#     try:
#         connection = praw.Reddit(
#             client_id=clientid,
#             cilent_secret=secretid,
#             user_agent=userid
#         )
#         print("Connection Successful")
#     except:
#         print("Connection Unsuccessful. Please check your login Credentials.")
#     return connection
#


#os.environ.get("user")

def connect_reddit(client_id_input, client_secret_input, user_agent_input):
    '''
    This function will connect to the reddit API

    returns:
        A connection to the API

    example:
        reddit = connect_reddit(client_id_input = 'script key 14 char', client_secret_input = '28 char secret', user_agent_input = 'APP NAME')
    '''
    connection = None
    connection = praw.Reddit(
        client_id=client_id_input,
        client_secret=client_secret_input,
        user_agent=user_agent_input
    )
    return connection

con = connect_reddit(
    client_id_input=os.environ.get("clientid"),
    client_secret_input=os.environ.get("secretid"),
    user_agent_input=os.environ.get("user")
)
subreddits=["wallstreetbets"]

def get_reddit_data(rl,con=con,limit=100):
    """
    :param rl: list of subreddits
    :param con: connection to the reddit api
    :param limit: number of posts
    :return: Will return data from the subreddits
    """
    all_subreddit_data=[]
    for i in rl:
        subred=con.subreddit(i)
        hot_posts=subred.hot(limit=limit)
        df =[]
        for p in hot_posts:
#            print(p.author,p.url,p.title,p.ups,p.selftext,p.is_video,p.num_comments)
#            print(dir(p))
            data={
                "author":p.author,
                "url":p.url,
                "title":p.title,
                "upvotes":p.ups,
                "text":p.selftext,
                "video":p.is_video,
                "comments":p.num_comments,
                "saved":p.saved,
                "pinned":p.pinned,
                "awards":p.total_awards_received,
                "views":p.view_count,
#                "downvotes":p.downvote,
                "time":p.created_utc

            }
            df.append(data)
        alldf=pd.DataFrame(df)
        all_subreddit_data.append(alldf)
    return pd.concat(all_subreddit_data)
r_df = get_reddit_data(subreddits)

r_df.to_csv("data/csv/reddit_data_05_21_21.csv",index=False)


"""
Additional functions of the praw class
p.(saved, pinned, total_awards_received, view_count, downvote, created.utc)
"""

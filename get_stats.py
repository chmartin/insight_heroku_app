import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import io
import urllib.parse
import base64
from query_sql import query_sql


def make_plot_user(full_list,one_user):
    img = io.BytesIO()
    axis = plt.figure(figsize=(6,6))
    sns.distplot( full_list , color="mediumblue", label="All Users",bins=100,kde=False)
    plt.plot([one_user, one_user], [0, 800],'k--',label="This User")
    plt.legend()
    plt.ylabel("Number of Users")
    plt.xlabel("Probability to Churn [%]")
    plt.title("User's likelihood to Churn")

    plt.savefig(img, format='png')
    plt.savefig("./images/temp_user.png")
    img.seek(0)
    plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode())
    return plot_data

def make_plot_friends(full_list,one_user):
    img = io.BytesIO()
    axis = plt.figure(figsize=(6,6))
    sns.distplot( full_list , color="mediumblue", label="All Users friends",bins=100,kde=False)
    plt.plot([one_user, one_user], [0, 800],'k--',label="This Users friends")
    plt.legend()
    plt.ylabel("Number of Friend Groups")
    plt.xlabel("Community Score")
    plt.title("Community Scores")

    plt.savefig(img, format='png')
    plt.savefig("./images/temp_friends.png")
    img.seek(0)
    plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode())
    return plot_data

def get_stats(n):
    
    churn_prob = 0
    friends_prob = 0
    #Read Probabilities
    one_user = query_sql("SELECT * FROM users WHERE steamid = {0}".format(n))
    prob_churned_all_users = query_sql("SELECT Prob_Churned FROM users")
    friends_churned_all_users = query_sql("SELECT Prob_Churned_friends_mean FROM users")
    churn_prob = one_user[0][1]*100
    friends_score = (1-one_user[0][2])*100
    list_churn_prob = []
    for x in prob_churned_all_users:
        if x[0] is not None:
            list_churn_prob.append(x[0]*100)
    list_friends_prob = []
    for x in friends_churned_all_users:
        if x[0] is not None:
            list_friends_prob.append((1.-x[0])*100)
    plot_url_1 = make_plot_user(list_churn_prob,churn_prob)
    plot_url_2 = make_plot_friends(list_friends_prob,friends_score)
    add_friend = one_user[0][3]*100
    play_owned_game = one_user[0][4]*100
    community_profile = one_user[0][5]*100
    custom_avatar = one_user[0][6]*100
    allow_comments = one_user[0][7]*100
    same_fave_prob = one_user[0][8]*100
    play_0p05_more = one_user[0][9]*100
    #print("Got Probs: {0}, {1}".format(churn_prob,friends_prob))
    return [int(churn_prob), int(friends_score), plot_url_1, plot_url_2, int(add_friend), int(play_owned_game), int(community_profile), int(custom_avatar), int(allow_comments), int(same_fav_prob), int(play_0p05_more)]


import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import io
import urllib.parse
import base64


def make_plot_user(full_list,one_user):
    img = io.BytesIO()
    axis = plt.figure(figsize=(6,6))
    sns.distplot( full_list , color="maroon", label="All Users",bins=100,kde=False)
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
    sns.distplot( full_list , color="maroon", label="All Users friends",bins=100,kde=False)
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
    with open('./data/SteamChurn.json') as jsonfile:
        data=json.load(jsonfile)
        churn_prob = data.get('Prob_Churned').get(n)*100
        friends_prob = (1-data.get('Prob_Churned_friends_mean').get(n))*100
        list_churn_prob = [(x)*100 for x in list(data.get('Prob_Churned').values())]
        list_friends_prob = [(1-x)*100 for x in list(data.get('Prob_Churned_friends_mean').values())]
        plot_url_1 = make_plot_user(list_churn_prob,churn_prob)
        plot_url_2 = make_plot_friends(list_friends_prob,friends_prob)
    #print("Got Probs: {0}, {1}".format(churn_prob,friends_prob))
    return [int(churn_prob), int(friends_prob), plot_url_1, plot_url_2]


import base64
from github import Github
from github import InputGitTreeElement
import pandas as pd 
import urllib
import re
import requests
import io

user = "deshiyan1010"
password = "hopeyoudidntseethat"
g = Github(user,password)


def commit(file_lst=["db.csv"]):

    global g
    
    repo = g.get_user().get_repo('DataBase')
    file_list = file_lst

    file_names = file_lst
    commit_message = 'DB'
    master_ref = repo.get_git_ref('heads/master')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)
    element_list = list()
    for i, entry in enumerate(file_list):
        with open(entry) as input_file:
            data = input_file.read()
        if entry.endswith('.png'):
            data = base64.b64encode(data)
        element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
        element_list.append(element)
    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)

def pull():

    global g

    repo = g.get_user().get_repo('DataBase')
    contents = repo.get_contents("db.csv")
    file_content = repo.get_contents(urllib.parse.quote(contents.path))
    

    url = file_content.download_url
    s = requests.get(url).content
    csv = pd.read_csv(io.StringIO(s.decode("utf-8")))
    csv = csv[["Name","Country Code","Phone Number","DaysLeft","State","District"]]
    return csv


def save_csv(csv):

    csv = csv[["Name","Country Code","Phone Number","DaysLeft","State","District"]]
    csv.to_csv("db.csv")
    commit()


if __name__=="__main__":
    pull()
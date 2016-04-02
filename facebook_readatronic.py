from facebook_secret import *
from facebook import *

graph = GraphAPI(APP_TOKEN)
profile = graph.get_object('me')
posts = graph.get_connections(profile['id'], 'posts')

def print_post(post):
    if 'name' in post['from']:
        print('\t\t', post['from']['name'])
    else:
        print('<no name>')
    if 'message' in post:
        print(post['message'])
    elif 'link' in post:
        print(post['link'])
    else:
        print(post.keys(), '\n-----')
    print('')


for i in range(3):
    try:
        [some_action(post=post) for post in posts['data']]
        posts = requests.get(posts['paging']['next']).json()
    except KeyError:
        break

#TODO: access activity feed, not wall

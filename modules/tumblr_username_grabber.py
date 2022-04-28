import random

import pytumblr
from modules.profanity_filter import profanityFilter, nameFilter


client = pytumblr.TumblrRestClient(
    'w90o8d0Zph49QjmuffSiYhpeEjVwMbYgkf4nQkaIFm6AA7PLcW',
    'XKYtiqV1G5D6I4tDNoEV3lB1ILlKjqQrxvNqxOYZONisRttUez',
    'feLyWXvlxnlexjUq6ThjB31XrlA5XYttpTWn5dfzY6tdQaPaII',
    'UTEnTUstV006CX9pyptiJDBICB8YIF3IRJjXRLEefkX5xKenqe',
)


def grab_usernames():
    offset = 0
    while True:
        t_f = random.choice(['tags', 'accounts'])
        # t_f = 'accounts'
        if t_f == 'accounts':
            accounts = ['iloveyou',
                        'difficult']  # TODO: add more
            random.shuffle(accounts)
            cposts = client.posts(accounts[0],
                                  limit=20,
                                  offset=20 * (random.randint(0, 4)),
                                  reblog_info=True,
                                  notes_info=True)

            # get the 'posts field of cposts(the response)'
            posts = cposts['posts']
            if not posts:
                pass

            usernames = []
            random.shuffle(posts)
            for notes in posts:
                try:
                    note_list = notes['notes']
                    random.shuffle(note_list)
                    for note in note_list:
                        # now check for any censored words in username
                        if profanityFilter(note['blog_name']) is True:  # if username contains censored word(s)
                            continue
                        if nameFilter(note['blog_name']) is True:  # if username contains a boy's first name
                            continue
                        if note == accounts[0]:
                            continue
                        usernames.append(note['blog_name'])
                        offset += 20
                except KeyError as e:
                    pass
                    if len(usernames) > 10:
                            break
                users = []
                for usr in set(usernames):
                    rand_ext = ['.', '_']
                    rand_choice = random.choice(['true', 'false'])
                    if rand_choice == 'true':  # aka, use . and/or _ in username for Instagram
                        username = ''.join('%s%s' % (x, random.choice(rand_ext) if random.random() > 0.5 else '') for x in usr)
                    else:
                        username = set(usernames).pop()
                    if username.strip()[-1] == '.' or username.strip()[-1] == '_':
                        continue
                    if len(username) > 30:
                        continue

                    line = ''.join(c for c in username if c not in '?:!/;$@#&*-')  # get out asterisks
                    users.append(line)

                random.shuffle(users)
                if len(users) > 0:
                    # return set(users).pop()
                    with open("tumblr_usernames.txt", 'w+') as f:
                        f.writelines((set(users.pop())))
                else:
                    print('Found no suitable names from Tumblr, retrying...')
                    continue

        elif t_f == 'tags':
            print('Attempting to find Tumblr usernames from random tagged posts..')
            tags = ['GIF',
                    'LOL',
                    'Fashion',
                    'Art',
                    'Vintage',
                    'Illustration',
                    'Animals',
                    'Food',
                    'Films',
                    ]
            random.shuffle(tags)
            for tag in tags:
                tag_select = client.tagged(tag)
                random.shuffle(tag_select)
                usernames = []
                for post in tag_select:
                    try:
                        blog_name = post['blog_name']
                        cposts = client.posts(blog_name, notes_info=True)
                        for notes in cposts['posts'][0]['notes']:
                            # now check for any censored words in username
                            if profanityFilter(notes['blog_name']) is True:  # if username contains censored word(s)
                                continue
                            if nameFilter(notes['blog_name']) is True:  # if username contains a boy's first name
                                continue
                            usernames.append(notes['blog_name'])
                    except KeyError as e:
                        pass
                    if len(usernames) > 10:
                        break
                if len(usernames) > 10:
                    break
            users = []
            for usr in set(usernames):
                print(usr)
                rand_ext = ['.', '_']
                rand_choice = random.choice(['true', 'false'])
                if rand_choice == 'true':  # aka, use . and/or _ in username for Instagram
                    username = ''.join('%s%s' % (x, random.choice(rand_ext) if random.random() > 0.5 else '') for x in usr)
                else:
                    username = set(usernames).pop()
                if username.strip()[-1] == '.' or username.strip()[-1] == '_':
                    continue
                if len(username) > 30:
                    continue

                line = ''.join(c for c in username if c not in '?:!/;$@#&*-')  # get out asterisks
                users.append(line)

            random.shuffle(users)
            if len(users) > 0:
                # return set(users).pop()
                with open("tumblr_usernames.txt", 'w+') as f:
                    f.writelines((set(users.pop())))
            else:
                print('Found no suitable names from Tumblr, retrying...')
                continue


if __name__ == '__main__':
    print(grab_usernames())

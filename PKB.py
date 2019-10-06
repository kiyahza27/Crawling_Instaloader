import instaloader
import pandas as pd
import time

#akun yang ingin di crawling

username = "akuntarget"
L = instaloader.Instaloader(max_connection_attempts=0)
L.login("username", "password")

akun_pertama = instaloader.Profile.from_username(L.context, username)

#membuat kolom

captionlist = []
hashtaglist = []
likeslist = []
commentlist = []
followerlist = []
usernamelist = []

#crawling data akun yang dituju
count = 1
for post in akun_pertama.get_posts():
        print("mengambil data dari akun " + username + " post ke " + str(count) + " dari " + str(akun_pertama.mediacount))
        caption = post.caption
        if caption is None:
            caption = ""
        if caption is not None:
            caption = caption.encode('ascii', 'ignore').decode('ascii')
        hashtag = post.caption_hashtags
        likes = post.likes
        
        comments = []
        for comment in post.get_comments() :
            comments.append(comment.text.encode('ascii', 'ignore').decode('ascii'))

        usernamelist.append(username)
        captionlist.append(caption)
        hashtaglist.append(hashtag)
        likeslist.append(likes)
        commentlist.append(comments)
        count = count+1
        
#mengambil data akun followers dari akun yang dituju
        
followers = []
count_account = 1
for follower in akun_pertama.get_followers():
    username_follower = follower.username
    akun_follower = instaloader.Profile.from_username(L.context, username_follower)
    if akun_follower.is_private == True:
        print("Profile Instagram dengan username " + username_follower + " tidak bisa diakses karena akun privat")
    count = 1
    for post in akun_follower.get_posts():
        print("mengambil data dari " + username_follower + " post ke " + str(count) + " dari " + str(akun_follower.mediacount) + ", follower ke " + str(count_account) + " dari " + str(akun_pertama.followers))
        caption = post.caption
        if caption is None:
            caption = ""
        if caption is not None:
            caption = caption.encode('ascii', 'ignore').decode('ascii')
        
        hashtag = post.caption_hashtags
        likes = post.likes
        
        comments = []
        for comment in post.get_comments() :
            comments.append(comment.text.encode('ascii', 'ignore').decode('ascii'))

        usernamelist.append(username_follower)
        captionlist.append(caption)
        hashtaglist.append(hashtag)
        likeslist.append(likes)
        commentlist.append(comments)
        count = count+1
    count_account = count_account + 1

#menjadikan data yang diambil menjadi data tabel
data = pd.DataFrame({"Account":usernamelist, "Post":captionlist, "Tag":hashtaglist, "Likes":likeslist, "Comments":commentlist})
timestring = time.strftime("%Y%m%d_%H%M%S")
data.to_csv('PKB_Cindi_Zakiyah.csv')

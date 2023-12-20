from flask import Blueprint, render_template, flash,jsonify,request, redirect, url_for
from .models import Post, User, Follow, Like, Comment
from . import db
import json
import os
import spotipy
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth',__name__)
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import requests


#SPOTIFY
client_id = "a9a46f5b920244b28781d1f759a0eae8"
client_secret = "5b47819a5965468fb52a7519ffd5d5e0"
# Use the Spotipy client credentials manager to authenticate with the API
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

views = Blueprint('views',__name__)

global main_username
main_username=""
global profile_picture
profile_picture= ""
global profile_pic_base64
global profile_bio
profile_bio= ""

global searched_account
global num_of_posts
global all_post_names
global all_post_artists
global all_post_covers

global track1_name
global track1_artist
global cover_image_url1
global preview_audio1
global track1_url
global track1_id

global track2_name
global track2_artist
global cover_image_url2
global preview_audio2
global track2_url
global track2_id

global track3_name
global track3_artist
global cover_image_url3
global preview_audio3
global track3_url
global track3_id

global track4_name
global track4_artist
global cover_image_url4
global preview_audio4
global track4_url
global track4_id





@views.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first( )

        if user:
            flash('email already exist', category='error')
        elif len(email) < 4:
            flash('email must be greated 4 char', category='error')
        elif len(username) < 2:
            flash('name must be greated 2 char', category='error')
        elif len(password1) < 1:
            flash('password must be longer then 1 char', category="error")
        elif password1 != password2:
            flash('password dont match', category='error')

        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method="sha256"),
                            profile_pic="noth", bio="noth", followers=0, following=0, num_of_posts=0)
            db.session.add(new_user)
            db.session.commit( )
            flash("account created", category='success')
            login_user(new_user, remember=True)
            global main_username
            main_username = username
            return redirect(url_for('views.post'))
    return render_template("sign_up.html", user=current_user, main_username=main_username)


@views.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        password= request.form.get('password')
        user=User.query.filter_by(email=email).first()
        global main_username
        main_username=user.username
        global profile_picture
        profile_picture=user.profile_pic
        if user:
            if check_password_hash(user.password, password):
                flash('logged in',  category='success')
                login_user(user, remember=True)
                follow_requests = Follow.query.filter_by(username_followed=main_username, accepted=0).all( )
                data = []
                for requests in follow_requests:
                    user = User.query.filter_by(username=requests.username_follower).first( )
                    if user:
                        data.append({
                            'username_follower': requests.username_follower,
                            'profile_pic': user.profile_pic
                        })
                return render_template("home.html", user=current_user, main_username=main_username, profile_pic=profile_picture, data=data)

            else:
                flash('incorrect password', category='error')

        else:
            flash('email does not exist', category='error')
    return render_template("login.html", user=current_user)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login'))





@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    import base64
    global profile_bio

    current = User.query.filter_by(username=main_username).first( )
    my_bio = current.bio
    my_pic = current.profile_pic

    if request.method == 'POST':
        if 'text_input' in request.form:
            new_bio = request.form['text_input']

            current = User.query.filter_by(username=main_username).first( )
            current.bio = new_bio
            db.session.commit( )
            flash('Profile bio updated', category='success')

            return render_template("edit_profile.html", user=current_user, main_username=main_username,
                                   profile_pic=my_pic,
                                   profile_bio=new_bio)

        elif 'image_input' in request.files:
            image = request.files['image_input']
            image_data = image.read( )
            new_pic = base64.b64encode(image_data).decode('utf-8')

            current = User.query.filter_by(username=main_username).first( )
            current.profile_pic = new_pic
            db.session.commit( )
            flash('Profile pic updated', category='success')

            return render_template("edit_profile.html", user=current_user, main_username=main_username,
                                   profile_pic=new_pic,
                                   profile_bio=my_bio)

    db.session.commit( )

    return render_template("edit_profile.html", user=current_user, main_username=main_username, profile_pic=my_pic,
                           profile_bio=my_bio)

@views.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    global main_username
    global profile_picture
    global profile_bio

    # Retrieve all rows from the User table where the name is...
    users_personal = User.query.filter_by(username=main_username).first( )
    my_posts = Post.query.filter_by(username=main_username).all( )

    profile_picture = users_personal.profile_pic
    profile_bio = users_personal.bio

    num_of_posts = 0
    for post in my_posts:
        num_of_posts +=1


    if request.method == 'POST':
        if request.form['button'] == 'Followers':
            users_that_follow_me = Follow.query.filter_by(username_followed=main_username, accepted=1).all( )

        elif request.form['button'] == 'Following':
            users_that_I_follow = Follow.query.filter_by(username_follower=main_username, accepted=1).all( )

    users_that_request_me = Follow.query.filter_by(username_followed=main_username, accepted=0).all( )
    users_that_follow_me = Follow.query.filter_by(username_followed=main_username, accepted=1).all( )
    users_that_I_follow = Follow.query.filter_by(username_follower=main_username, accepted=1).all( )

    return render_template("profile.html", user=current_user, my_posts=my_posts, followers=users_that_follow_me, following=users_that_I_follow,
                           requests=users_that_request_me,
                           profile_bio=profile_bio,
                           main_username=main_username, profile_pic=profile_picture,
                           num_of_posts=num_of_posts)

@views.route("/show", methods=["GET", "POST"])
def show_followers():

    if request.method == "POST":
        users_that_I_follow = Follow.query.filter_by(username_followed=main_username, accepted = 0).all( )
        for follower in users_that_I_follow:
            decision = request.form.get(follower.username_follower)
            if decision == "accept":
                follower.accepted = True
                add_followers_to_me = User.query.filter_by(username=main_username).first( )
            else:
                follower.accepted = False
            db.session.commit()
    users_that_I_follow = Follow.query.filter_by(username_followed=main_username, accepted = 0).all( )
    return render_template("profile.html", followers=users_that_I_follow, user=current_user)

"""
@views.route("/follow_requests", methods=["GET", "POST"])
def follow_requests():
    numberOfRequests = 0
    users_that_request_me = Follow.query.filter_by(username_followed=main_username, accepted=0).all( )
    print(users_that_request_me)
    
    for follower in users_that_request_me:
        numberOfRequests += 1
        decision = request.form.get(follower.username_follower)
        
        if decision == "accept":
            follower.accepted = True
            add_followers_to_me = User.query.filter_by(username=main_username).first( )
            add_followers_to_me.followers = add_followers_to_me.followers + 1

            add_following_to_user = User.query.filter_by(username=follower.username_follower).first( )
            add_following_to_user.following = add_following_to_user.following + 1

            flash('You have accepted the follow request', category='success')
        else:
            follower.accepted = False
            delete_request = Follow.query.filter_by(username_followed=main_username,
                                                    username_follower=follower.username_follower).first( )
            db.session.delete(delete_request)
            flash('you have decline the follow request', category='error')
        
    db.session.commit( )

    return render_template("home.html", user=current_user, requests=users_that_request_me)
"""




global song_name
global song_artist
global song_link
global audio_link
global album_cover
global user_id
global username
global profile_pic

@views.route("/post", methods=['GET', 'POST'])
@login_required
def post():
    global search

    global track1_name
    global track1_artist
    global cover_image_url1
    global preview_audio1
    global track1_url
    global track1_id

    global track2_name
    global track2_artist
    global cover_image_url2
    global preview_audio2
    global track2_url
    global track2_id

    global track3_name
    global track3_artist
    global cover_image_url3
    global preview_audio3
    global track3_url
    global track3_id

    global track4_name
    global track4_artist
    global cover_image_url4
    global preview_audio4
    global track4_url
    global track4_id

    global song_name
    global song_artist
    global song_link
    global audio_link
    global album_cover
    global user_id
    global username
    global profile_pic

    global main_username
    if request.method == 'POST':
        if request.form['submit_button'] == 'Search':
            try:
                track_name = request.form.get('song_name')

                # Search for a track by its name and artist
                results = sp.search(q=f'track:{track_name}', type='track')

                # Get the first track from the search results
                track1 = results['tracks']['items'][0]
                track2 = results['tracks']['items'][1]
                track3 = results['tracks']['items'][2]
                track4 = results['tracks']['items'][3]

                track1_name = track1['name']
                track1_artist = track1['artists'][0]['name']
                cover_image_url1 = track1['album']['images'][0]['url']
                preview_audio1 = track1['preview_url']
                track1_url = track1["external_urls"]["spotify"]
                track1_id = track1["id"]

                track2_name = track2['name']
                track2_artist = track2['artists'][0]['name']
                cover_image_url2 = track2['album']['images'][0]['url']
                preview_audio2 = track2['preview_url']
                track2_url = track2["external_urls"]["spotify"]
                track2_id = track2["id"]

                track3_name = track3['name']
                track3_artist = track3['artists'][0]['name']
                cover_image_url3 = track3['album']['images'][0]['url']
                preview_audio3 = track3['preview_url']
                track3_url = track3["external_urls"]["spotify"]
                track3_id = track3["id"]

                track4_name = track4['name']
                track4_artist = track4['artists'][0]['name']
                cover_image_url4 = track4['album']['images'][0]['url']
                preview_audio4 = track4['preview_url']
                track4_url = track4["external_urls"]["spotify"]
                track4_id = track4["id"]

                play_button = "play/pause"
                song_found = "These are the top 4 songs found"


                return render_template("post.html", user=current_user, song_found=song_found, play_button=play_button,
                                       track1_name=track1_name, track1_artist=track1_artist,
                                       cover_image_url1=cover_image_url1, preview_audio1=preview_audio1, track1_url=track1_url, track1_id=track1_id,
                                       track2_name=track2_name, track2_artist=track2_artist,
                                       cover_image_url2=cover_image_url2, preview_audio2=preview_audio2, track2_url=track2_url, track2_id=track2_id,
                                       track3_name=track3_name, track3_artist=track3_artist,
                                       cover_image_url3=cover_image_url3, preview_audio3=preview_audio3, track3_url=track3_url, track3_id=track3_id,
                                       track4_name=track4_name, track4_artist=track4_artist,
                                       cover_image_url4=cover_image_url4, preview_audio4=preview_audio4,
                                       track4_url=track4_url, track4_id=track4_id,
                                       )

            except IndexError:
                song_found = "No song found"
                return render_template("post.html", user=current_user, song_found=song_found)

        elif request.form['submit_button'] == 'Post 1':
            song_name = track1_name
            song_artist = track1_artist
            song_link = track1_url
            audio_link = preview_audio1
            album_cover = cover_image_url1
            user_id = current_user.id
            username = main_username
            profile_pic = profile_picture

            return render_template("confirm_post.html", user=current_user, song_name=song_name, song_artist=song_artist, album_cover=album_cover)

        elif request.form['submit_button'] == 'Post 2':
            song_name = track2_name
            song_artist = track2_artist
            song_link = track2_url
            audio_link = preview_audio2
            album_cover = cover_image_url2
            user_id = current_user.id
            username = main_username
            profile_pic = profile_picture

            return render_template("confirm_post.html", user=current_user, song_name=song_name, song_artist=song_artist,
                                   album_cover=album_cover)

        elif request.form['submit_button'] == 'Post 3':
            song_name = track3_name
            song_artist = track3_artist
            song_link = track3_url
            audio_link = preview_audio3
            album_cover = cover_image_url3
            user_id = current_user.id
            username = main_username
            profile_pic = profile_picture

            return render_template("confirm_post.html", user=current_user, song_name=song_name, song_artist=song_artist,
                                   album_cover=album_cover)

        elif request.form['submit_button'] == 'Post 4':
            song_name = track4_name
            song_artist = track4_artist
            song_link = track4_url
            audio_link = preview_audio4
            album_cover = cover_image_url4
            user_id = current_user.id
            username = main_username
            profile_pic = profile_picture

            return render_template("confirm_post.html", user=current_user, song_name=song_name, song_artist=song_artist,
                                   album_cover=album_cover)

    else:
        import requests
        import json

        # Define playlist ID
        playlist_id = "37i9dQZEVXbJiyhoAPEfMK"

        # Get the access token
        auth_response = requests.post("https://accounts.spotify.com/api/token", data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        })

        # Check the accepted code of the response
        if auth_response.status_code == 200:
            # Get the access token from the JSON album_cover
            auth_data = json.loads(auth_response.text)
            access_token = auth_data["access_token"]

            # Define the endpoint URL
            endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

            # Set the authorization header
            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            # Make the GET request to the Spotify Web API
            response = requests.get(endpoint, headers=headers)

            # Check the accepted code of the response
            if response.status_code == 200:
                # Get the JSON album_cover from the response
                data = json.loads(response.text)

                # Get the first 4 songs from the list of items
                track1_id = data["items"][0]["track"]["id"]
                track2_id = data["items"][1]["track"]["id"]
                track3_id = data["items"][2]["track"]["id"]
                track4_id = data["items"][3]["track"]["id"]

                return render_template("post.html", user=current_user, track1_id=track1_id, track2_id=track2_id, track3_id=track3_id, track4_id=track4_id)
        else:
            song_found = "Song could not be found with Spotify"
            return render_template("post.html", user=current_user, song_found=song_found)
    return render_template("post.html", user=current_user)


@views.route('/confirm-post', methods=['POST'])
def confirm_post():

    global song_name
    global song_artist
    global song_link
    global audio_link
    global album_cover

    caption = request.form['text_input']

    if song_name == track1_name:
        new_post = Post(song_name=track1_name, song_artist=track1_artist, song_link=track1_url,
                        audio_link=preview_audio1, album_cover=cover_image_url1, user_id=current_user.id,
                        username=main_username, caption=caption, likes=0)
        flash('POSTED', category='success')

        db.session.add(new_post)
        db.session.commit( )

    elif song_name == track2_name:
        new_post = Post(song_name=track2_name, song_artist=track2_artist, song_link=track2_url,
                        audio_link=preview_audio2, album_cover=cover_image_url2, user_id=current_user.id,
                        username=main_username, caption=caption, likes=0)
        flash('POSTED', category='success')

        db.session.add(new_post)
        db.session.commit( )

    elif song_name == track3_name:
        new_post = Post(song_name=track3_name, song_artist=track3_artist, song_link=track3_url,
                        audio_link=preview_audio3, album_cover=cover_image_url3, user_id=current_user.id,
                        username=main_username, caption=caption, likes=0)
        flash('POSTED', category='success')

        db.session.add(new_post)
        db.session.commit( )

    elif song_name == track4_name:
        new_post = Post(song_name=track4_name, song_artist=track4_artist, song_link=track4_url,
                        audio_link=preview_audio4, album_cover=cover_image_url4, user_id=current_user.id,
                        username=main_username, caption=caption, likes=0)
        flash('POSTED', category='success')

        db.session.add(new_post)
        db.session.commit( )

    return render_template("home.html", user=current_user, main_username=main_username)


@views.route('/delete-post', methods=['POST'])
def delete_post():
    post = json.loads(request.data)
    postId= post['postId']
    post =Post.query.get(postId)
    if post:
        if post.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit()
    return jsonify({})



global you_follow
global users_picture
global users_bio
global users_posts
global users_personal




@views.route('/profile_searched', methods=['GET','POST'])
@login_required
def profile_searched():
    already_follow = 0
    global searched_account
    global num_of_posts
    global all_post_names
    global all_post_artists
    global all_post_covers
    global you_follow
    global users_picture
    global users_bio
    global users_posts
    global users_personal

    if request.method == 'POST':
        if request.form['submit_button'] == 'search':
            person_searched = request.form.get('search_account')
            searched_account=person_searched
            usersearched = User.query.filter_by(username=person_searched).first()
            if usersearched:
                username_searched=usersearched.username
                flash('successful', category='success')

                # Retrieve all rows from the User table where the name is...
                users_personal = User.query.filter_by(username=searched_account).first( )
                users_posts = Post.query.filter_by(username=searched_account).all( )

                # Iterate through the retrieved rows and print their names and profile pic
                users_picture = users_personal.profile_pic
                users_bio = users_personal.bio

                num_of_posts = 0
                for post in users_posts:
                    if post.likes > 0:
                        latest_liker = Like.query.filter_by(liked_post_name=post.song_name).order_by(
                            Like.date.desc()).first()
                        if latest_liker:
                            post.latest_liker = latest_liker.username_liker

                        other_likers = Like.query.filter_by(liked_post_name=post.song_name).count()
                        post.other_likers = other_likers - 1 if other_likers > 1 else 0
                    num_of_posts += 1

                do_you_follow_them = Follow.query.filter_by(username_followed=searched_account, accepted=1).all( )
                you_follow = 0
                if do_you_follow_them:
                    for user in do_you_follow_them:
                        if user.username_follower == main_username:
                            you_follow = 1
                            break
                        else:
                            continue

                return render_template("profile_searched.html", user=current_user, you_follow=you_follow,searched_account=searched_account,
                                       profile_pic=users_picture, profile_bio=users_bio,
                                       num_of_posts=num_of_posts, users_posts=users_posts, users_personal=users_personal)
            else:
                flash('not a real user', category='error')

        elif request.form['submit_button'] == 'follow':

            users_that_I_follow = Follow.query.filter_by(username_follower=main_username).all( )

            if users_that_I_follow:
                for post in users_that_I_follow:
                    if post.username_followed == searched_account:
                        already_follow = 1
                        break
                    else:
                        continue

            if already_follow == 0:
                flash('you have requested to follow this user', category='success')
                follow_the_user = Follow(username_followed=searched_account,
                                         username_follower=main_username, accepted=0)

                db.session.add(follow_the_user)
                db.session.commit( )
                db.session.commit( )
            else:
                flash('you already follow this user', category='error')


            return render_template("profile_searched.html",  user=current_user, you_follow=you_follow,
                                   searched_account=searched_account,
                                   profile_pic=users_picture, profile_bio=users_bio,
                                   num_of_posts=num_of_posts, users_posts=users_posts, users_personal=users_personal)

        elif request.form['submit_button'] == 'unfollow':

            users_that_I_follow = Follow.query.filter_by(username_follower=main_username, username_followed = searched_account).first( )

            if users_that_I_follow:
                db.session.delete(users_that_I_follow)
                db.session.commit( )
                flash('you have unfollowed this user', category='success')
            else:
                flash('you do not follow this user, you cannot unfollow', category='error')

            return render_template("profile_searched.html", user=current_user, searched_account=searched_account,
                                   profile_pic=profile_picture,
                                   num_of_posts=num_of_posts)

        return render_template("profile_searched.html", user=current_user, you_follow=0,
                                   searched_account=searched_account,
                                   profile_pic=users_picture, profile_bio=users_bio,
                                   num_of_posts=num_of_posts, users_posts=users_posts, users_personal=users_personal)


    return render_template("home.html", user=current_user)


@views.route('/submit_comment', methods=['POST'])
def submit_comment():
    if request.method == 'POST':
        post_id = request.json.get('post_id')
        comment_text = request.json.get('comment_text')

        # You can add validation and other checks here before saving the comment

        # Create a new Comment instance and save it to the database
        new_comment = Comment(post_id=post_id, comment_text=comment_text)
        db.session.add(new_comment)
        db.session.commit()

        # Return a success message or any relevant data if needed
        return jsonify({'message': 'Comment submitted successfully'})


# Route to fetch comments for a specific post
@views.route('/get_comments/<int:post_id>')
def get_comments(post_id):
    post_comments = Comment.query.filter_by(post_id=post_id).all()
    comments = [{'comment_text': comment.comment_text} for comment in post_comments]
    return jsonify({'comments': comments})


@views.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    post = Post.query.get(post_id)
    liked_by_user = False

    if post:
        user = current_user  # Assuming you are using Flask-Login to get the current user
        like = Like.query.filter_by(username_liker=user.username, post_id=post_id).first()

        if like:
            db.session.delete(like)
        else:
            liked_by_user = True
            like = Like(username_liker=user.username, username_liked=post.username, liked_post_name=post.song_name, user_id=user.id, post_id=post_id)
            db.session.add(like)

        post.likes = len(post.likes_rel)
        db.session.commit()

    return jsonify({'likes': post.likes, 'liked_by_user': liked_by_user})

@views.route('/', methods=['GET','POST'])
@login_required
def feed():
    follow_requests = Follow.query.filter_by(username_followed=main_username, accepted=0).all( )
    data = []
    for requests in follow_requests:
        user = User.query.filter_by(username=requests.username_follower).first( )
        if user:
            data.append({
                'username_follower': requests.username_follower,
                'profile_pic': user.profile_pic
            })

    if request.method == "POST":
        for follower in follow_requests:
            decision = request.form.get('follower_username')
            action = request.form.get('action')
            if action == "accept":
                add_followers_to_me = User.query.filter_by(username=main_username).first( )
                add_followers_to_me.followers = add_followers_to_me.followers + 1

                add_following_to_user = User.query.filter_by(username=decision).first( )
                add_following_to_user.following = add_following_to_user.following + 1

                accept_follow = Follow.query.filter_by(username_follower=decision, username_followed=main_username).first( )
                accept_follow.accepted = accept_follow.accepted + 1

                db.session.commit( )

                flash('You have accepted the follow request', category='success')
                return render_template("home.html", user=current_user)

            else:
                follower.accepted = False
                delete_request = Follow.query.filter_by(username_followed=main_username,
                                                        username_follower=follower.username_follower).first( )
                db.session.delete(delete_request)
                flash('you have decline the follow request', category='error')

        db.session.commit( )

    return render_template("home.html", data=data, user=current_user,main_username=main_username, profile_pic=profile_picture)


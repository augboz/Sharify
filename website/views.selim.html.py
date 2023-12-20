from flask import Blueprint, render_template, flash,jsonify,request, redirect, url_for
from .models import Post, User
from . import db
import json
import os
import spotipy
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth',__name__)
import sqlite3
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

@views.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method =='POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user=User.query.filter_by(email=email).first()
        if user:
            flash('email already exist', category='error')
        elif len(email) <4:
            flash('email must be greated 4 char',category='error')
        elif len(username) <2:
            flash('name must be greated 2 char',category='error')
        elif len(password1) <1:
            flash('password must be longer then 1 char', category="error")
        elif password1 != password2:
            flash('password dont match', category='error')

        else:
            new_user =User(email=email, username = username, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("account created", category='success')
            login_user(new_user, remember=True)
            global main_username
            main_username = username
            return redirect(url_for('views.post'))
    return render_template("sign_up.html", user=current_user,main_username=main_username)


@views.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        password= request.form.get('password')
        user=User.query.filter_by(email=email).first()
        global main_username
        main_username=user.username
        if user:
            if check_password_hash(user.password, password):
                flash('logged in',  category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.feed'))

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





global profilePic




@views.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    global main_username
    global profilePic
    # Retrieve all rows from the User table where the name is...
    profilePic = User.query.filter_by(username=main_username).first( )

    # Iterate through the retrieved rows and print their names and emails
    for user in profilePic:
        profile_pic = user.profile_pic

    return render_template("profile.html", user=current_user, main_username=main_username, profile_pic=profile_pic )



global track1_name
global track2_name
global track3_name
global track4_name
@views.route("/post", methods=['GET', 'POST'])
@login_required
def post():
    global search
    global track1_name
    global track2_name
    global track3_name
    global track4_name
    global main_username
    if request.method == 'POST':

        if request.form['submit_button'] == 'Button 5':
            try:
                track_name = request.form.get('song_name')

                # Search for a track by its name and artist
                results = sp.search(q=f'track:{track_name}', type='track')

                # Get the first track from the search results
                track1 = results['tracks']['items'][0]
                track2 = results['tracks']['items'][1]
                track3 = results['tracks']['items'][2]
                track4 = results['tracks']['items'][3]

                track1_name = "1: " + track1['name']
                track1_artist = track1['artists'][0]['name']
                cover_image_url1 = track1['album']['images'][0]['url']
                preview_audio1 = track1['preview_url']
                track1_url = track1["external_urls"]["spotify"]
                track1_id = track1["id"]

                track2_name = "2: " + track2['name']
                track2_artist = track2['artists'][0]['name']
                cover_image_url2 = track2['album']['images'][0]['url']
                preview_audio2 = track2['preview_url']
                track2_url = track2["external_urls"]["spotify"]
                track2_id = track2["id"]

                track3_name = "3: " + track3['name']
                track3_artist = track3['artists'][0]['name']
                cover_image_url3 = track3['album']['images'][0]['url']
                preview_audio3 = track3['preview_url']
                track3_url = track3["external_urls"]["spotify"]
                track3_id = track3["id"]

                track4_name = "4: " + track4['name']
                track4_artist = track4['artists'][0]['name']
                cover_image_url4 = track4['album']['images'][0]['url']
                preview_audio4 = track4['preview_url']
                track4_url = track4["external_urls"]["spotify"]
                track4_id = track4["id"]

                play_button = "play/pause"
                song_found = "These are the top 4 songs found"


                """
                new_post = Post(data=track_name, user_id=current_user.id)
                db.session.add(new_post)
                db.session.commit()
                flash('Post added!', category='success')
                """
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

        elif request.form['submit_button'] == 'Button 1':
             print("button 1")
             print(track1_name)
             new_post = Post(song_name=track1_name, user_id=current_user.id, username=main_username)
             db.session.add(new_post)
             db.session.commit()
             flash('POSTED', category='success')
             return render_template("home.html", user=current_user)

        elif request.form['submit_button'] == 'Button 2':
            print("button 2")
            new_post = Post(song_name=track2_name, user_id=current_user.id, username=main_username)
            db.session.add(new_post)
            db.session.commit()
            flash('POSTED', category='success')
            return render_template("home.html", user=current_user)


        elif request.form['submit_button'] == 'Button 3':
            print("button 3")
            new_post = Post(song_name=track3_name, user_id=current_user.id, username=main_username)
            db.session.add(new_post)
            db.session.commit()
            flash('POSTED', category='success')
            return render_template("home.html", user=current_user)

        elif request.form['submit_button'] == 'Button 4':
            print("button 4")
            new_post = Post(song_name=track4_name, user_id=current_user.id, username=main_username)
            db.session.add(new_post)
            db.session.commit()
            flash('POSTED', category='success')
            return render_template("home.html", user=current_user)
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
            # Get the access token from the JSON data
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
                # Get the JSON data from the response
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



global searched_account

@views.route('/', methods=['GET','POST'])
def feed():
    global searched_account

    if request.method == 'POST':
        if request.form['submit_button'] == 'search':
            person_searched = request.form.get('search_account')
            searched_account=person_searched
            usersearched = User.query.filter_by(username=person_searched).first()
            if usersearched:
                username_searched=usersearched.username
                print(username_searched)
                flash('successful', category='success')
                return render_template("profile_searched.html", user=current_user, searched_account=searched_account)

            else:
                print("not a real user")
                flash('not a real user', category='error')

    return render_template("home.html", user=current_user)


@views.route('/profile_searched', methods=['GET','POST'])
def profile_searched():
    global searched_account


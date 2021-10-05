from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import facebook
from django.contrib.auth.models import User

from .models import FbPosts, FbObject, Post


def login(request):
    return render(request, 'login.html')


@login_required
def home(request):
    # user who logged in
    user = request.user
    # getting all the logged in user details that facebook shared
    social = user.social_auth.get(provider='facebook')
    # getting logged in users access token
    token = social.extra_data['access_token']
    # calling facebook graphapi using access token and user uid to get all the user feeds
    graph = facebook.GraphAPI(access_token=token, version=2.12)
    events = graph.get_object(id=social.uid, fields='feed')
    # retriving all the postid's from the response and storing it in postidList
    feed = events['feed']
    eventList = feed['data']
    postidList = []
    for event in eventList:
        postidList.append(event['id'])
    # calling facebook graph api with postidList to get post details which include attachments and created time
    posts = graph.get_objects(
        ids=postidList, fields='attachments,created_time')

    # looping through the postsData to get the required fields that is postid,postDescription
    # postImage and created_at and save it into db
    postList = []
    for postid in postidList:
        postDetails = posts.get(postid)
        attachment = postDetails.get('attachments')
        if attachment:
            postData = attachment.get('data')[0]
            postImage = ''
            if postData.get('media'):
                postImage = postData['media']['image']['src']
            postList.append(postData)
            if not FbPosts.objects.filter(postId=postid).exists():
                fbPost = FbPosts.objects.create(
                    postId=postid,
                    userName=User.username,
                    userId=social.uid,
                    postDescription=postData.get('description'),
                    postImage=postImage,
                    created_at=postDetails['created_time']
                )

    # retriving all the saved posts from db
    remoteFbPosts = FbPosts.objects.all()
    # saving all the retrived posts into cloud mongo db
    for remoteFbPost in remoteFbPosts:
        if not FbObject.objects.using('mongo').filter(userId=remoteFbPost.userId).exists():
            # create new record for each post
            postN = Post.objects.using('mongo').create(
                postId=remoteFbPost.postId,
                postDescription=remoteFbPost.postDescription,
                postImage=remoteFbPost.postImage,
                created_at=remoteFbPost.created_at
            )
            # create new record for new user
            # here one fbObject has many post implementing one to many mapping
            FbObject.objects.using('mongo').create(
                userName=remoteFbPost.userName,
                userId=remoteFbPost.userId,
                posts=[postN]
            )
        else:
            # fetching the fbObject if it already exists
            fbObject = FbObject.objects.using(
                'mongo').get(userId=remoteFbPost.userId)
            # adding new posts to existing fbObject
            fbObject.posts.append(Post(
                postId=remoteFbPost.postId,
                postDescription=remoteFbPost.postDescription,
                postImage=remoteFbPost.postImage,
                created_at=remoteFbPost.created_at
            ))
            fbObject.save(using='mongo')
    # rendering the home page
    return render(request, 'home.html', {'posts': postList})

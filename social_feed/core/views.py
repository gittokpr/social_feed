from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import facebook
from django.contrib.auth.models import User

from .models import FbPosts, FbObject, Post


def login(request):
    return render(request, 'login.html')


@login_required
def home(request):

    user = request.user
    social = user.social_auth.get(provider='facebook')
    token = social.extra_data['access_token']
    graph = facebook.GraphAPI(access_token=token, version=2.12)
    events = graph.get_object(id=social.uid, fields='feed')
    feed = events['feed']
    eventList = feed['data']
    postidList = []
    for event in eventList:
        postidList.append(event['id'])
    print(postidList)

    posts = graph.get_objects(
        ids=postidList, fields='attachments,created_time')
    # print(posts)

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
        # print(attachment.get('data'))
        # postList.append(attachment['data'][0])
    remoteFbPosts = FbPosts.objects.all()
    print(remoteFbPosts)
    for remoteFbPost in remoteFbPosts:
        print(remoteFbPost.userId)
        if not FbObject.objects.using('mongo').filter(userId=remoteFbPost.userId).exists():
            print("inside if")
            pList = []
            postN = Post.objects.using('mongo').create(
                postDescription=remoteFbPost.postDescription,
                postImage=remoteFbPost.postImage,
                created_at=remoteFbPost.created_at
            )
            pList.append(postN)
            FbObject.objects.using('mongo').create(
                userName=remoteFbPost.userName,
                userId=remoteFbPost.userId,
                posts=pList
            )
            '''fbobj.userName(remoteFbPost.userName)
            fbobj.userId(remoteFbPost.userId)
            fbobj.posts(pList)
            fbobj.save(using='mongo')'''
        else:
            print("inside else")
            fbObject = FbObject.objects.using(
                'mongo').get(userId=remoteFbPost.userId)
            fbObject.posts.add(Post(
                postDescription=remoteFbPost.postDescription,
                postImage=remoteFbPost.postImage,
                created_at=remoteFbPost.created_at
            ))
            fbObject.save(using='mongo')

    return render(request, 'home.html', {'posts': postList})

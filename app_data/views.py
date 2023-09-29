from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .forms import registerform, uploadform, profileform, loginform
from django.shortcuts import redirect,render, get_object_or_404 
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import registration, login_user, upload
from django.contrib.auth.models import User
from django.db.models import Subquery
from django.db import connection
from django.db.models import QuerySet
import cv2
import os
import datetime
from werkzeug.utils import secure_filename
from random import shuffle




merge="""select app_data_registration.id, app_data_registration.name, app_data_registration.profile, app_data_upload.title, app_data_upload.description, app_data_upload.url, app_data_upload.image, app_data_upload.video_in 
         from app_data_registration
         inner join app_data_upload on app_data_registration.id=app_data_upload.uid   """
with connection.cursor() as cursor:
    cursor.execute(merge)

    results = cursor.fetchall()
    # print(results)

data = [{'id': row[0], 'name': row[1], 'profile': row[2], 'title': row[3], 'description': row[4], 'url': row[5], 'image': row[6], 'video_in': row[7]} for row in results]
shuffle(data)
queryset = QuerySet(model=upload, query=upload.objects.all().query, using=upload.objects.db)
queryset._result_cache = data  

def home(request):
    temp=loader.get_template('layout/home.html')
    # videos= upload.objects.values_list('url', flat=True)
    # videos=upload.objects.all()
    # print('hi hello...........', videos)
    return HttpResponse(temp.render({'video': queryset}, request))

@csrf_exempt
def reg(request):
    if request.method=='POST':
        form=registerform(request.POST)
        if form.is_valid():
            form.save()
            gmail=request.POST.get('gmail')
            user=registration.objects.get(gmail=gmail)
            my_object = login_user.objects.get(id=1)
            my_object.uid = user.id
            my_object.user_mail = gmail
            my_object.save()
            log=login_user.objects.get(id=1)
            users = registration.objects.get(gmail=log.user_mail)    
            data = [{'id': row[0], 'name': row[1], 'profile': row[2], 'title': row[3], 'description': row[4], 'url': row[5], 'image': row[6], 'video_in': row[7]} for row in results]

            filtered_queryset = [item for item in data if item['id'] != users.id]
            shuffle(filtered_queryset)
            queryset = QuerySet(model=upload, query=upload.objects.all().query, using=upload.objects.db)
            queryset._result_cache = filtered_queryset 
            form={
                'video': queryset,
                'users': users,
                'message': 'Register Successfully'
            }        
            temp=loader.get_template('layout/home.html')
            return HttpResponse(temp.render(form,request))
        form=registerform()
        form={'form': form}
        temp=loader.get_template('layout/reg.html')
        return HttpResponse(temp.render(form,request))
    form=registerform()
    form={'form': form}
    temp=loader.get_template('layout/reg.html')
    return HttpResponse(temp.render(form,request))


@csrf_exempt
def login_page(request):
    # user = registration.objects.get(gmail="kumarbala9090@gmail.com",password=1234)
    # return render(request, 'layout/login.html', {'form': user.password})
    if request.method == 'POST':
        gmail = request.POST.get('gmail')
        password = request.POST.get('password')
        try:
            user = registration.objects.get(gmail=gmail,password=password)
            print(user)
        except:
            user=None
            pass    

        if user is not None:
            my_object = login_user.objects.get(id=1)
            my_object.uid = user.id
            my_object.user_mail = gmail
            my_object.save()
            # videos= upload.objects.values_list('url', flat=True)
            # excluded_values = upload.objects.filter(uid=2)
            videos=upload.objects.exclude(uid=user.id)
            merge="""select app_data_registration.id, app_data_registration.name, app_data_registration.profile, app_data_upload.title, app_data_upload.description, app_data_upload.url, app_data_upload.image, app_data_upload.video_in 
         from app_data_registration
         inner join app_data_upload on app_data_registration.id=app_data_upload.uid   """
            with connection.cursor() as cursor:
                cursor.execute(merge)

                results = cursor.fetchall()
                # print(results)

            data = [{'id': row[0], 'name': row[1], 'profile': row[2], 'title': row[3], 'description': row[4], 'url': row[5], 'image': row[6], 'video_in': row[7]} for row in results]
            # print(data, users.id)

            filtered_queryset = [item for item in data if item['id'] != user.id]
            shuffle(filtered_queryset)
            queryset = QuerySet(model=upload, query=upload.objects.all().query, using=upload.objects.db)
            queryset._result_cache = filtered_queryset  
            # print('hello the.........',videos)
            return render(request,'layout/home.html', {'users': user, 'video': queryset, 'message': 'Login Successfully'})
        else:
            return redirect('/log')
    else:
        form=loginform()
        return render(request, 'layout/login.html', {'form': form})

def login_home(request):
    user=login_user.objects.get(id=1)
    users = registration.objects.get(gmail=user.user_mail)
    videos= upload.objects.exclude(uid=user.id)
    merge="""select app_data_registration.id, app_data_registration.name, app_data_registration.profile, app_data_upload.title, app_data_upload.description, app_data_upload.url, app_data_upload.image, app_data_upload.video_in 
         from app_data_registration
         inner join app_data_upload on app_data_registration.id=app_data_upload.uid   """
    with connection.cursor() as cursor:
        cursor.execute(merge)

        results = cursor.fetchall()
        # print(results)

    data = [{'id': row[0], 'name': row[1], 'profile': row[2], 'title': row[3], 'description': row[4], 'url': row[5], 'image': row[6], 'video_in': row[7]} for row in results]
    # print(data, users.id)

    filtered_queryset = [item for item in data if item['id'] != users.id]
    shuffle(filtered_queryset)
    queryset = QuerySet(model=upload, query=upload.objects.all().query, using=upload.objects.db)
    queryset._result_cache = filtered_queryset  
    # print('hello the.........',videos)
    
    return render(request, 'layout/home.html', {'users': users, 'video': queryset})

@csrf_exempt
def uploads(request):
    # form=uploadform(request.POST)
    user=login_user.objects.get(id=1)
    users = registration.objects.get(gmail=user.user_mail)
    if request.method == 'POST':  
        form = uploadform(request.POST, request.FILES)  
        if form.is_valid():  
            form.save()  
            url=request.POST.get('url')
            print(url)
            log_user_id=upload.objects.get(url=url)
            log_user_id.uid=users.id
            log_user_id.save()

            filtered_queryset = [item for item in data if item['id'] != users.id]
            queryset = QuerySet(model=upload, query=upload.objects.all().query, using=upload.objects.db)
            queryset._result_cache = filtered_queryset
        return render(request, 'layout/home.html', {'users': users, 'video': queryset, 'message': 'Video uploaded successfull'})
        

        
    form=uploadform()
    return render(request, 'layout/video_upload.html', {'form':form, 'users': users})


from django.db import models
@csrf_exempt
def video_play(request):
    try:    
        user=login_user.objects.get(id=1)
        users=registration.objects.get(gmail=user.user_mail)
        value = request.GET.get('value')
        values=upload.objects.filter(image=value)
        for i in values:
            a=i.uid
        
        user_id=registration.objects.filter(id=a)
        videos= upload.objects.exclude(image=value)
        id= upload.objects.exclude(uid=users.id)
        # videos= upload.objects.exclude()
        # print(videos)
        # print(id)
        merge="""select app_data_registration.id, app_data_registration.name, app_data_registration.profile, app_data_upload.title, app_data_upload.description, app_data_upload.url, app_data_upload.image 
            from app_data_registration
            inner join app_data_upload on app_data_registration.id=app_data_upload.uid   """
        with connection.cursor() as cursor:
            cursor.execute(merge)

            results = cursor.fetchall()

        excluded_images = videos.values_list('image', flat=True)
        excluded_id = id.values_list('uid', flat=True)
        # print(excluded_id)
        # print(excluded_images)
        data = [{'id': row[0], 'name': row[1], 'profile': row[2], 'title': row[3], 'description': row[4], 'url': row[5], 'image': row[6]} for row in results]

        filtered_queryset = [item for item in data if item['image'] in excluded_images and item['id'] in excluded_id]
        # print(filtered_queryset)
        queryset = QuerySet(model=upload, query=upload.objects.all().query, using=upload.objects.db)
        queryset._result_cache = filtered_queryset
        
    except Exception as e:
        print(e)
        users=None   
        value = request.GET.get('value')
        values=upload.objects.filter(image=value)
        for i in values:
            a=i.uid
        
        user_id=registration.objects.filter(id=a)
        # print(videos)
        merge="""select app_data_registration.id, app_data_registration.name, app_data_registration.profile, app_data_upload.title, app_data_upload.description, app_data_upload.url, app_data_upload.image 
            from app_data_registration
            inner join app_data_upload on app_data_registration.id=app_data_upload.uid   """
        with connection.cursor() as cursor:
            cursor.execute(merge)

            results = cursor.fetchall()

        data = [{'id': row[0], 'name': row[1], 'profile': row[2], 'title': row[3], 'description': row[4], 'url': row[5], 'image': row[6]} for row in results]


        filtered_queryset = [item for item in data if item['image'] != value]

        queryset = QuerySet(model=upload, query=upload.objects.all().query, using=upload.objects.db)
        queryset._result_cache = filtered_queryset
    
    # print(queryset)
    return render(request, 'layout/video.html', {'value': values, 'video_user': user_id, 'other': queryset, 'users': users})

def user_video(request):
    log=login_user.objects.get(id=1)
    users = registration.objects.get(gmail=log.user_mail)
    videos= upload.objects.filter(uid=log.uid)
    print(videos)

    merge="""select app_data_registration.id, app_data_registration.name, app_data_registration.profile, app_data_upload.title, app_data_upload.description, app_data_upload.url, app_data_upload.image, app_data_upload.video_in 
         from app_data_registration
         inner join app_data_upload on app_data_registration.id=app_data_upload.uid   """
    with connection.cursor() as cursor:
        cursor.execute(merge)

        results = cursor.fetchall()
        # print(results)

    data = [{'id': row[0], 'name': row[1], 'profile': row[2], 'title': row[3], 'description': row[4], 'url': row[5], 'image': row[6], 'video_in': row[7]} for row in results]

    filtered_queryset = [item for item in data if item['id'] == users.id]

    queryset = QuerySet(model=upload, query=upload.objects.all().query, using=upload.objects.db)
    queryset._result_cache = filtered_queryset   

    return render(request, 'layout/user-video.html', {'video': queryset, 'users': users})

@csrf_exempt
def profile(request):
    form=profileform()
    user=login_user.objects.get(id=1)
    users = registration.objects.get(gmail=user.user_mail)
    print(users.id)
    # for i in users:
    #     profile=i.profile
    #     users=i.name
    # print(profile)    
    if request.method == 'POST':
        try:
            file=request.FILES.get('profile')
            # print(file) 
            files=file.name
            # print(files)
            basepath = os.path.dirname(__file__)
            basepath = os.path.dirname(basepath)
            now_time=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            # print(now_time)
            new_filename="%s%s"%(now_time,files)
            
            with open(basepath +'/static/assets/media/'+new_filename, 'wb') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
            # print(x[-1])
            # delt=users.profile
            if users.profile != 'static/assets/media/default-avatar.jpg':
                del_path=basepath+'/'+str(users.profile)    
                os.remove(del_path)  
            send= 'static/assets/media/'+new_filename
            registration.objects.filter(id=users.id).update(profile=send)
        except Exception as e:
            print(e)    

        try:
            name=request.POST.get('name')
            use=registration.objects.get(id=users.id)
            use.name=name
            use.save()
        except Exception as e:
            print(e)    

        return render(request, 'layout/home.html', {"form": form, 'users': users, 'profile': users, 'video': queryset,
                                                         "message": 'Your Profile Update Successfully'})

    form=profileform()
   
    return render(request, 'layout/user_profile.html', {"form": form, 'users': users, 'profile': users})

x=[]
thumbs=[]
@csrf_exempt
def v_e(request):
    log=login_user.objects.get(id=1)
    users = registration.objects.get(gmail=log.user_mail)
    try:
        thumb=request.GET.get('thumb')
        thumbs.append(thumb)
        update= upload.objects.filter(image=thumb)
        # print(update)
        update_detail= upload.objects.get(image=thumb) 
        x.append(update_detail.image)
    except:
        # print('hello',thumbs[0])
        updates= upload.objects.filter(image=thumbs[0])
        pass
    
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            upload.objects.filter(image=x[-1]).update(title=title)
        except:
            pass 

        try:
            desc = request.POST.get('des')
            upload.objects.filter(image=x[-1]).update(description=desc)
        except:
            pass

        try:
            file=request.FILES.get('profile')
            # print(file) 
            files=file.name
            # print(files)
            basepath = os.path.dirname(__file__)
            basepath = os.path.dirname(basepath)
            # print(basepath)
            # file_path = os.path.join(basepath, 'static/assets/media', secure_filename(file.name))
            # file.save(file_path)   
            now_time=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            # print(now_time)
            new_filename="%s%s"%(now_time,files)
            
            with open(basepath +'/static/assets/upload/'+new_filename, 'wb') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
            # print(x[-1])
            delt=x[-1]
            del_path=basepath+'/'+str(delt)    
            os.remove(del_path)  
            send= 'static/assets/upload/'+new_filename
            upload.objects.filter(image=x[-1]).update(image=send)       
            
        except Exception as e:
            print(e)
            pass    

        try:
            vid = request.POST.get('vid')
            upload.objects.filter(image=x[-1]).update(video_in=vid)
        except:
            pass

        try:
            tag = request.POST.get('tag')
            upload.objects.filter(image=x[-1]).update(tags=tag)
        except:
            pass 
          
        return render(request, 'layout/edit.html', {'users': users, 'update': updates, 'message': ' Saved '})
    return render(request, 'layout/edit.html', {'users': users, 'update': update})



def delete(request):
    log=login_user.objects.get(id=1)
    users = registration.objects.get(gmail=log.user_mail)
    try:
        vid=request.GET.get('thumb')
        use=upload.objects.get(image=vid)
        use.delete()
    except:
        pass    
    return render(request, 'layout/user-video.html', {'users': users, 'message': 'Video Deleted'})


def out(request):
    delt=login_user.objects.filter(id=1)
    delt.update(uid=None, user_mail=None)
    return render(request, 'layout/home.html', {'video': queryset, 'message': 'Sign Out'})

@csrf_exempt
def search(request):
    try:
        login=login_user.objects.get(id=1)
        users=registration.objects.get(gmail=login.user_mail)
    except:
        users=''    
    cat=request.POST.get('search')
    search_content = cat.split()
    print(search_content)
    merge="""select app_data_upload.id, app_data_registration.name, app_data_registration.profile, app_data_upload.title, app_data_upload.description, app_data_upload.url, app_data_upload.image, app_data_upload.tags 
         from app_data_registration
         inner join app_data_upload on app_data_registration.id=app_data_upload.uid   """
    with connection.cursor() as cursor:
        cursor.execute(merge)

        results = cursor.fetchall()
        # print(results)

    data = [{'id': row[0], 'name': row[1], 'profile': row[2], 'title': row[3], 'description': row[4], 'url': row[5], 'image': row[6], 'tags': row[7]} for row in results]

    filtered_queryset = [row for row in data if any(word in row['tags'] or word in row['title'] for word in search_content)]

    queryset = QuerySet(model=upload, query=upload.objects.all().query, using=upload.objects.db)
    queryset._result_cache = filtered_queryset 
    return render(request, 'layout/home.html', {'video': queryset, 'users': users})

def category(request):
    cat=request.GET.get('category')
    try:
        log=login_user.objects.get(id=1)
        users = registration.objects.get(gmail=log.user_mail)
        print(cat)
        if cat=='gaming':
            datas=upload.objects.filter(category='gaming')
            
        elif cat=='education':
            datas=upload.objects.filter(category='education')
            
        elif cat=='music':
            datas=upload.objects.filter(category='music')

        elif cat=='sports':
            datas=upload.objects.filter(category='sports')

        print(datas)
        for i in datas:
            print(i.uid)
        filtered_queryset = [item for item in data if item['id'] in datas.values_list('uid', flat=True)]

        queryset = QuerySet(model=upload, query=upload.objects.all().query, using=upload.objects.db)
        queryset._result_cache = filtered_queryset 
        print(queryset)    
        return render(request, 'layout/home.html', {'video': queryset, 'users': users})
    except:
        print(cat)
        if cat=='gaming':
            datas=upload.objects.filter(category='gaming')
            
        elif cat=='education':
            datas=upload.objects.filter(category='education')
            
        elif cat=='music':
            datas=upload.objects.filter(category='music')

        elif cat=='sports':
            datas=upload.objects.filter(category='sports')

        print(datas)
        for i in datas:
            print(i.uid)
        filtered_queryset = [item for item in data if item['id'] in datas.values_list('uid', flat=True)]

        queryset = QuerySet(model=upload, query=upload.objects.all().query, using=upload.objects.db)
        queryset._result_cache = filtered_queryset 
        print(queryset)    
        return render(request, 'layout/home.html', {'video': queryset})
    






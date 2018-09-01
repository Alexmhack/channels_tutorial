# channels_tutorial
working along django channels official tutorial and creating a chat service with chat groups

# Dependencies

**requirements.txt**
```
django==2.1
channels==2.1.3
asgi_redis==1.4.3
```

# Installation

**cmd**
```
> pip install django
> pip install channels
> pip install asgi_redis
```

Launch ubuntu1804 using the command ubuntu1804

**Ubuntu1804**
```
> ubuntu1804
$ sudo apt-get install redis-server
$ redis-server
```

**Ubuntu1804** is the ubuntu terminal and some features of ubuntu from the ubuntu app 
donwloaded from play store, follow the instructions given in the description of the app

Once redis-server is installed you don't need to start it everytime, if an error comes on
running the command ```redis-server``` that means server is already running and you can 
restart the server using

**cmd**
```
> redis-cli shutdown
> redis-server
```

# Start project
Start fresh django project *mysite* inside virtualenv or outside of it as we discussed in 
[django_channels github repo](https://github.com/Alexmhack/django_channels)

**cmd**
```
> django-admin startproject mysite
> cd mysite
> python manage.py startapp chat
```

Start a new app named chat and add it in your installed apps settings

Add a *index.html* file in your templates folder

Using javascript/jquery we are going to open the url for the room name entered in the input

**templates/chat/index.html**
```
<!-- SCRIPTS -->
    <script type="text/javascript" charset="utf-8" async defer>
        var roomName = $("#room-name-input").focus();

        $("#room-name-input").keyup(function(e) {
            if (e.keyCode === 13) {
                $("#room-name-submit").click();
            }
        });

        $("#room-name-submit").click(function(e) {
            var roomName = $("#room-name-input").val();
            window.location.pathname = '/chat/' + roomName + '/';
        })
    </script>
```

We have used jquery but you can use plain javascript. Using the .val() function from jquery 
we fetch the value of the input form with id *room-name-input* and then using javascript 
```window.location.pathname``` we enter the url for room name

Now we have to create a view and url for that view in our chat app 

**chat/views.py**
```
from django.shortcuts import render

def index(request):
	return render(request, 'chat/index.html', {})
```

Create new file in chat app

**chat/urls.py**
```
from django.urls import path

from .views import index

urlpatterns = [
	path('', index, name='index'),
]
```

include the chat app urls in main project urlconf

**mysite/urls.py**
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
]
```

Now let's check 

**mysite**
```
> python manage.py runserver
```

Enter in anything and press enter or just hit the button and you will be taken to the
new url *127.0.0.1/chat/<input-entered>*. 

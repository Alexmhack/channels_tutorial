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

# Integrating channels library
In the section we are going to integrate our simple non-functional django app with channels
library and make our chat rooms functional

We will be creating routes for channels just like we create urls in urlconf for our django 
project, routes work in the same way, it tells the channels what to run when an HTTP request
is received by channels server.

Create a new file for routing inside mysite folder where our settings.py file lies

**mysite/routing.py**
```
from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({
	# (http->django views is added by default)
})
```
**[SOURCE](https://channels.readthedocs.io/en/latest/tutorial/part_1.html)**

We don't need to add our views they are added by default as the comment says

Now we need to tell our django project about channels by including library inside our project
installed apps settings

**mysite/settings.py**
```
INSTALLED_APPS = [
    'channels',
    'chat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Now for pointing channels to root configuration, edit the **mysite/settings.py** file and add
```ASGI_APPLICATION``` variable with value a path for our routing file

```
ASGI_APPLICATION = 'mysite.routing.application'
```

*mysite* is the folder, *routing* is the routing.py file we just created and application is 
what we added in routing file.

Run the server again and you will see that channels has overtaken our default django server.

```
> python manage.py runserver

Performing system checks...

System check identified no issues (0 silenced).
September 01, 2018 - 10:24:20
Django version 2.0.7, using settings 'mysite.settings'
Starting ASGI/Channels version 2.1.3 development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
2018-09-01 10:24:20,773 - INFO - server - HTTP/2 support not enabled (install the http2 and tls Twisted extras)
2018-09-01 10:24:20,773 - INFO - server - Configuring endpoint tcp:port=8000:interface=127.0.0.1
2018-09-01 10:24:20,773 - INFO - server - Listening on TCP address 127.0.0.1:8000

```

Locate to the same url [127.0.0.1/chat](http://127.0.0.1:8000/chat/) and you should see the same
page again, in your console you should see that channels is working finely with our project

# Add room view
In this section we will be creating a new view for room where users can chat with each other 
while in the same room.

Create a new template for this view

**templates/chat/room.html**
```
{% block script %}
    
    <script type="text/javascript" charset="utf-8" async defer>
        
        var roomName = {{ room_name_json }};

        var chatSocket = new Websocket(
            'ws://' + window.location.host + 'ws/chat/' + roomName + '/'
        );

        chatSocket.onmessage = function(e) {
            var data =  JSON.parse(e.data);
            var message = data['message'];
            $("#chat-log").val() += (message  +'\n');
        };

        chatSocket.onclose = function(e) {
            console.log("chat socket closed unexpectedly");
        };

        $("#chat-message-input").focus();

        $("#chat-message-input").keyup(function(e) {
            if (e.keyCode === 13) {
                $("#chat-message-submit").click();
            }
        });

        $("#chat-message-submit").click(function(e) {
            var $messageInput = $("#chat-message-input");
            var message = $messageInput.val();

            chatSocket.send(JSON.stringify({
                'message': message
            }));

            $messageInput.val('');
        });

    </script>

{% endblock %}
```

We send the context variable room_name_json from our *room_view* inside 
**chat/views.py**

```
import json

from django.shortcuts import render
from django.utils.safestring import mark_safe

def room_view(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

```

1. If chatSocket received a message then we parse the json data and store the message 
from it in a js variable and add the message in the textarea.

2. If we close the browser then we print a message on the console.

3. If user pressed enter we click the send button.

4. If the send button is pressed then we fetch the entered message from the input
and send message from the WebSocket instance and make the input field empty.

After our view is ready we create a url for our view.

**chat/urls.py**
```
    ...
    path('<room_name>/', room_view, name='room-view'),
```

**NOTE:** '/' should be added after <room_name> in the url for our room_view

# Channel Consumer
Now we will create a basic consumer that accepts WebSocket connections on the path
```ws/chat/room_name/ ``` that takes any message it receives on the WebSocket and 
echoes it back to the same WebSocket.

**NOTE:** We have used a ws/ prefix for sending the web socket because using it we 
can distinguish between the WebSocket connections from ordinary HTTP connections

Create a new file inside the chat app ```consumers.py```. Inside that file we simply
create synchronous WebSocket consumer that accepts all connections, receives messages 
from its client, and echos those messages back to the same client. For now it does not 
broadcast messages to other clients in the same room.

We need to create a routing configuration for tha chat app that has a route to the 
consumer. Create a new file inside chat app **routing.py**

**chat/routing.py**
```
from django.urls import path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<room_name>/', ChatConsumer),
]
```

The next step is to point the root routing configuration at the chat.routing module.

**mysite/routing.py**
```
import chat.routing

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    )
})
```

What above piece of code does is, we create a new key named 'websocket' in the 
ProtocolTypeRouter, any connection is made to the channels server it is inspected by
*ProtocolTypeRouter* and if it is a WebSocket connection like **ws:// or wss://** then 
it is passed onto *AuthMiddlewareStack*.

AuthMiddlewareStack provides the connection with a reference to the currently 
authenticated user just like the django's AuthenticationMiddleware does with the 
request object through which we can use the request variables such as ```request.user
```.

AuthMiddlewareStack hands over the connection to the URLRouter which simply routes the
HTTP path to a particular consumer based on the provided url patterns just like django
does with its urls and then urls routes to particular views.

**Run migrations** to apply database changes (Django’s session framework needs the 
database) and then start the Channels development server:

Open [http://127.0.0.1:8000/chat/lobby/](http://127.0.0.1:8000/chat/lobby/) and
enter any message in the input field and you should see the message echoed back to 
you from the channels server.

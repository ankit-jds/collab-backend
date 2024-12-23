# collab-backend
Realtime Collaboration Backend

Created virtual environment

Installed django djangorestframework

startproject
startapp
folder structure

runserver successful.

✅create RESTful GET API 

✅installed channels_redis django-redis daphne
ASGI setup
setup asgi routing
collab consumer connected over websocket

✅complete the basic websocket receive, send to group, channel layers, etc

✅complete document model, get documents, get specific document, create document (POST).

✅retrieve the document latest content and send to user when websocket connection established.

create operation model and save each operation i.e (INSERT/DELETE) in db 

For realtime collaboration tool like google doc.

Initially,
create document model => to store the content of document

implement django-redis to cache document, latest versions  

i would consider only operations like INSERT, DELETE
create operation model => to store each operation in database, as logs for aggragating and making latest version.

create snapshot => to store various versions of document.

cron job to aggregate operation and create a snapshot and update document 

text cursor (to show where other users are editing) 

will do the authentication, authorisation 
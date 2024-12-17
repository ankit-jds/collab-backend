from django.urls import re_path
from collaboration.views import *

urlpatterns = [re_path(r"^document/$", DocumentView.as_view(), name="document")]

from django.urls import re_path
from collaboration.views import *

urlpatterns = [
    re_path(r"^document/$", DocumentView.as_view(), name="document"),
    re_path(r"^qrcode/$", QRCodeView.as_view(), name="qrcode"),
    # re_path(r"^sj/$", SnapshotJobView.as_view(), name="snapshot_job"),
]

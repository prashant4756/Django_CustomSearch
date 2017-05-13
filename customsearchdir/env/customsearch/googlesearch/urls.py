from django.conf.urls import url

import googlesearch.views

urlpatterns = [
	url(r'^custom_search/', googlesearch.views.custom_search, name='customSearch'),
]
from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	#bare Block /block
	#bare all

	url(r'^test$', views.test, name='test'),
	url(r'^search/$', views.search, name='search'),
	url(r'^search/(?P<data>.*)/$', views.search, name='search'),
	url(r'^block/$', views.blockReview, name='blockReview'),
	url(r'^block/(?P<blockHeigth>[0-9]+)/$', views.block, name='block'),
	url(r'^transaction/$', views.transactionReview, name='transactionReview'),
	url(r'^transaction/(?P<transactionId>[0-9]+)/$', views.transactionId, name='transactionId'),
	url(r'^transaction/(?P<transactionHash>[a-fA-F0-9]{64})/$', views.transactionHash, name='transactionHash'),
	url(r'^input/$', views.inputReview, name='inputReview'),
	url(r'^input/(?P<inputId>[0-9]+)/$', views.input_, name='input_'),
	url(r'^output/$', views.outputReview, name='outputReview'),
	url(r'^output/(?P<outputId>[0-9]+)/$', views.output, name='output'),

]
from django.conf.urls import patterns, url

from app.views import *


urlpatterns = patterns('app.views',
    url(r'^$', GeoLookup.as_view(), name='geo_lookup'),
    url(r'^compose_message/$', ComposeMessage.as_view(), name='compose_message'),
    url(r'^user_messages/$', UserMessageList.as_view(), name='list_user_messages'),
    url(r'^message/(?P<pk>\d+)/$', MessageDetail.as_view(), name='message_detail'),
    url(r'^confirm_message_sent/(?P<message_id>\d+)/$', confirm_message_sent, name='confirm_message_sent'),
    url(r'^verify_email_pending/$', email_verification_prompt, name='email_verification_prompt'),
    url(r'^verify_email_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        email_verification_confirmation, name='email_verification_confirmation'),
    url(r'^verify_email_complete/$', email_verification_complete, name='email_verification_complete'),
)



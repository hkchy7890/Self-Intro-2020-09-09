from django.urls import path
from .views import mainpage, login_view, logout_view, about, whyit, photos, contact
from .views import create_post, posts_all, like_post, polls_main, poll_vote, poll_results

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', mainpage),
    path('login/', login_view),
    path('logout/', logout_view),
    path('about/', about),
    path('whyit/', whyit),
    path('photos/', photos),
    path('contact/', contact),
    path('createpost/', create_post),
    path('posts/', posts_all),
    path('like_post', like_post),
    path('polls/', polls_main),
    path('vote/<poll_id>/', poll_vote),
    path('results/<poll_id>/', poll_results),

]+staticfiles_urlpatterns()+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

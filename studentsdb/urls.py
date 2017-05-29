from django.conf.urls import patterns, include, url
from django.contrib import admin
from students.views.groups import GroupCreateView, GroupUpdateView, GroupDeleteView
from students.views.students import EditStudentView, StudentDeleteView
from .settings import MEDIA_ROOT, DEBUG
from students.views.journal import JournalView
from django.conf.urls import include, url 
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView, TemplateView


js_info_dict = {
    'packages': ('students',),
}

urlpatterns = patterns('',
# Students urls

    url(r'^$', 'students.views.students.students_list', name='home'),
    url(r'^students/add/?$', 'students.views.students.students_add', name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', EditStudentView.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),

# Groups urls

    url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
    url(r'^groups/add/$', GroupCreateView.as_view(), name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(), name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(), name='groups_delete'),

    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^contact-admin/$', 'students.views.contact_admin.contact_admin', name='contact_admin'),
                       
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users')),
    
    url(r'^jsi18n\.js$', 'django.views.i18n.javascript_catalog', js_info_dict),
    url('^set-language/$', 'students.views.set_language.set_language', name='set_language'),
                       

)

#urlpatterns = i18_patterns('',
#    url(r'^$', 'path.to.homepage.view', name='homepage'),
  #  url(r'^blog/$', include(blog_patterns), namespace='blog'),
#    url(r'^events/', include(events_patterns, namespace='events')),                       
#)



if DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT})
                           )

# Examples:
    # url(r'^$', 'studentsdb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


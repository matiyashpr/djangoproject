from django.conf.urls import patterns, include, url
from django.contrib import admin
from students.views.groups import GroupAddView, GroupUpdateView, GroupDeleteView, groups_list
from students.views.students import StudentUpdateView, StudentDeleteView
from .settings import MEDIA_ROOT, DEBUG
from students.views.journal import JournalView
from django.conf.urls import include, url 
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required
from students.views.subject import SubjectCreateView, SubjectUpdateView, SubjectDeleteView
from students.views.exams import ExamCreateView, ExamUpdateView, ExamDeleteView
from students.views.exam_results import ExamResultCreateView, ExamResultUpdateView, ExamResultDeleteView
from students.views.random_user import generate_users



js_info_dict = {
    'packages': ('students',),
}

urlpatterns = patterns('',
# Students urls

    url(r'^$', 'students.views.students.students_list', name='home'),
    url(r'^students/add/?$', 'students.views.students.students_add', name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),

# Groups urls

    url(r'^groups/$', login_required(groups_list), name='groups'),
    url(r'^groups/add/$', login_required(GroupAddView.as_view()), name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', login_required(GroupUpdateView.as_view()), name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', login_required(GroupDeleteView.as_view()), name='groups_delete'),

    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^contact-admin/$', 'students.views.contact_admin.contact_admin', name='contact_admin'),
                       
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users')),
    
    url(r'^jsi18n\.js$', 'django.views.i18n.javascript_catalog', js_info_dict),
    url('^set-language/$', 'students.views.set_language.set_language', name='set_language'),
                       
    url(r'^users/profile/$', login_required(TemplateView.as_view(template_name='registration/profile.html')), name='profile'),
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page':'home'}, name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users')),
                       
    url('^social/', include('social.apps.django_app.urls', namespace='social')),
                       
    url(r'^exams/$', 'students.views.exams.exams_list', name='exams'),
    url(r'^exams/add/$', ExamCreateView.as_view(), name='exams_add'),
    url(r'^exams/(?P<pk>\d+)/edit/$', ExamUpdateView.as_view(), name='exams_edit'),
    url(r'^exams/(?P<pk>\d+)/delete/$', ExamDeleteView.as_view(), name='exams_delete'),

    url(r'^exam_results/$', 'students.views.exam_results.exam_results', name='exam_results'), 
    url(r'^exam_results/add/$', ExamResultCreateView.as_view(), name='exam_result_add'),
    url(r'^exam_results/(?P<pk>\d+)/edit/$', ExamResultUpdateView.as_view(), name='exam_result_edit'),
    url(r'^exam_results/(?P<pk>\d+)/delete/$', ExamResultDeleteView.as_view(), name='exam_result_delete'),
                       
    url(r'^subjects/$', 'students.views.subject.subject_list', name='subjects'),
    url(r'^subjects/add/$', SubjectCreateView.as_view(), name='subjects_add'),
    url(r'^subjects/(?P<pk>\d+)/edit/$', SubjectUpdateView.as_view(), name='subjects_edit'),
    url(r'^subjects/(?P<pk>\d+)/delete/$', SubjectDeleteView.as_view(), name='subjects_delete'),

    url(r'^random_user/$', 'students.views.random_user.generate_users', name='generate_user'),
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


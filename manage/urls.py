from django.conf.urls.static import static
from django.urls import path, re_path
from ZGG.views import login, admin_logout, zgg_user, bill_edit, zgg_bill, ltt_user_json,\
     zgg_user_edit, detail, export_excel, import_sql, zgg_bill_json, zgg_user_json, ltt_user, ltt_user_edit

from ZGG import zg_visual
# from ZGG.views import page_not_found, page_error
from LTT.views import config, class_config, kind_config, project_config, download,\
    facility_edit, facility_json, facility, facility_copy, class_json, kind_json, project_json, \
    class_delete, kind_delete, project_delete, facility_fail_json, facility_fail, \
    board, board_json, going_form
from manage import settings

urlpatterns = [
    path('', login, name='login'),
    path('logout/', admin_logout, name='logout'),
    path('zgg/user', zgg_user, name='zgg_user'),
    path('ltt/user', ltt_user, name='ltt_user'),
    path('zgg/bill', zgg_bill, name='zgg_bill'),
    path('zgg/visual', zg_visual.visual, name='zgg/visual'),

    path('ltt_user_json', ltt_user_json, name='ltt_user_json'),
    path('zgg_user_json', zgg_user_json, name='zgg_user_json'),
    path('zgg_bill_json', zgg_bill_json, name='zgg_bill_json'),
    re_path('zgg/user/edit/(?P<user_id>\d+)', zgg_user_edit, name='user_edit'),
    re_path('ltt/user/edit/(?P<user_id>\d+)', ltt_user_edit, name='user_edit'),
    re_path('zgg/bill/edit/(?P<bill_id>\d+)', bill_edit, name='bill_edit'),
    re_path('zgg/bill/detail/(?P<bill_id>\d+)', detail, name='detail'),
    path('zgg/export_excel', export_excel, name='export_excel'),
    path('zgg/import_sql', import_sql, name='import_sql'),



    path('ltt/facility', facility, name='facility'),
    path('ltt/facility/fail', facility_fail, name='facility_fail'),
    re_path('ltt/facility/edit/(?P<id>\d+)', facility_edit, name='facility_edit'),
    re_path('ltt/facility/copy/(?P<id>\d+)', facility_copy, name='facility_copy'),
    path('ltt/config', config, name='config'),
    path('ltt/config/class', class_config, name='class_config'),
    path('ltt/config/kind', kind_config, name='kind_config'),
    path('ltt/config/project', project_config, name='project_config'),
    re_path('ltt/config/class/delete/(?P<id>\d+)', class_delete, name='class_delete'),
    re_path('ltt/config/kind/delete/(?P<id>\d+)', kind_delete, name='kind_delete'),
    re_path('ltt/config/project/delete/(?P<id>\d+)', project_delete, name='project_delete'),
    re_path('ltt/facility/log/download/(?P<id>\d+)', download, name='download'),
    path('ltt/board', board, name='board'),


    path('going_form', going_form, name='going_form'),
    path('board_json', board_json, name='board_json'),
    # path('ajax_project', ajax_project, name='ajax_project'),
    path('class_json', class_json, name='class_json'),
    path('kind_json', kind_json, name='kind_json'),
    path('project_json', project_json, name='project_json'),
    path('facility_json', facility_json, name='facility_json'),
    path('facility_fail_json', facility_fail_json, name='facility_fail_json'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'zgg_user.views.page_not_found'
# handler500 = 'zgg_user.views.page_error'

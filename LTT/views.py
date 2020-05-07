import os

from datetime import datetime, timedelta
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import urlquote

from manage import settings
from .models import Project, Ltt, Kind, Class
import json


# Create your views here.

# LTT
def facility_json(request):
    if request.method == 'GET':
        pageSize = int(request.GET.get('pageSize'))
        pageNumber = int(request.GET.get('pageNumber'))
        searchText = request.GET.get('searchText')
        sortName = request.GET.get('sortName')
        sortOrder = request.GET.get('sortOrder')

        sn = request.GET.get('search_sn').strip()
        k_name = request.GET.get('search_k_name').strip()
        result = request.GET.get('search_result').strip()
        search_time = request.GET.get('search_time').strip()
        rows = []

        if sn or k_name or result or search_time:
            if search_time:
                search_time = search_time.split(' ')
                start_time = search_time[0]
                end_time = search_time[-1]

                total = Ltt.objects.filter(
                    Q(sn__contains=sn) & Q(k__k_name__contains=k_name) & Q(result__contains=result) & Q(
                        put_time__range=(start_time, end_time))).order_by('-put_time').order_by('sn').count()
                ltt = Ltt.objects.filter(
                    Q(sn__contains=sn) & Q(k__k_name__contains=k_name) & Q(result__contains=result) & Q(
                        put_time__range=(start_time, end_time))).order_by('-put_time').order_by('sn')[
                      (pageNumber - 1) * pageSize:(pageNumber) * pageSize]

            else:
                total = Ltt.objects.filter(
                    Q(sn__contains=sn) & Q(k__k_name__contains=k_name) & Q(result__contains=result)).order_by(
                    '-put_time').order_by('sn').count()
                ltt = Ltt.objects.filter(
                    Q(sn__contains=sn) & Q(k__k_name__contains=k_name) & Q(result__contains=result)).order_by(
                    '-put_time').order_by('sn')[(pageNumber - 1) * pageSize:(pageNumber) * pageSize]
        else:
            total = Ltt.objects.all().count()
            ltt = Ltt.objects.order_by('-put_time').order_by('sn')[(pageNumber - 1) * pageSize:(pageNumber) * pageSize]

        result = {"total": total, "rows": rows}
        for data in ltt:
            rows.append(
                {'id': data.id, 'put_time': str(data.put_time), 'ltt_id': data.ltt_id, 'sn': data.sn, 'pn': data.pn,
                 'pn_desc': data.pn_desc, 'out_time': str(data.out_time), 'execute_user': data.execute_user,
                 'start_time': str(data.start_time),
                 'over_time': str(data.over_time), 'result': data.result, 'log': str(data.log),
                 'p_name': data.p.p_name,
                 'remark': data.remark, 'c_name': data.c.c_name, 'k_name': data.k.k_name})

        return HttpResponse(json.dumps(result), content_type="application/json")


def facility(request):
    login_user = request.session['login_user']
    ltt = Ltt.objects.all().values()
    project = Project.objects.all().values()
    class_ = Class.objects.all().values()
    kind = Kind.objects.all().values()
    if request.method == 'POST':
        p_id_list = request.POST.getlist('p_id')
        k_id = request.POST.get('k_id')
        c_id = request.POST.get('c_id')
        sn = request.POST.get('sn').strip()
        pn = request.POST.get('pn').strip()
        pn_desc = request.POST.get('pn_desc').strip()
        put_time = request.POST.get('put_time', None)
        out_time = request.POST.get('out_time', None)
        execute_user = request.session['login_user']['name'].strip()
        start_time = request.POST.get('start_time', None)
        over_time = request.POST.get('over_time', None)
        result = request.POST.get('result').strip()
        remark = request.POST.get('remark').strip()
        log = request.FILES.get('log', None)
        if put_time == '':
            put_time = None
        if out_time == '':
            out_time = None
        if start_time == '':
            start_time = None
        if over_time == '':
            over_time = None
        if c_id == '' or k_id == '' or sn == '' or pn == '' or pn_desc == '' or put_time == '':
            error = '设备信息不能为空'
        else:
            for p_id in p_id_list:
                Ltt.objects.create(
                    c_id=c_id,
                    sn=sn,
                    pn=pn,
                    pn_desc=pn_desc,
                    put_time=put_time,
                    out_time=out_time,
                    execute_user=execute_user,
                    start_time=start_time,
                    over_time=over_time,
                    result=result,
                    remark=remark,
                    log=log,
                    k_id=k_id,
                    p_id=p_id,
                )
                try:
                    path = os.path.join(settings.MEDIA_ROOT, 'l_log/%s' % log.name)
                    if path:
                        with open(path, 'wb') as f:
                            for i in log.chunks():
                                f.write(i)
                                print('创建成功')
                            f.close()
                except AttributeError:
                    continue
            return redirect('/ltt/facility')
    if request.session['login_user']['ltt_authority'] == '普通用户':
        return render(request, 'ltt/facility_user.html', locals())
    else:
        return render(request, 'ltt/facility.html', locals())


# 文件下载
def download(request, id):
    ltt = Ltt.objects.filter(pk=id).first()
    filename = str(ltt.log)
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    file = open(filepath, 'rb')
    response = HttpResponse(file)
    filename = '%s-%s-%s.txt' % (ltt.p.c.c_name, ltt.p.p_name, ltt.result)
    filename = urlquote(filename)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    file.close()
    return response


def facility_edit(request, id):
    login_user = request.session['login_user']
    project = Project.objects.all().values()
    class_ = Class.objects.all().values()
    kind = Kind.objects.all().values()
    ltt = Ltt.objects.filter(pk=id).first()
    if request.method == 'POST':
        k_id = request.POST.get('k_id')
        p_id = request.POST.get('p_id')
        c_id = request.POST.get('c_id')

        sn = request.POST.get('sn').strip()
        pn = request.POST.get('pn').strip()
        pn_desc = request.POST.get('pn_desc').strip()
        put_time = request.POST.get('put_time')
        out_time = request.POST.get('out_time')
        start_time = request.POST.get('start_time')
        over_time = request.POST.get('over_time')
        execute_user = request.POST.get('execute_user').strip()
        result = request.POST.get('result').strip()
        remark = request.POST.get('remark').strip()
        log: InMemoryUploadedFile = request.FILES.get('log', ltt.log)
        if out_time != '':
            others_id = Ltt.objects.filter(sn=ltt.sn).values('id')
            for other_id in others_id:
                other_facility = Ltt.objects.filter(id=other_id['id']).first()
                other_facility.out_time = out_time
                other_facility.save()

        if remark != '':
            others_id = Ltt.objects.filter(sn=ltt.sn).values('id')
            for other_id in others_id:
                other_facility = Ltt.objects.filter(id=other_id['id']).first()
                other_facility.remark = remark
                other_facility.save()
        if put_time == '':
            put_time = None
        if out_time == '':
            out_time = None
        if start_time == '':
            start_time = None
        if over_time == '':
            over_time = None
        if ltt.log and log != ltt.log:
            d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            old_path = os.path.join(d, 'media/%s' % ltt.log.name)
            os.remove(old_path)
        if ltt:
            ltt.sn = sn
            ltt.pn = pn
            ltt.pn_desc = pn_desc
            ltt.put_time = put_time
            ltt.out_time = out_time
            ltt.execute_user = execute_user
            ltt.start_time = start_time
            ltt.over_time = over_time
            ltt.result = result
            ltt.remark = remark
            ltt.log = log
            ltt.k_id = k_id
            ltt.p_id = p_id
            ltt.c_id = c_id
            error = '修改成功'
            ltt.save()

            if log != ltt.log:
                img_path = os.path.join(settings.MEDIA_ROOT, 'l_log/%s' % log.name)
                if img_path:
                    with open(img_path, 'wb') as f:
                        for i in log.chunks():
                            f.write(i)
                            print('修改log成功')
                        f.close()
            return redirect('/ltt/facility')
        else:
            error = '修改失败'
    if request.session['login_user']['ltt_authority'] == '系统管理员':
        return render(request, 'ltt/facility_edit_admin.html', locals())
    else:
        return render(request, 'ltt/facility_edit.html', locals())


def facility_copy(request, id):
    login_user = request.session['login_user']
    ltt = Ltt.objects.filter(pk=id).first()
    if request.method == 'GET':
        Ltt.objects.create(
            id=None,
            c_id=ltt.c_id,
            k_id=ltt.k_id,
            p_id=ltt.p_id,
            result=ltt.result,
            sn=ltt.sn,
            pn=ltt.pn,
            pn_desc=ltt.pn_desc,
            put_time=ltt.put_time,
            out_time=ltt.out_time,
            execute_user=ltt.execute_user,
            remark=ltt.remark,
            log='',

        )
        return redirect('/ltt/facility')
    else:
        return render(request, 'ltt/facility.html', locals())


# def ajax_project(request):
#     if request.method == 'GET':
#         c_name = request.GET.get('c_name', None)
#         data = []
#         if c_name:
#             c_id = Class.objects.get(c_name=c_name).id
#             data = list(Project.objects.filter(c_id=c_id).values("id", "p_name"))
#         return HttpResponse(json.dumps(data), "application/json")


def facility_fail_json(request):
    if request.method == 'GET':
        pageSize = int(request.GET.get('pageSize'))
        pageNumber = int(request.GET.get('pageNumber'))
        searchText = request.GET.get('searchText')
        sortName = request.GET.get('sortName')
        sortOrder = request.GET.get('sortOrder')

        total = Ltt.objects.filter(result='FAIL').count()
        ltt = Ltt.objects.filter(result='FAIL').order_by('-id')[(pageNumber - 1) * pageSize:(pageNumber) * pageSize]
        rows = []
        result = {"total": total, "rows": rows}

        for data in ltt:
            rows.append(
                {'id': data.id, 'put_time': str(data.put_time), 'sn': data.sn, 'pn': data.pn, 'pn_desc': data.pn_desc,
                 'out_time': str(data.out_time), 'execute_user': data.execute_user, 'start_time': str(data.start_time),
                 'over_time': str(data.over_time), 'result': data.result, 'log': str(data.log), 'p_name': data.p.p_name,
                 'remark': data.remark, 'c_name': data.c.c_name, 'k_name': data.k.k_name, })

        return HttpResponse(json.dumps(result), content_type="application/json")


def facility_fail(request):
    login_user = request.session['login_user']
    if request.session['login_user']['ltt_authority'] == '普通用户':
        return render(request, 'ltt/facility_fail_user.html', locals())
    else:
        return render(request, 'ltt/facility_fail.html', locals())


def config(request):
    login_user = request.session['login_user']
    return render(request, 'ltt/config.html', locals())


def class_json(request):
    if request.method == 'GET':
        pageSize = int(request.GET.get('pageSize'))
        pageNumber = int(request.GET.get('pageNumber'))
        searchText = request.GET.get('searchText')
        sortName = request.GET.get('sortName')
        sortOrder = request.GET.get('sortOrder')

        total = Class.objects.all().count()
        class_ = Class.objects.order_by('-id')[(pageNumber - 1) * pageSize:(pageNumber) * pageSize]
        rows = []
        result = {"total": total, "rows": rows}

        for data in class_:
            rows.append({'id': data.id, 'c_name': data.c_name})

        return HttpResponse(json.dumps(result), content_type="application/json")


def class_config(request):
    login_user = request.session['login_user']
    if request.method == 'POST':
        c_name = request.POST.get('c_name').strip()
        find_data = Class.objects.filter(c_name=c_name)
        if find_data:
            error = '该类别已存在！'
        elif c_name == '':
            error = '机种不能为空'
        else:
            Class.objects.create(
                c_name=c_name
            )
            return redirect('/ltt/config/class')
        return render(request, 'ltt/config_class.html', locals())
    return render(request, 'ltt/config_class.html', locals())


def class_delete(request, id):
    if request.method == 'GET':
        Class.objects.filter(id=id).delete()
        return redirect('/ltt/config/class')
    return render(request, 'ltt/config_class.html', locals())


def kind_json(request):
    if request.method == 'GET':
        pageSize = int(request.GET.get('pageSize'))
        pageNumber = int(request.GET.get('pageNumber'))
        searchText = request.GET.get('searchText')
        sortName = request.GET.get('sortName')
        sortOrder = request.GET.get('sortOrder')

        total = Kind.objects.all().count()
        kind = Kind.objects.order_by('-id')[(pageNumber - 1) * pageSize:(pageNumber) * pageSize]
        rows = []
        result = {"total": total, "rows": rows}

        for data in kind:
            rows.append({'id': data.id, 'k_name': data.k_name, })

        return HttpResponse(json.dumps(result), content_type="application/json")


def kind_config(request):
    login_user = request.session['login_user']
    if request.method == 'POST':
        k_name = request.POST.get('k_name').strip()
        find_data = Kind.objects.filter(k_name=k_name)
        if find_data:
            error = '该机种已存在！'
        elif k_name == '':
            error = '机种不能为空'
        else:
            Kind.objects.create(
                k_name=k_name
            )
            return redirect('/ltt/config/kind')
        return render(request, 'ltt/config_kind.html', locals())
    return render(request, 'ltt/config_kind.html', locals())


def kind_delete(request, id):
    if request.method == 'GET':
        Kind.objects.filter(id=id).delete()
        return redirect('/ltt/config/kind')
    return render(request, 'ltt/config_kind.html', locals())


def project_json(request):
    if request.method == 'GET':
        pageSize = int(request.GET.get('pageSize'))
        pageNumber = int(request.GET.get('pageNumber'))

        total = Project.objects.all().count()
        project = Project.objects.order_by('-id')[(pageNumber - 1) * pageSize:(pageNumber) * pageSize]
        rows = []
        result = {"total": total, "rows": rows}

        for data in project:
            rows.append({'id': data.id, 'p_name': data.p_name})

        return HttpResponse(json.dumps(result), content_type="application/json")


def project_config(request):
    login_user = request.session['login_user']
    class_ = Class.objects.all().values()
    if request.method == 'POST':
        p_name = request.POST.get('p_name')
        find_data = Project.objects.filter(p_name=p_name)
        if find_data:
            error = '该测试项目已存在！'
        elif p_name == '':
            error = '测试项目不能为空'
        else:
            Project.objects.create(
                p_name=p_name
            )
            return redirect('/ltt/config/project')
        return render(request, 'ltt/config_project.html', locals())
    return render(request, 'ltt/config_project.html', locals())


def project_delete(request, id):
    login_user = request.session['login_user']
    if request.method == 'GET':
        Project.objects.filter(id=id).delete()
        return redirect('/ltt/config/project')
    return render(request, 'ltt/config_project.html', locals())


def board_json(request):
    if request.method == 'GET':
        sn_dict = Ltt.objects.values('sn').distinct()
        now_year = datetime.now().year
        #  柱状图
        pass_count_bar = 30
        going_count_bar = 0
        fail_count_bar = 2
        bar_pass_list = [224, 158]
        bar_going_list = [0, 0]
        bar_fail_list = [0, 0]
        for sn in sn_dict:
            result_list = Ltt.objects.filter(sn=sn['sn'], start_time__year__gte=now_year).values('result')
            result = []
            for data in result_list:
                result.append(data['result'])
            # print(result)
            # print(result_list)

            if 'PASS' in result and 'FAIL' not in result and 'On Going' not in result:
                pass_count_bar += 1
            elif 'FAIL' not in result and 'On Going' in result:
                going_count_bar += 1
            elif 'FAIL' in result:
                fail_count_bar += 1
        # print('测试完成：%s' % pass_count_bar)
        # print('正在测试：%s' % going_count_bar)
        # print('异常：%s' % fail_count_bar)
        bar_pass_list.append(pass_count_bar)
        bar_going_list.append(going_count_bar)
        bar_fail_list.append(fail_count_bar)
        bar = (bar_pass_list, bar_going_list, bar_fail_list, ['完成（台）', '在测（台）', '异常（台）'])
        # print(bar)

        # 饼状图
        pass_count_pie = 30
        fail_count_pie = 2
        going_count_pie = 0
        pie_list = []
        for sn in sn_dict:
            result_list = Ltt.objects.filter(sn=sn['sn']).values('over_time', 'result')
            result = []
            over_time = []
            for data in result_list:
                result.append(data['result'])
                over_time.append(data['over_time'])

            if 'PASS' in result and 'FAIL' not in result and 'On Going' not in result and len(over_time) == len(result):
                pass_count_pie += 1
            elif 'FAIL' not in result and 'On Going' in result:
                going_count_pie += 1
            elif 'FAIL' in result:
                fail_count_pie += 1
        # print('测试完成：%s' % pass_count_pie)
        # print('正在测试：%s' % going_count_pie)
        # print('异常：%s' % fail_count_pie)

        pass_dict = {'value': pass_count_pie, 'name': '测试完成'}
        going_dict = {'value': going_count_pie, 'name': '在测'}
        fail_dict = {'value': fail_count_pie, 'name': '异常'}
        pie_list.append(pass_dict)
        pie_list.append(going_dict)
        pie_list.append(fail_dict)
        pie = (pie_list, [pass_dict['name'], going_dict['name'], fail_dict['name']])
        # print(pie)
        return JsonResponse({"pie": pie, "bar": bar}, content_type="application/json", safe=False)


def going_form(request):
    if request.method == 'GET':
        pageSize = int(request.GET.get('pageSize'))
        pageNumber = int(request.GET.get('pageNumber'))
        sn_dict = Ltt.objects.values('sn').distinct()[(pageNumber - 1) * pageSize:(pageNumber) * pageSize]
        rows = []
        data = {}
        for sn in sn_dict:
            total = Ltt.objects.values('sn').distinct().count()
            data_first = Ltt.objects.order_by('start_time').filter(sn=sn['sn']).values('pn', 'pn_desc', 'sn', 'remark',
                                                                                      'start_time').first()
            result_values = Ltt.objects.filter(sn=sn['sn']).values('result')

            ltt_result_values = Ltt.objects.order_by('start_time').filter(sn=sn['sn']).values('sn', 'p__p_name',
                                                                                              'result')
            rcq = ''
            nc = ''
            dd = ''
            fb = ''
            for ltt_result_value in ltt_result_values:
                if ltt_result_value['p__p_name'] == '软重启':
                    rcq = ltt_result_value['result']
                elif ltt_result_value['p__p_name'] == '断电重启':
                    dd = ltt_result_value['result']
                elif ltt_result_value['p__p_name'] == '内存测试':
                    nc = ltt_result_value['result']
                elif ltt_result_value['p__p_name'] == '封包测试':
                    fb = ltt_result_value['result']

            result_list = []
            for result_value in result_values:
                result_list.append(result_value['result'])

            while len(result_list) != 4:
                result_list.append('')

            data_last = Ltt.objects.order_by('start_time').filter(sn=sn['sn']).values('pn', 'pn_desc', 'sn',
                                                                                      'remark', 'start_time').last()
            if data_first['start_time'] == None and data_last['start_time']:
                start_time = str(data_last['start_time'])
                over_time = data_last['start_time'] + timedelta(days=28)
            elif data_first['start_time'] == None and data_last['start_time'] == None:
                start_time = ''
                over_time = ''
            else:
                start_time = str(data_first['start_time'])
                over_time = data_first['start_time'] + timedelta(days=28)

            rows.append({'pn': data_first['pn'], 'pn_desc': data_first['pn_desc'], 'sn': data_first['sn'],
                         'remark': data_first['remark'], 'start_time': start_time,
                         'over_time': str(over_time), 'dd': dd, 'rcq': rcq, 'nc': nc, 'fb': fb})

            data = {"total": total, "rows": rows}

        return HttpResponse(json.dumps(data), content_type="application/json")


def board(request):
    login_user = request.session['login_user']
    return render(request, 'ltt/board.html', locals())

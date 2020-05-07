import json

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection

from ZGG.models import Bill


def visual(request):
    try:
        if request.method == 'GET':
            # 方便看所有列名
            pd.set_option('display.max_columns', None)

            # 创建游标
            mycursor = connection.cursor()

            # 从excel读取数据文件
            df = pd.read_sql('select * from bill', con=connection)

            # pivot完成数据表透视功能，aggfunc表示计算个数，也可以使用np.sum  np.mean等统计手法
            # index 行使用step id， column列名使用product name, value使用计数
            df1 = pd.pivot_table(df, index=[u'state', u'pro1', u'pro2', u'pro3'], columns=['zc_site'],
                                 values=['zc_type'], fill_value=0, margins=True, aggfunc='count').query(
                'state == ["启用"]').sort_index(axis=0, ascending=False)

            pd.set_option('colheader_justify', 'center')  # FOR TABLE <th>

            html_string = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="Dashboard">
    <meta name="keyword" content="Dashboard, Bootstrap, Admin, Template, Theme, Responsive, Fluid, Retina">
    <link rel="icon" href="../../static/img/favicon.ico" type="image/x-icon"/>
    <title>治工具看板-管理平台</title>
    <link rel="stylesheet" type="text/css" href="../../static/css/df_style.css"/>
    <link href="../../static/css/bootstrap.css" rel="stylesheet">

    <link href="../../static/css/font-awesome/css/font-awesome.css" rel="stylesheet"/>
    <link rel="stylesheet" type="text/css" href="../../static/css/zabuto_calendar.css">
    <link rel="stylesheet" type="text/css" href="../../static/css/jquery.gritter.css"/>
    <link rel="stylesheet" type="text/css" href="../../static/css/lineicons/style.css">
    
    <link href="https://cdn.bootcss.com/bootstrap-table/1.11.1/bootstrap-table.min.css" rel="stylesheet">
    <link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
    <link href="../../static/css/style.css" rel="stylesheet">
    <link href="../../static/css/style-responsive.css" rel="stylesheet">


    <script src="../../static/js/Chart.js"></script>
</head>

<body>

<section id="container">

    <!--header-->
    <header class="header black-bg" style="background-color:whitesmoke;">
        <div class="sidebar-toggle-box">
            <div class="fa fa-bars tooltips" data-placement="right" data-original-title="导航"></div>
        </div>
        <!--logo start-->
        <a href="/index" class="logo" style="color: gray"><b>EMS工程管理系统</b></a>
        <!--logo end-->
    <div class="top-menu">
        <ul class="nav pull-right top-menu">
            <li><a class="logout" href="/logout/" style="color: white"><span class="glyphicon glyphicon-off"></span>&nbsp;退出</a></li>
        </ul>
    </div>

    </header>


    <!--sidebar start-->
    <aside>
        <div id="sidebar" class="nav-collapse">
            <!-- sidebar menu start-->
            <ul class="sidebar-menu" id="nav-accordion">

                <p class="centered"><a href="#">
                    <img src="../../static/img/touxiang.jpg"
                         width="200" height="100"></a></p>
                <h5 class="centered">

                </h5>


            

            <li class="sub-menu">
                <a href="javascript:;">
                    <i class="fa fa-ge"></i>
                    <span>治工具管理系统</span>
                </a>
                <ul class="sub">
                    <li><a href="/zgg/bill">资产信息库</a></li>
                    <li><a href="/zgg/visual">治工具看板</a></li>
                </ul>
            </li>

            <li class="sub-menu">
                <a href="javascript:;">
                    <i class="fa fa-sitemap"></i>
                    <span>LTT管理系统</span>
                </a>
                <ul class="sub">
                    <li><a href="/ltt/facility">LTT设备状态管理</a></li>
                    <li><a href="/ltt/facility/fail">Fail-Report</a></li>
                    <li><a href="/ltt/board">LTT看板</a></li>
                </ul>
            </li>
            </ul>
            <!-- sidebar menu end-->
        </div>
    </aside>

    <!--sidebar end-->

    <!-- **********************************************************************************************************************************************************
    MAIN CONTENT
    *********************************************************************************************************************************************************** -->
    <!--main content start-->
    <section id="main-content">
        <section class="wrapper" style='background-color: white;'>
            <h2 class="text-center">生产治工具统计表</h2>
            <button data-toggle="modal" class="btn btn-default"">
            <span class="glyphicon glyphicon-download-alt" aria-hidden="true"></span>&nbsp;导出图表</button>
            <br>
            <br>
            {table}
        </section>
    </section>
    <!--main content end-->


    <!--footer start-->
    <footer class="common_footer">
        <p class="text-center text-white">Copyright 2010 - 2019 山石网科，保留一切权利。</p>
        <p class="text-center text-white">&copy;2019 Hillstone Networks All Rights Reserved. | Manage 1.0.0</p>
    </footer>

    <!--footer end-->

</section>


<!-- js placed at the end of the document so the pages load faster -->
<script src="../../static/js/jquery.js"></script>
<script src="../../static/js/jquery.table2excel.js"></script>
<script src="../../static/js/table2excel.js"></script>

<script src="../../static/js/jquery-ui-1.9.2.custom.min.js"></script>
<script src="../../static/js/bootstrap.min.js"></script>
<script class="include" type="text/javascript" src="../../static/js/jquery.dcjqaccordion.2.7.js"></script>
<script src="../../static/js/jquery.scrollTo.min.js"></script>
<script src="../../static/js/jquery.nicescroll.js" type="text/javascript"></script>
<script src="../../static/js/jquery.sparkline.js"></script>
<script src="../../static/js/jquery-ui-1.9.2.custom.min.js"></script>

<!--common script for all pages-->
<script src="../../static/js/common-scripts.js"></script>

<script type="text/javascript" src="../../static/js/jquery.gritter.js"></script>
<script type="text/javascript" src="../../static/js/gritter-conf.js"></script>

</body>
</html>
    
            '''
            # title = '生产治工具统计表'
            with open('templates/zgg/visual.html', 'w', encoding='utf-8') as f:
                f.write(html_string.format(
                    table=df1.to_html(classes='mystyle').replace('pro1', '').replace('pro2', '')
                        .replace('state', '').replace('启用', '').replace('pro3', '').replace('zc_type', '')
                        .replace('zc_site', '').replace('All', '总计(启用)')
                        .replace('class="dataframe mystyle">',
                                 'cellpadding="-1" id="datatable" class="mystyle table table-condensed text-center">'
                                 # .replace('class="dataframe mystyle">','cellpadding="-1" class="mystyle table table-condensed text-center"><caption><h3>{}</h3></caption>'.format(title)
                                 .replace(
                                     '<tr><th></th><th></th><th></th><th></th><th colspan="6" halign="left"></th></tr>',
                                     ' '))))

            return render(request, 'zgg/visual.html', locals())
        else:
            return render(request, 'zgg/visual.html', locals())
    except ValueError:
        return redirect('/zgg/bill')

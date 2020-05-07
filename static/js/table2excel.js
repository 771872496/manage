$('button').click(function () {
    console.log(1);
    $("#datatable").table2excel({
        exclude: ".noExl",
        name: "Excel Document Name",
        filename: "治具统计表",
        exclude_img: true,
        exclude_links: true,
        exclude_inputs: true
    });
});


//      table2excel插件的可用配置参数有：
//
//            exclude：不被导出的表格行的CSS class类。
//            name：导出的Excel文档的名称。
//            filename：Excel文件的名称。
//            exclude_img：是否导出图片。
//            exclude_links：是否导出超链接
//            exclude_inputs：是否导出输入框中的内容。

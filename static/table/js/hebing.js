/**
 * 合并行
 * @param data  原始数据（应在服务端完成排序）
 * @param fieldName 合并属性名称数组
 * @param colspan 列数
 * @param target 目标表格对象
 * @param upperLevelFieldname 该字段上一级的字段集合（合并格数不能超过上一字段）
 */
function mergeCells(data, fieldName, colspan, target,upperLevelFieldnameList) {
    if (data.length == 0) {
        return;
    }
    //初始化upperFieldValueList
    var upperFieldValueList=[];
    upperLevelFieldnameList.forEach(function (item) {
        upperFieldValueList.push(data[0][item]);
    })
    data.push({"GDSTITLE":"","NAME2":"","NAME1":"","CATALOGNAME":""});//主要是给数据增加一行解决底部合并问题
    var numArr = [];
    var value = data[0][fieldName];
    var num = 0;
    for (var i = 0; i < data.length; i++) {debugger
        if ((value != data[i][fieldName])|doCheck(data[i],upperLevelFieldnameList)) {
            numArr.push(num);
            value = data[i][fieldName];
            num = 1;
            continue;
        }
        num++;
    }
    var merIndex = 0;
    for (var i = 0; i < numArr.length; i++) {
        $(target).bootstrapTable('mergeCells', { index: merIndex, field: fieldName, colspan: colspan, rowspan: numArr[i] })
        merIndex += numArr[i];
    }

    //用于检查是否相同，相同返回false不相同更新父类并返回true
    function doCheck(item,upperLevelFieldnameList) {
        var log=false;
        upperLevelFieldnameList.forEach(function (value,index) {
            if(upperFieldValueList[index] !=item[value]){
                log=true;
                upperFieldValueList[index]=item[value]
            };
        })
        return log;
    }
}
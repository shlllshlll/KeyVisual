/*
 * @Author: SHLLL
 * @Email: shlll7347@gmail.com
 * @Date:   2018-04-22 15:52:16
 * @Last Modified by:   SHLLL
 * @Last Modified time: 2018-04-22 23:53:23
 * @License: MIT LICENSE
 */
// 将所有的函数功能封装到一个匿名函数中，并将其暴露在table命名空间中
(function(table, $) {
    "use strict";

    var resultTable = $("#result-table"); // 获取DOM中table表格
    var tableHead = resultTable.find("thead>tr"); //选取表格头
    var tableBody = resultTable.find("tbody");

    var dataResult = null;
    var displayCount = 15;

    var nPageCount = null;
    var nPageCurrent = 1;
    var nNavDom = $(".pagination");
    var nNavList = [];

    function setTableHead(tableName) {
        tableHead.empty() // 首先删除所有的子元素

        tableHead.append("<th scope='col'>#</th>");
        for (var count in tableName) {
            var th = $("<th scope='col'></th>");
            th.text(tableName[count]);
            tableHead.append(th);
        }
    }

    function setTableBody(data) {
        tableBody.empty();

        for (var count = 0; count < Math.min(displayCount, data.length); count++) {
            // 新建一行
            var tr = $("<tr></tr>");
            tableBody.append(tr);

            // 插入行号
            var th = $("<th scope='row'></th>");
            th.text(data[count].pk);
            tableBody.append(th);

            // 插入新闻标题超链接
            var title = $("<td></td>");
            var url = $("<a></a>");
            url.attr("href", data[count].fields.url);
            url.text(data[count].fields.title.substring(0, 10) + "...");
            title.append(url);
            tableBody.append(title);

            // 插入发布日期
            var date = $("<td></td>");
            date.text(data[count].fields.datee);
            tableBody.append(date);

            // 插入新闻内容
            var news = $("<td></td>");
            news.text(data[count].fields.news.substring(0, 40) + "...");
            tableBody.append(news);
        }
    }

    function ajaxGetJson(data) {
        // 将JSON字符串转换为JSON对象
        data = JSON.parse(data);
        setTableBody(data);
    }

    /**
     * Navigation link clicked callback.
     * @return {undefined} null.
     */
    function navgateClick() {
        // 获取当前访问的是第几页
        var pageNum = parseInt($(this).text());
        var startCount = displayCount * (pageNum - 1);
        var endCount = displayCount * pageNum;

        // 更改页码显示
        nNavDom.children().removeClass("active");
        $(this).addClass("active");

        // 向django服务器发送ajax请求
        var url = startCount + "/" + endCount;
        $.getJSON(url, ajaxGetJson)
    }

    function initNavgate() {
        // 计算一共有多少页
        nPageCount = Math.ceil(dataResult.len / displayCount);

        for (var count = 1; count <= nPageCount; count++) {
            var a = $('<a class="page-link" href="javascript:void(0)"></a>');
            a.text(count);
            var li = $('<li class="page-item"></li>');
            li.append(a);
            nNavDom.append(li);
            li.click(navgateClick);
            nNavList.push(li);
        }

        nNavList[0].addClass("active")
        nPageCurrent = 1;
    }

    table.init = function(result) {
        // 初始化result
        dataResult = result;

        // 初始化页码导航
        initNavgate();

        // 初始化表格的标题
        setTableHead(result.title);

        // 初始化表格内容
        setTableBody(result.data);

    };

}(window.table = window.table || {}, jQuery));

(function(table, dataResult) {
    var title = ["标题", "发布日期", "新闻"];
    var result = { data: dataResult, title: title, len: dataLen };
    // 初始化表格
    table.init(result)
}(table, dataResult));

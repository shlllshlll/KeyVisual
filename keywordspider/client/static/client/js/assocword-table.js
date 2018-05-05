/*
 * @Author: SHLLL
 * @Email: shlll7347@gmail.com
 * @Date:   2018-04-24 22:13:19
 * @Last Modified by:   SHLLL
 * @Last Modified time: 2018-04-29 21:06:33
 * @License: MIT LICENSE
 */

class AssocwordTable extends BaseTable {
    constructor(content) {
        super(content); // 调用父类的初始化方法
        this.curActiveTab = "freq"; // 设置当前激活的标签页
        this.curDisplay = content.display;
    }

    initDom() {
        super.initDom();
        this.tableRow.css('margin-top', '1em');

        const navTabDom = $('<nav class="nav nav-pills justify-content-center"></nav>');
        const navTabItem1 = $('<a class="nav-link active"  data-toggle="pill" tab-name="freq" href="javascript:void(0)">频繁项</a>')
        const navTabItem2 = $('<a class="nav-link"  data-toggle="pill" tab-name="assoc" href="javascript:void(0)">关联规则</a>')
        navTabDom.css('margin-top', '2em');
        navTabDom.append(navTabItem1);
        navTabDom.append(navTabItem2);
        this.navTabDom = navTabDom;

        this.containDom.prepend(navTabDom);
    }

    setTableBody(data, display) {
        this.tableBody.empty();

        for (let count = 0; count < Math.min(this.displayCount, data.length); count++) {
            // 新建一行
            const tr = $("<tr></tr>");
            this.tableBody.append(tr);

            // 插入行号
            const th = $("<th scope='row'></th>");
            th.text(data[count].pk);
            tr.append(th);

            for (let index = 0; index < display.length; index++) {
                const node = $("<td></td>");
                node.text(data[count].fields[display[index]]);
                tr.append(node);
            }
        }
    }

    initNavTab(){
        this.navTabDom.find('a').on('show.bs.tab', e=>{
            const curTab = $(e.target);
            const lastTab = $(e.relatedTarget);
            curTab.addClass('activate');
            lastTab.removeClass('activate');
            this.curActiveTab = curTab.attr('tab-name');
            const url = 'len/' + this.curActiveTab;
            $.getJSON(url, data => {
                this.pageCount = Math.ceil(data.len / this.displayCount);
                this.curDisplay = data.display;
                this.setTableHead(data.title, data.width);
                this.initNavgate();
                // 定义ajax回调方法
                $.getJSON(this.curActiveTab + "/0/" + this.displayCount, data => {
                    // 将JSON字符串转换为JSON对象
                    data = JSON.parse(data);
                    this.setTableBody(data, this.curDisplay);
                });
                this.setTableBody(this.dataResult.data, this.curDisplay);
            });
        })
    }

    initNavgate() {
        // 根据页码数创建页码
        this.navDom.empty();
        this.navList.length = 0;
        for (let count = 1; count <= this.pageCount; count++) {
            const a = $('<a class="page-link" href="javascript:void(0)"></a>');
            a.text(count);
            const li = $('<li class="page-item"></li>');
            li.append(a);
            this.navDom.append(li);

            // 为当前this创建别名以供匿名函数使用
            // 定义click回调方法
            li.click(e => {
                const currentDom = e.currentTarget;
                // 获取当前访问的是第几页
                const pageNum = parseInt($(currentDom).text());
                const startCount = this.displayCount * (pageNum - 1);
                const endCount = this.displayCount * pageNum;

                // 更改页码显示
                this.navDom.children().removeClass("active");
                $(currentDom).addClass("active");

                // 向django服务器发送ajax请求
                const url = this.curActiveTab + "/" + startCount + "/" + endCount;
                // 定义ajax回调方法
                $.getJSON(url, data => {
                    // 将JSON字符串转换为JSON对象
                    data = JSON.parse(data);
                    this.setTableBody(data, this.curDisplay);
                });
            });
            this.navList.push(li);
        }

        this.navList[0].addClass("active")
    }

    init() {
        // 初始化标签页导航
        this.initNavTab();
        // 初始化页码导航
        this.initNavgate();
        // 初始化表格的标题
        this.setTableHead(this.dataResult.title, this.dataResult.width);
        // 定义ajax回调方法
        $.getJSON(this.curActiveTab + "/0/" + this.displayCount, data => {
            // 将JSON字符串转换为JSON对象
            data = JSON.parse(data);
            this.setTableBody(data, this.curDisplay);
        })
    }
}

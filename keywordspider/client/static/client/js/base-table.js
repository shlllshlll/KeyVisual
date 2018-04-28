/*
 * @Author: SHLLL
 * @Email: shlll7347@gmail.com
 * @Date:   2018-04-23 18:57:58
 * @Last Modified by:   SHLLL
 * @Last Modified time: 2018-04-28 21:19:43
 * @License: MIT LICENSE
 */
/**
 * 定义一个BaseTable类
 * @param  {object} content 传递要显示的表格数据
 */
class BaseTable {
    /**
     * BaseTable类构造函数
     * @param  {object} content 传递要显示的表格数据
     * @return {undefined}      None.
     */
    constructor(content) {
        this.dataResult = content;
        this.displayCount = 15;
        this.pageCount = Math.ceil(content.len / this.displayCount);

        this.navDom = $(".pagination");
        this.navList = [];

        const resultTable = $("#result-table");
        this.tableHead = resultTable.find("thead>tr"); //选取表格头
        this.tableBody = resultTable.find("tbody");
    }

    initNavgate() {
        // 根据页码数创建页码
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
                const url = startCount + "/" + endCount;
                // 定义ajax回调方法
                $.getJSON(url, data => {
                    // 将JSON字符串转换为JSON对象
                    // data = JSON.parse(data);
                    this.setTableBody(data);
                })
            });
            this.navList.push(li);
        }

        this.navList[0].addClass("active")
    }

    setTableHead(tableName) {
        this.tableHead.empty() // 首先删除所有的子元素

        this.tableHead.append("<th scope='col'>#</th>");
        for (let count in tableName) {
            const th = $("<th scope='col'></th>");
            th.text(tableName[count]);
            this.tableHead.append(th);
        }
    }

}

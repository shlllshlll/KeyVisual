/*
 * @Author: SHLLL
 * @Email: shlll7347@gmail.com
 * @Date:   2018-04-23 18:57:58
 * @Last Modified by:   SHLLL
 * @Last Modified time: 2018-05-22 23:50:32
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

        this.initDom();
    }

    initDom() {
        const containDom = $("main.container"); // 选取container根节点

        const tableRow = $('<div class="row""></div>');
        const tableCol = $('<div class="col table-striped"></div>');
        const tableDom = $('<table class="table table-hover" id="result-table"></table>');
        const tableHead = $('<thead></thead>');
        const tableHeadTr = $('<tr class="table-info"></tr>');
        const tableBody = $('<tbody></tbody>');
        tableRow.css('margin-top', '2em');
        tableHead.append(tableHeadTr);
        tableDom.append(tableHead);
        tableDom.append(tableBody);
        tableCol.append(tableDom);
        tableRow.append(tableCol);
        this.tableHead = tableHeadTr;
        this.tableBody = tableBody;
        this.tableRow = tableRow;

        const navContain = $('<div id="pagination"></div>');
        this.navDom = navContain;

        containDom.append(tableRow);
        containDom.append(navContain);
        this.containDom = containDom;
    }

    initNavgate(baseurl='', getJsonFunc = null) {
        $('#pagination').twbsPagination({
            totalPages: this.pageCount,
            visiblePages: 5,
            onPageClick: (event, page) => {
                const startCount = this.displayCount * (page - 1);
                const endCount = this.displayCount * page;
                // 向django服务器发送ajax请求
                const url = baseurl + startCount + "/" + endCount;

                if(getJsonFunc) {
                    getJsonFunc.call(this, url);
                } else {
                    // 定义ajax回调方法
                    $.getJSON(url, data => {
                        // 将JSON字符串转换为JSON对象
                        data = JSON.parse(data);
                        this.setTableBody(data);
                    });
                }
            },
            paginationClass: 'pagination justify-content-end',
            first: '首页',
            prev: '前一页',
            next: '下一页',
            last: '尾页',
        });
    }

    setTableHead(tableName, tableWidth = null) {
        this.tableHead.empty(); // 首先删除所有的子元素

        for (let count in tableName) {
            const th = $("<th scope='col'></th>");
            th.text(tableName[count]);
            if (tableWidth) {
                th.css("width", tableWidth[count]);
            }
            this.tableHead.append(th);
        }
    }

    init() {
        // 初始化页码导航
        this.initNavgate();

        // 初始化表格的标题
        this.setTableHead(this.dataResult.title, this.dataResult.width);

        // 定义ajax回调方法
        $.getJSON("0/" + this.displayCount, data => {
            // 将JSON字符串转换为JSON对象
            data = JSON.parse(data);
            this.setTableBody(data);
        });
    }

}

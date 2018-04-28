/*
* @Author: SHLLL
* @Email: shlll7347@gmail.com
* @Date:   2018-04-24 22:13:19
* @Last Modified by:   SHLLL
* @Last Modified time: 2018-04-25 01:09:02
* @License: MIT LICENSE
*/

class KeywordTable extends BaseTable {
    constructor(content){
        super(content);   // 调用父类的初始化方法
    }

    setTableBody(data) {
        this.tableBody.empty();

        for (let count = 0; count < Math.min(this.displayCount, data.length); count++) {
            // 新建一行
            const tr = $("<tr></tr>");
            this.tableBody.append(tr);

            // 插入行号
            const th = $("<th scope='row'></th>");
            th.text(data[count].pk);
            this.tableBody.append(th);

            // 插入新闻标题超链接
            const title = $("<td></td>");
            const url = $("<a></a>");
            url.attr("href", data[count].fields.url);
            url.text(data[count].fields.title.substring(0, 10) + "...");
            title.append(url);
            this.tableBody.append(title);

            // 插入发布日期
            const date = $("<td></td>");
            date.text(data[count].fields.keywords);
            this.tableBody.append(date);
        }
    }

    init(){
        // 初始化页码导航
        this.initNavgate();

        // 初始化表格的标题
        this.setTableHead(this.dataResult.title);

        // 初始化表格内容
        this.setTableBody(this.dataResult.data);

    }
}

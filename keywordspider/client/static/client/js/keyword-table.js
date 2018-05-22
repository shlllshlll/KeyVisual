/*
* @Author: SHLLL
* @Email: shlll7347@gmail.com
* @Date:   2018-04-24 22:13:19
* @Last Modified by:   SHLLL
* @Last Modified time: 2018-05-22 21:28:10
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
            tr.append(th);

            // 插入新闻标题超链接
            const title = $("<td></td>");
            const url = $("<a></a>");
            url.attr("href", data[count].fields.url);
            url.text(data[count].fields.title.substring(0, 10) + "...");
            title.append(url);
            tr.append(title);

            // 插入关键词
            const date = $("<td></td>");
            const keywordAry = data[count].fields.keywords.split('/');   // 分割字符串
            for (let keyword of keywordAry) {
                const keywordBadge = $("<span class='badge badge-primary'></span>");
                keywordBadge.text(keyword);
                keywordBadge.css("margin-left", "0.5rem");
                date.append(keywordBadge);
            }
            tr.append(date);
        }
    }
}

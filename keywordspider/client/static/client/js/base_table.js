/*
 * @Author: SHLLL
 * @Email: shlll7347@gmail.com
 * @Date:   2018-04-23 18:57:58
 * @Last Modified by:   SHLLL
 * @Last Modified time: 2018-04-23 20:44:11
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
        this.content = content;
        let resultTable = $("#result-table");
        var tableHead = resultTable.find("thead>tr"); //选取表格头
        var tableBody = resultTable.find("tbody");
    }
}

/*
* @Author: SHLLL
* @Email: shlll7347@gmail.com
* @Date:   2018-05-09 17:49:05
* @Last Modified by:   SHLLL
* @Last Modified time: 2018-05-10 18:06:36
* @License: MIT LICENSE
*/
"use strict";

function init() {
    function removeAltert(message) {
        $(".alert").remove();   // 删除Altert
    }

    function addAlert(message) {
        const html = '<div class="alert alert-danger fade show" role="alert">'+message+
        `<button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
        </button></div>`;
        const alert = $(html);
        alert.css("marginTop", "20px");
        $(".alert").remove();   // 首先删除先前的Alert
        $("main").prepend(alert);
        document.documentElement.scrollTop = 0;
    }

    function initProcess() {
        // 获取circle JQuery对象
        const circle1 = $('#circle1');
        // const string1 = circle1.find('strong').contents()[0];
        const circle2 = $('#circle2');
        // const string2 = circle2.find('strong').contents()[0];
        const circle3 = $('#circle3');
        // const string3 = circle3.find('strong').contents()[0];

        circle1.circleProgress({
            lineCap: "round",
            value: 0.75,
            size: 200,
            fill: "#ff1e41"
        });

        circle2.circleProgress({
            lineCap: "round",
            value: 0.75,
            size: 200,
            fill: "#F94FE5"
        });

        circle3.circleProgress({
            lineCap: "round",
            value: 0.75,
            size: 200,
            fill: "#40E0D0"
        });
    }

    initProcess();
    $("#ctr-btn").click(()=>{
        // 首先构建一个JSON对象表单
        const postData = {
            saveMethod: $("#datacsv").prop("checked")?"csv":$("#datamysql").prop("checked")?"mysql":null,
            targetWebsite: $("#targetWebsite").val(),
            runSpider: $("#spiderCheckbox").prop("checked"),
            runKeyword: $("#keywordCheckbox").prop("checked"),
            runAssoword: $("#assowordCheckbox").prop("checked"),
            spiderNum: $("#spiderNum").val(),
            minSupp: $("#minSupp").val(),
            minConf: $("#minConf").val()
        };

        // 检查表单中的数据是否正确
        if(!postData.saveMethod) {
            addAlert("请至少选择一个数据存储方式");
            return;
        } else if(!postData.runSpider && !postData.runKeyword && !postData.runAssoword) {
            addAlert("请至少选择一个功能组件");
            return;
        } else {
            removeAltert();
        }

        $.post("post/", postData, data=>{
            console.log(data);
        })
    })
}

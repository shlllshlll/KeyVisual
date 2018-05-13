/*
* @Author: SHLLL
* @Email: shlll7347@gmail.com
* @Date:   2018-05-09 17:49:05
* @Last Modified by:   SHLLL
* @Last Modified time: 2018-05-12 22:12:25
* @License: MIT LICENSE
*/
"use strict";

function init(result) {
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

    function initProcess(result) {
        // 随机获取进度百分比函数
        const getRandom = () => Math.ceil((Math.random() * 0.5 + 0.4) * 100) / 100;
        // 获取circle JQuery对象
        const circle1 = $('#circle1');
        const string1 = circle1.find('strong').contents()[0];
        const circle2 = $('#circle2');
        const string2 = circle2.find('strong').contents()[0];
        const circle3 = $('#circle3');
        const string3 = circle3.find('strong').contents()[0];

        circle1.bind('circle-animation-progress', (event, anProcess, stValue) => {
        string1.nodeValue = Math.ceil(anProcess * result.res_len);
        });
        circle1.bind('circle-animation-end', e=>{
            string1.nodeValue =result.res_len;
        });
        circle1.circleProgress({
            lineCap: "round",
            value: getRandom(),
            size: 200,
            fill: "#ff1e41"
        });

        circle2.bind('circle-animation-progress', (event, anProcess, stValue) => {
            string2.nodeValue = Math.ceil(anProcess * result.key_len);
        });

        circle2.bind('circle-animation-end', e=>{
            string2.nodeValue =result.key_len;
        });
        circle2.circleProgress({
            lineCap: "round",
            value: getRandom(),
            size: 200,
            fill: "#F94FE5"
        });


        circle3.bind('circle-animation-progress', (event, anProcess, stValue) => {
            string3.nodeValue = Math.ceil(anProcess * result.conf_len);
        });
        circle3.bind('circle-animation-end', e=>{
            string3.nodeValue =result.conf_len;
        });
        circle3.circleProgress({
            lineCap: "round",
            value: getRandom(),
            size: 200,
            fill: "#40E0D0"
        });
    }

    $.fn.extend({setProgressbar: function(value, animated){
        if(animated && !this.hasClass('progress-bar-animated')){
            this.addClass('progress-bar-animated');
        } else if(!animated && this.hasClass('progress-bar-animated')) {
            this.removeClass('progress-bar-animated');
        }
        // 对value限制幅度
        value = value > 100 ? 100 : value < 0 ? 0 : value;
        this.attr('aria-valuenow', value);
        this.css('width', value+'%');
    }});

    initProcess(result);
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

        $.post("post/", postData, ()=>{
            const spiderProgress = $("#spiderProgress");
            const keywordProgress = $("#keywordProgress");
            const assowordProgress = $("#assowordProgress");

            spiderProgress.setProgressbar(0, true);
            keywordProgress.setProgressbar(0, true);
            assowordProgress.setProgressbar(0, true);
            (function fresh(){
                $.getJSON("status/", data=>{
                    spiderProgress.setProgressbar(100*data.spider, data.spider<2?true:false);
                    keywordProgress.setProgressbar(100*data.keyword, data.keyword<2?true:false);
                    assowordProgress.setProgressbar(100*data.assoword, data.assoword<2?true:false);
                    console.log(data);
                    if(data.running !== 2){
                        setTimeout(fresh, 500);
                    }
                });
            })();
        })
    })
}

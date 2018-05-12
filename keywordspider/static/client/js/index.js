/*
 * @Author: SHLLL
 * @Email: shlll7347@gmail.com
 * @Date:   2018-05-06 16:24:34
 * @Last Modified by:   SHLLL
 * @Last Modified time: 2018-05-07 17:13:01
 * @License: MIT LICENSE
 */

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

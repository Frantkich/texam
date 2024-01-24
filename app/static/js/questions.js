"use strict";
console.log('exam_active.js loaded');

function uncollapseQuestionList() {
    $("#questions").toggle("collapse multi-collapse");
}
uncollapseQuestionList();

function noInputSelected() {
    $("select").attr("disabled", true);
}
noInputSelected();

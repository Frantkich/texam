"use strict";
console.log('exam_active.js loaded');

import { custom_alert } from './script.js';
import { saveAnswers } from './save_answers_export.js';


$("#submit").on("click", function () {
    if (window.confirm("The exam will be submitted, you can't do anything after that, do you want to proceed ?")) {
        $(this).prop("disabled", true);
        $(this).html(`<span class="spinner spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ${$(this).text()}`);
        saveAnswers().then(response => {
            $.ajax({
                url: "submit",
                type: "POST",
                success: (data) => {
                    window.location.href = `/results/${data.result_id}`;
                },
                complete: (data) => {
                    custom_alert(data);
                    $(this).find(".spinner").remove();
                    $(this).prop("disabled", false);
                }
            });
        });
    }
});

$("#answer").on("click", function () {
    if (window.confirm("Your answers will be saved and submit to TLC, do you want to proceed ?")) {
        $(this).prop("disabled", true);
        $(this).html(`<span class="spinner spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ${$(this).text()}`);
        saveAnswers().then(response => {
            $.ajax({
                url: "answers/submit",
                type: "POST",
                complete: (data) => {
                    $(this).find(".spinner").remove();
                    $(this).prop("disabled", false);
                    custom_alert(data, 10000)
                }
            });
        });
    }
});

function uncollapseQuestionList() {
    $("#questions").toggle("collapse multi-collapse");
}
uncollapseQuestionList();

function toggleAllQuestion() {
    $(".questionCollapseButton").click();
}
toggleAllQuestion();

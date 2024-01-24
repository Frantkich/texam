"use strict";
console.log('exam_active.js loaded');

import { custom_alert, get_base_url, toggle_button_loading } from './script.js';
import { saveAnswers } from './save_answers_export.js';


function sendAnswers() {
    return $.ajax({
        url: `${get_base_url()}/exams/active/submit/answers`,
        type: "POST",
        complete: (data) => {
            toggle_button_loading($("#sendAnswers"));
            custom_alert(data.responseJSON, 10000)
        }
    });
}

$("#saveAnswers").on("click", function() {
    toggle_button_loading($(this));
    saveAnswers();
});


$("#sendAnswers").on("click", function() {
    if (window.confirm("Your answers will be saved and submit to TLC, do you want to proceed ?")) {
        toggle_button_loading($("#saveAnswers"));
        toggle_button_loading($(this));
        saveAnswers().then( () => { sendAnswers(); });
    }
});


$("#submit_now").on("click", function() {
    if (window.confirm("The exam will be submitted, you can't do anything after that, do you want to proceed ?")) {
        $("#submit").click()
        toggle_button_loading($("#saveAnswers"));
        toggle_button_loading($("#sendAnswers"));
        toggle_button_loading($("#submit"));
        saveAnswers().then( () => {
            sendAnswers().then( () => {
                $.ajax({
                    url: `${get_base_url()}/exams/active/submit/exam`,
                    type: "POST",
                    success: (data) => {
                        window.location.href = `texam/results/${data.result_id}`;
                    },
                    error: (data) => {
                        custom_alert(data.responseJSON);
                        toggle_button_loading($("#submit"));
                    }
                });
            });
        });
    }
});


$("#submit_delay").on("click", function () {
    if (window.confirm("The exam will be submitted, you can't do anything after that, do you want to proceed ?")) {
        $("#submit").click()
        toggle_button_loading($("#saveAnswers"));
        toggle_button_loading($("#sendAnswers"));
        toggle_button_loading($("#submit"));
        saveAnswers().then( () => {
            sendAnswers().then( () => {
                $.ajax({
                    url: `${get_base_url()}/exams/active/submit/exam/${$("#submit_delay_count").val()}`,
                    type: "POST",
                    complete: (data) => {
                        custom_alert(data.responseJSON);
                        toggle_button_loading($("#submit"));
                    },
                });
            });
        });
    }
});

// uncollapse question list by default 
function uncollapseQuestionList() {
    $("#questions").toggle("collapse multi-collapse");
}
uncollapseQuestionList();

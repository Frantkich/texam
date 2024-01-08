"use strict";
console.log('exam_active.js loaded');

import { custom_alert } from './script.js';

$("#submit").on("click", () => {
    if (window.confirm("The exam will be submitted, you can't do anything after that, do you want to proceed ?")) {
        saveAnswers().then(response => {
            $.ajax({
                url: "submit",
                type: "POST",
                success: (data) => {
                    window.location.href = `/results/${data.result_id}`;
                },
                complete: (data) => {custom_alert(data)}
            });
        });
    }
});

$("#answer").on("click", () => {
    if (window.confirm("Your answers will be saved and submit to TLC, do you want to proceed ?")) {
        saveAnswers().then(response => {
            $.ajax({
                url: "answers/submit",
                type: "POST",
                complete: (data) => {custom_alert(data, 10000)}
            });
        });
    }
});

// TO UPDATE IN app\static\js\exam.js
function saveAnswers() {
    let questions = [];
    $(".question").each((index, question) => {
        let answers = [];
        $(question).find(".answer").each((index, answer) => {
            answers.push(Object({
                id: $(answer).find(".answerRemarks").attr("id").split("_")[1],
                description: $(answer).find(".answerDesc").text().trim(),
                score: $(answer).find(".answerScore").val(),
                remarks: $(answer).find(".answerRemarks").val()
            }));
        });
        questions.push(Object({
            id: $(question).find(".answerList").attr("id").split("_")[1],
            description: $(question).find(".questionDesc").text().trim(),
            answers: answers
        }));
    });
    let examData = Object({
        code: $("#examCode").text().trim(),
        questions: questions
    })
    return $.ajax({
        url: "answers/save",
        type: "UPDATE",
        data: JSON.stringify(examData),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        complete: (data) => {custom_alert(data)}
    });
}

function uncollapseQuestionList() {
    $("#questions").toggle("collapse multi-collapse");
}
uncollapseQuestionList();

function toggleAllQuestion() {
    $(".questionCollapseButton").click();
}
toggleAllQuestion();

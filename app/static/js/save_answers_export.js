"use strict";
console.log('save_answers_export.js loaded');

import { custom_alert, get_base_url, toggle_button_loading } from './script.js';

export { saveAnswers };


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
        name: $("#examName").text(),
        questions: questions
    })
    return $.ajax({
        url: `${get_base_url()}/exams/answers/save`,
        type: "UPDATE",
        data: JSON.stringify(examData),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        complete: (data) => {        
            custom_alert(data.responseJSON)
            toggle_button_loading($("#saveAnswers"));
        }
    });
}

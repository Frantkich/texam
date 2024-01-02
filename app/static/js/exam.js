"use strict";
console.log('exam.js loaded');

/**
 * Event handler for the "Save Answers" button click.
 * Collects the answers from the questions on the page and sends them to the server.
 */
$("#saveAnswers").on("click", () => {
    saveAnswers();
});

// TO UPDATE IN app\static\js\exam_active.js
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
        url: "answers",
        type: "POST",
        data: JSON.stringify(examData),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: (data) => {
            if (data.status != "success") {
                alert("Error: " + data.message);
            }
        },
        error: (error) => { console.log(error); }
    });
}
$("#fetchNewQuestions").on("click", () => {
    let examCode = $("#examCode").text().trim();
    if (window.confirm("Are you sure ?")) {
        $.ajax({
            url: "fetchNewQuestions/" + examCode,
            type: "UPDATE",
            success: (data) => {
                if (data.status == "success") {
                    location.reload();
                } else {
                    alert("Error: " + data.message);
                }
            },
            error: (error) => { console.log(error); }
        });
    }
});

$("#startExam").on("click", () => {
    let examCode = $("#examCode").text().trim();
    if (window.confirm("Are you sure ?")) {
        $.ajax({
            url: "start/" + examCode,
            type: "POST",
            success: (data) => {
                if (data.status == "success") {
                    location.href = "active";
                } else {
                    alert("Error: " + data.message);
                }
            },
            error: (error) => { console.log(error); }
        });
    }
});

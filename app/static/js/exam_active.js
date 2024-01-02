"use strict";
console.log('exam_active.js loaded');


$("#submit").on("click", () => {
    if (window.confirm("The exam will be submitted, you can't do anything after that, do you want to proceed ?")) {
        saveAnswers().then(response => {
            $.ajax({
                url: "submit",
                type: "POST",
                success: (data) => {
                    if (data.status == "success") {
                        window.location.href = `active?end=${$("#examCode").text().trim()}`;
                    } else {
                        alert("Error: " + data.message);
                    }
                },
                error: (error) => { console.log(error); }
            });
        });
    }
});

$("#answer").on("click", () => {
    if (window.confirm("Your answers will be saved and submit to TLC, do you want to proceed ?")) {
        saveAnswers().then(response => {
            $.ajax({
                url: "submitAnswers",
                type: "POST",
                success: (data) => {
                    console.log(data);
                },
                error: (error) => { console.log(error); }
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
    console.log(examData)
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

function uncollapseQuestionList() {
    $("#questions").toggle("collapse multi-collapse");
}
uncollapseQuestionList();

function toggleAllQuestion() {
    $(".questionCollapseButton").click();
}
toggleAllQuestion();

console.log('exam.js loaded');

/**
 * Event handler for the "Save Answers" button click.
 * Collects the answers from the questions on the page and sends them to the server.
 */
$("#saveAnswers").on("click", () => {
    let questions = [];
    $(".question").each((index, question) => {
        answers = [];
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
    $.ajax({
        url: "/exam/answers",
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
});

/**
 * Event handler for the input event on the answer score input field.
 * Ensures that the entered score is within the specified range.
 */
$(".answerScore").on("input", function() {
    let score = parseInt($(this).val());
    let max = parseInt($(this).attr("max"));
    let min = parseInt($(this).attr("min"));
    if (score < min ) {score = min;}
    if (score > max ) {score = max;} 
    $(this).val(score);
    if (score == max) {
        console.log("remarks_" + $(this).attr("answer_id"))
        let remarks = $("#remarks_" + $(this).attr("answer_id"))
        if ( remarks.text().trim() == "" ) {
            alert("Don't forget to add remarks to justify yourself!");
            remarks.prev().find(".bi-chevron-bar-down").click();
        }
    }
});


$("#fetchNewQuestions").on("click", () => {
    let examCode = $("#examCode").text().trim();
    if (window.confirm("Are you sure ?")) {
        $.ajax({
            url: "/exam/fetchNewQuestions/" + examCode,
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

$(".bi-chevron-bar-down").on("click", function() {
    $(this).toggleClass("bi-chevron-bar-up");
    $(this).toggleClass("bi-chevron-bar-down");
});

function uncollapseRemarks() {
    $(".answerRemarks").each((index, answerRemarks) => {
        if ($(answerRemarks).val().trim() != "") {
            $(answerRemarks).prev().find(".bi-chevron-bar-down").click();
        }
    });
}
uncollapseRemarks();

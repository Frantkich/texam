"use strict";
console.log('exam_questions.js loaded');

$(".answerScore").on("input", function() {
    if ($(this).val() == 3) {
        let remarks = $("#remarks_"+$(this).attr("id"))
        if ( remarks.val() == "" ) {
            alert("Don't forget to add remarks to justify yourself!");
            remarks.prev().find(".bi-chevron-bar-down").click();
        }
    }
});

function selectSelections() {
    $(".answerScore").each((index, answerScore) => {
        let score = $(answerScore).attr("value");
        $(answerScore).find("option").each((index, option) => {
            if ($(option).val() == score) {
                $(option).attr("selected", true);
            }
        });
    });
}
selectSelections();

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

"use strict";
console.log('questions_list.js loaded');


$(".answerScore").on("input", function() {
    if ($(this).val() == 2 || $(this).val() == 3) {
        let no_occ = 0;
        $(this).parent().parent().parent().parent().parent().find("li").each((index, li) => {
            if ($(li).find(".answerScore").val() == $(this).val() && $(li).find(".answerScore") != $(this)) {
                alert(`You can't have two answers "${$(this).find("option:selected").text()}" !`);
                $(li).find(".answerScore").val(null);
            }
        });
    }
    if ($(this).val() == 3) {
        let remarks = $("#remarks_"+$(this).attr("id"))
        if ( remarks.val() == "" ) {
            remarks.prev().find(".bi-chevron-bar-down").click();
        }
    }
});


$(".bi-chevron-bar-up").on("click", function() {toggle_chevron($(this));});
$(".bi-chevron-bar-down").on("click", function() {toggle_chevron($(this));});

function toggle_chevron(el) {
    el.toggleClass("bi-chevron-bar-up");
    el.toggleClass("bi-chevron-bar-down");
}

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


function uncollapseRemarks_if_not_null() {
    $(".answerRemarks").each((index, answerRemarks) => {
        if ($(answerRemarks).val().trim() != "") {
            $(answerRemarks).prev().find(".bi-chevron-bar-down").click();
        }
    });
}
uncollapseRemarks_if_not_null();

function uncollapseQuestions() {
    $(".question").each((index, question) => {
        let validated = false;
        $(question).find(".answerScore").each((index, answerScore) => {
            if ($(answerScore).val() == 3) {validated = true;}
        });
        if (! validated) {
            $(question).find(".bi-check").hide();
            $(question).find(".questionCollapseButton").click();
        }
    });
}
uncollapseQuestions();

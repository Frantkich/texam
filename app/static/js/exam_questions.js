"use strict";
console.log('exam_questions.js loaded');


$(".answerScore").on("input", function() {
    if ($(this).val() == 2 || $(this).val() == 3) {
        let no_occ = 0;
        $(this).parent().parent().parent().parent().parent().find("li").each((index, li) => {
            if ($(li).find(".answerScore").val() == $(this).val()) {
                no_occ += 1;
                if (no_occ > 1) {
                    alert(`You can't have two answers "${$(this).find("option:selected").text()}" !`);
                    $(li).find(".answerScore").val(null);
                }
            }
        });
    }
    if ($(this).val() == 3) {
        let remarks = $("#remarks_"+$(this).attr("id"))
        if ( remarks.val() == "" ) {
            alert("Don't forget to add remarks to justify yourself!");
            remarks.prev().find(".bi-chevron-bar-down").click();
        }
    }
});


$(".bi-chevron-bar-down").on("click", function() {
    $(this).toggleClass("bi-chevron-bar-up");
    $(this).toggleClass("bi-chevron-bar-down");
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


function uncollapseRemarks() {
    $(".answerRemarks").each((index, answerRemarks) => {
        if ($(answerRemarks).val().trim() != "") {
            $(answerRemarks).prev().find(".bi-chevron-bar-down").click();
        }
    });
}
uncollapseRemarks();

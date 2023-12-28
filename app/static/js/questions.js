// main.js
console.log('questions_index.js loaded');

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
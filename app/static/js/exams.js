"use strict";
console.log('exams_index.js loaded');

$("#searchInput").val("");

$("#searchInput").on("input", function() {
    var selected = $(this).val();
    $("ul li").show();
    $("ul li").filter(function() {
        return $(this).text().toLowerCase().indexOf(selected.toLowerCase()) === -1;
    }).hide();
});


function fetch_exams() { 
    $("#fetch").prop("disabled", true);
    $("#fetch").html(`<span class="spinner spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ${$("#fetch").text()}`);
    $.ajax({
        url: "fetch",
        type: "UPDATE",
        success: (data) => {
            if (data.length) {
                $("#itemList").empty();
                data.forEach((exam) => {
                    $("#itemList").append(`<a href="${ exam.code }"><li class="list-group-item">${ exam.name }</li></a>`);
                });
            } else {
                alert("Error: " + data.message);
            }
        },
        complete: (data) => {
            console.log(data)
            $("#fetch").prop("disabled", false);
            $("#fetch").find(".spinner").remove();
        }
    });
}

$("#fetch").on("click", () => { 
    fetch_exams();
});

fetch_exams();

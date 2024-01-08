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

$("#fetch").on("click", function() { 
    if (confirm("Are you sure?")) {
        $(this).prop("disabled", true);
        $(this).html(`<span class="spinner spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ${$(this).text()}`);
        $.ajax({
            url: "fetch",
            type: "UPDATE",
            success: (data) => {
                if (data.length) {
                    data.forEach((exam) => {
                        $("#itemList").append(`<a href="${ exam.code }"><li class="list-group-item">${ exam.name }</li></a>`);
                    });
                } else {
                    alert("Error: " + data.message);
                }
            },
            complete: (data) => {
                console.log(data)
                $(this).prop("disabled", false);
                $(this).find(".spinner").remove();
            }
        });
    }
});

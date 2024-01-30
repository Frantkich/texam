"use strict";
console.log('exams_index.js loaded');

import { custom_alert, get_base_url, toggle_button_loading } from './script.js';

$("#searchInput").val("");

function filter_exams(search_string) {
    $("#itemList li").filter(function() {
        return $(this).text().toLowerCase().indexOf(search_string.toLowerCase()) === -1;
    }).hide();
}

$("#searchInput").on("input", function() {
    $("#itemList li").show();
    filter_exams($(this).val());
});


function fetch_exams(mode) {
    toggle_button_loading($(`#fetch_${mode}`));
    $.ajax({
        url: `${get_base_url()}/exams/fetch/${mode}`,
        type: "UPDATE",
        success: (data) => {
            if (data.length) {
                $("#itemList").empty();
                data.forEach((exam) => {
                    $("#itemList").append(`<a href="${document.location.pathname}/${ exam.name }"><li class="list-group-item">${ exam.name }</li></a>`);
                });
                filter_exams($("#searchInput").val());
            } else {
                alert("Error: " + data.message);
            }
            custom_alert({ "status": "success", "message": `Fetched ${data.length} exams.`});
        },
        error: (data) => {
            custom_alert(data.responseJSON);
        },
        complete: (data) => {
            toggle_button_loading($(`#fetch_${mode}`));
        }
    });
}

$("#fetch_user").on("click", () => { 
    fetch_exams("user");
});
$("#fetch_all").on("click", () => { 
    fetch_exams("all");
});

fetch_exams("user");


$( "#jf_horse" ).animate({marginLeft: "150%"}, 8000 );
$( "#jf_speed" ).animate({marginLeft: "150%"}, 8000 );

function AnimateRotate(d){
    var elem = $("#jf_horse");
    $({deg: 0}).animate({deg: d}, {
        duration: 150,
        step: function(now){ elem.css({transform: "rotate(" + now + "deg)"})},
        complete: function(){AnimateRotate(d*-1)}
    });
}
AnimateRotate(10);
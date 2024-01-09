"use strict";
console.log('exam.js loaded');

import { custom_alert } from './script.js';
import { saveAnswers } from './save_answers_export.js';

/**
 * Event handler for the "Save Answers" button click.
 * Collects the answers from the questions on the page and sends them to the server.
 */
$("#saveAnswers").on("click", () => {
    saveAnswers();
});

$("#startExam").on("click", function () {
    let examCode = $("#examCode").text().trim();
    if (window.confirm("Are you sure ?")) {
        $(this).prop("disabled", true);
        $(this).html(`<span class="spinner spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ${$(this).text()}`);
        $.ajax({
            url: "start/" + examCode,
            type: "POST",
            success: (data) => {
                if (data.status == "success") {
                    location.href = "active";
                }
            },
            error: (data) => {
                custom_alert(data);
                $(this).prop("disabled", false);
                $(this).find(".spinner").remove();
            },
        });
    }
});

"use strict";
console.log('exam.js loaded');

import { custom_alert, get_base_url, toggle_button_loading } from './script.js';
import { saveAnswers } from './save_answers_export.js';

/**
 * Event handler for the "Save Answers" button click.
 * Collects the answers from the questions on the page and sends them to the server.
 */
$("#saveAnswers").on("click", function() {
    toggle_button_loading($(this));
    saveAnswers();
});

$("#startExam").on("click", function () {
    let exam_name = $("#examName").text().trim();
    if (window.confirm("Are you sure ?")) {
        toggle_button_loading($(this));
        $.ajax({
            url: `${get_base_url()}/exams/start/${exam_name}`,
            type: "POST",
            success: (data) => {
                if (data.status == "success") {
                    location.href = `${get_base_url()}/exams/active`;
                }
            },
            error: (data) => {
                custom_alert(data.responseJSON);
                toggle_button_loading($(this));
            },
        });
    }
});

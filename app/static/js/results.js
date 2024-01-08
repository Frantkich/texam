"use strict";
console.log('results.js loaded');


$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});
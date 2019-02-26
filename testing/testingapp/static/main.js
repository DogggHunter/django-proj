$(document).ready(function() {
    $('.custom_form input[type=text], textarea, select').addClass('form-control');
});

$(function() {
    $(".show-note-form").click(function() {
        $(".note-form").toggleClass("note-form-active");
    })
});
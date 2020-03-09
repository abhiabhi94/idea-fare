'use strict';

$(document).ready(function(event) {
    $('.subForm').submit(subscribe);
    $('.copy').on('click', function(event) {
        event.preventDefault();
        // Check if the request if for a idea or the window
        let text;
        if ($(this).data) {
            text = $(this).data('text');
        } else {
            text = window.location.href;
        }
        // console.log('link:', text);
        const dummy = document.createElement('input');
        $('body').append(dummy);
        dummy.value = text;
        dummy.select();
        // For IE
        if (window.clipboardData) {
            window.clipboardData.setData('Text', text);
        } else {
            document.execCommand('copy');
        }
        $(dummy).remove();
        createResponse('info', 'Link Copied Successfully');
    })
});
/**
 * 
 * @param {event} event - The event that takes place 
 */
function subscribe(event) {
    const responseDiv = $('#sub-response');
    const email = $('#email').val();
    responseDiv.html('Registering ' + email + ' with HackAdda!');
    const url = $(this)[0].action;
    const data = $(this).serialize;
    $.ajax({
        url: url,
        type: 'POST',
        data: $(this).serialize(),
        dataType: 'json',
        // error: function($Xhr, textStatus, errorMessage) {
        // console.log('Error Message:' + errorMessage);
        // },
        complete: function(data) {
            data = data.responseJSON;
            createResponse(data['status'], data['email'] + data['msg']);
            responseDiv.html('');
            if (data['status'] !== -1) {
                email.val('');
            }
        }
    });
    event.preventDefault();
}
/**
 * Create a temporary div, append it to the div'#response', fix it to the top and fade it.
 * @param {int} status - an integer based upon the response received for AJAX request.
 * (-1->'error'|0->'success'| 1->'warning')
 * @param {string} msg - a string depicting the message to be displayed in the response. 
 * @param {int} time - time after which the response fades away
 */
function createResponse(status, msg, time = 2000) {
    switch (status) {
        case -1:
            status = "danger";
            break;
        case 0:
            status = "success";
            break;
        case 1:
            status = "warning";
    }
    const cls = 'alert alert-' + status;
    const response = $('#response');
    const temp = $('<div/>')
        .addClass(cls)
        .html('<div>' + msg + '</div>');
    // console.log(temp);
    response.append(temp);
    fixToTop(temp);
    temp.fadeIn(time);
    temp.fadeOut(2 * time);
    setTimeout(function() {
        temp.remove();
    }, 2 * time + 10);
}
/**
 * Fixes an element to the top of the viewport.
 * @param {element} div - element that is to be fixed at the top of the viewport. 
 */
function fixToTop(div) {
    const isfixed = div.css('position') == 'fixed';
    if (div.scrollTop() > 200 && !isfixed)
        div.css({ 'position': 'fixed', 'top': '0px' });
    if (div.scrollTop < 200 && isfixed)
        div.css({ 'position': 'static', 'top': '0px' });
}
'use strict';

const modal = document.getElementById("report-modal");
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

const btn = document.getElementById("report-button");
btn.onclick = function() {
    modal.style.display = "block";
}

const span = document.getElementById("report-modal-close");
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

const lastFlagReason = document.getElementById('last-flag-reason')

// when the user clicks on the last reason , open the comment box
const flagForm = document.getElementById('report-modal-form');
const flagComment = document.getElementById('report-modal-form-comment');
flagForm.onchange = function(event) {
    if (event.target.value === lastFlagReason.innerHTML) {
        flagComment.required = true;
        flagComment.style.display = "block";
    } else {
        flagComment.style.display = "none";
    }
}
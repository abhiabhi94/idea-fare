'use strict';

let parents = document.getElementsByClassName("report-modal-form-combined");
for (let parent of parents) {
    let modal = parent.querySelector('.flag-report-modal');
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };

    let btn = parent.querySelector(".flag-report-button");
    btn.onclick = function() {
        modal.style.display = "block";
    };

    let span = parent.querySelector(".report-modal-close");
    span.onclick = function() {
        modal.style.display = "none";
    };

    // when the user clicks on the last reason , open the comment box
    let flagForm = parent.querySelector('.report-modal-form');
    let lastFlagReason = flagForm.querySelector('.last-flag-reason');
    let flagComment = flagForm.querySelector('.report-modal-form-comment');
    flagForm.onchange = function(event) {
        if (event.target.value === lastFlagReason.innerHTML) {
            flagComment.required = true;
            flagComment.style.display = "block";
        } else {
            flagComment.style.display = "none";
        }
    };
};

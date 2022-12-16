'use strict';

const $likeForm = $('.like');

/** like: likes or unlikes a warble that is clicked on */
async function like(evt) {
    evt.preventDefault();
    const msgId = evt.target.getAttribute('id');
    const $csrfToken = $(evt.target).find('#csrf_token');

    const fields = {
        csrf_token: $csrfToken.val(),
    }

    const data = JSON.stringify(fields)
    const response = await axios.post(
        `/messages/${msgId}/like`,
        data,
        {headers: {'content-type': 'application/json'}});

    const $icon = $(evt.target).find('i');

    if (response.data === "Success!") {
        $icon.toggleClass('bi-heart-fill bi-heart');
    }

}

$likeForm.on('submit', like);
'use strict';

const $likeForm = $('.like');

/** like: likes or unlikes a warble that is clicked on */
async function like(evt) {
    evt.preventDefault();
    const msg_id = evt.target.getAttribute('id');
    await axios.post(`/messages/${msg_id}/likes`);
    const $icon = $(evt.target).find('i');
    $icon.toggleClass('bi-heart-fill');
    $icon.toggleClass('bi-heart');
}

$likeForm.on('submit', like);
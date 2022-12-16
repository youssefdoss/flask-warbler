'use strict';

const $likeForm = $('.like');
const $messageModal = $('#messageModal')
const $newMessageButton = $('#new-message');
const $newMessageForm = $('#new-message-form');

/** like: likes or unlikes a warble that is clicked on */
async function like(evt) {
    evt.preventDefault();
    const msgId = evt.target.getAttribute('id');
    const $csrfToken = $(evt.target).find('#csrf_token');

    const fields = {
        csrf_token: $csrfToken.val(),
    }

    const response = await axios.post(
        `/messages/${msgId}/like`,
        fields,
        {headers: {'content-type': 'application/json'}});

    const $icon = $(evt.target).find('i');

    if (response.data === "Success!") {
        $icon.toggleClass('bi-heart-fill bi-heart');
    }
}

/** addTweet: Adds a tweet to the database and updates the DOM accordingly */
async function addTweet(evt) {
    evt.preventDefault();
    const $csrfToken = $(evt.target).find('#csrf_token');
    const $text = $(evt.target).find('#text');
    const $location = $(evt.target).find('#location');

    const fields = {
        csrf_token: $csrfToken.val(),
        text: $text.val(),
        location: $location.val()
    }

    await axios.post(
        '/messages/new',
        fields,
        {headers: {'content-type': 'application/json'}}
    );
}

$newMessageButton.on('click', function () {
    $messageModal.modal('show');
});

$likeForm.on('submit', like);
$newMessageForm.on('submit', addTweet);
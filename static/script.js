'use strict';

const $likeForm = $('.like');
const $messageModal = $('#messageModal')
const $newMessageButton = $('#new-message');
const $newMessageForm = $('#new-message-form');
const $messages = $('#messages');
const $nav = $('nav');

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

    const response = await axios.post(
        '/messages/new',
        fields,
        {headers: {'content-type': 'application/json'}}
    );
    const msg = response.data.msg;
    const user = response.data.user;
    const date = new Date(msg.timestamp);
    const months = ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December']

    if (response.data.modify_DOM === true) {
        const $newMessage = $(`<li class="list-group-item">
        <a href="/messages/${ msg.id }" class="message-link"/>
        <a href="/users/${ msg.user_id }">
          <img src="${ user.image_url }" alt="" class="timeline-image">
        </a>
        <div class="message-area">
          <a href="/users/"${ msg.user_id }">@${ user.username }</a>
          <span class="text-muted">${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}</span>
          <p>${ msg.text }</p>
        </div>
      </li>`);
        $messages.prepend($newMessage);

    }

    $messageModal.after(
        `<div class="alert alert-success mb-4">Message added!</div>`
    )

    $messageModal.modal('hide');
}

$newMessageButton.on('click', function () {
    $messageModal.modal('show');
});

$likeForm.on('submit', like);
$newMessageForm.on('submit', addTweet);


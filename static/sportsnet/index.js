document.addEventListener('DOMContentLoaded', function () {
  const buttons = document.querySelectorAll('[data-action="open-modal"]');
  buttons.forEach((button) => {
    button.addEventListener('click', function () {
      openConfirmationModal(this);
    });
  });

  function openConfirmationModal(element) {
    const url = element.getAttribute('data-url');
    const message = element.getAttribute('data-message');

    // Ensure elements exist before trying to set properties
    const msgElement = document.getElementById('deleteModalLabel');
    const confirmBtn = document.getElementById('modal-confirm-btn');
    const modalElement = document.getElementById('confirmationModal');

    if (msgElement && confirmBtn && modalElement) {
      // Set the modal's message and confirmation button URL
      msgElement.textContent = message;
      confirmBtn.setAttribute('data-url', url);

      // Use Bootstrap's Modal class to show the modal
      const bootstrapModal = new bootstrap.Modal(modalElement);
      bootstrapModal.show();
    } else {
      console.error('Modal elements not found in the DOM.');
    }
  }

  window.openConfirmationModal = openConfirmationModal;

  document
    .getElementById('modal-confirm-btn')
    .addEventListener('click', function () {
      const url = this.getAttribute('data-url');

      fetch(url, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': getCSRFToken(),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
        });

      // fetch(url, {
      //   method: 'DELETE',
      //   headers: {
      //     'X-CSRFToken': getCSRFToken(),
      //   },
      // })
      //   .then((response) => response.json())
      //   .then((data) => {
      //     if (data.status === 'success') {
      //       console.log(data.message);
      //       alert(data.message);

      //       const playerElement = document.getElementById(
      //         'player-' + url.split('/').pop()
      //       );
      //       if (playerElement) {
      //         playerElement.remove();
      //       }

      //       const modalElement = document.getElementById('deleteModal');
      //       const bootstrapModal = bootstrap.Modal.getInstance(modalElement);
      //       bootstrapModal.hide();
      //     } else {
      //       alert('Failed to remove player');
      //     }
      //   })
      //   .catch((error) => {
      //     console.error('Error:', error);
      //   });
    });
});

function getCSRFToken() {
  const token = document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute('content')
    .trim();
  return token;
}

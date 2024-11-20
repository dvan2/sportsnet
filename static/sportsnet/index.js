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
      if (url) {
        window.location.href = url;
      } else {
        console.error('No URL set for confirm action.');
      }
    });
});

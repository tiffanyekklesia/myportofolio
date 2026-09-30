function showToast(title, message, type = 'normal', duration = 3000) {
    const toast = document.getElementById('toast-component');
    const titleElement = document.getElementById('toast-title');
    const messageElement = document.getElementById('toast-message');

    titleElement.textContent = title;
    messageElement.textContent = message;

    toast.classList.remove(
        'toast-normal',
        'toast-success',
        'toast-error',
        'toast-warning',
        'toast-hidden'
    );

    toast.classList.add(`toast-${type}`);
    toast.classList.add('toast-show');

    toast.showPopover();

    setTimeout(() => {
        toast.hidePopover();
        toast.classList.remove('toast-show');
        toast.classList.add('toast-hidden');
    }, duration);
}
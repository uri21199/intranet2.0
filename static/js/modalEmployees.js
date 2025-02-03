document.addEventListener("DOMContentLoaded", function () {
    const openButtons = document.querySelectorAll(".open-modal");
    const closeButtons = document.querySelectorAll(".close");
    const modals = document.querySelectorAll(".modal");

    openButtons.forEach(button => {
        button.addEventListener("click", function () {
            const modalId = this.getAttribute("data-modal");
            document.getElementById(modalId).style.display = "flex";
        });
    });

    closeButtons.forEach(button => {
        button.addEventListener("click", function () {
            this.parentElement.parentElement.style.display = "none";
        });
    });

    window.addEventListener("click", function (event) {
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });
    });
});

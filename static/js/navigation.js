document.addEventListener("DOMContentLoaded", function() {
    const toggleBtn = document.getElementById("close-btn");
    const sidebar = document.querySelector(".aside-sidebar");

    toggleBtn.addEventListener("click", function() {
        sidebar.classList.toggle("collapsed");

        // Agregar una transición suave al cerrar
        if (sidebar.classList.contains("collapsed")) {
            sidebar.style.overflow = "hidden"; // Evita que se vea el texto al colapsar
        } else {
            setTimeout(() => {
                sidebar.style.overflow = "visible";
            }, 300); // Espera el tiempo de la transición
        }
    });
});

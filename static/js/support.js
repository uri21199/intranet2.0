document.addEventListener("DOMContentLoaded", function () {
    loadCategories();
});

/**
 * Cargar las categorías según el rol del usuario
 */
function loadCategories() {
    fetch("/support/get_ticket_categories")
        .then(response => response.json())
        .then(data => {
            let categorySelect = document.getElementById("category");
            categorySelect.innerHTML = '<option value="">Seleccione...</option>';

            data.categories.forEach(category => {
                let option = document.createElement("option");
                option.value = category.id;
                option.textContent = category.name;
                categorySelect.appendChild(option);
            });
        })
        .catch(error => console.error("Error cargando categorías:", error));
}

/**
 * Cargar subcategorías cuando se selecciona una categoría
 */
function loadSubcategories() {
    let categoryId = document.getElementById("category").value;
    let subcategorySelect = document.getElementById("subcategory");
    subcategorySelect.innerHTML = '<option value="">Seleccione...</option>';

    if (!categoryId) return;

    fetch(`/support/get_ticket_subcategories?category_id=${categoryId}`)
        .then(response => response.json())
        .then(data => {
            data.subcategories.forEach(subcat => {
                let option = document.createElement("option");
                option.value = subcat.id;
                option.textContent = subcat.name;
                subcategorySelect.appendChild(option);
            });
        })
        .catch(error => console.error("Error cargando subcategorías:", error));
}

/**
 * Enviar formulario para crear un nuevo ticket
 */
function submitTicket() {
    let categoryId = document.getElementById("category").value;
    let subcategoryId = document.getElementById("subcategory").value;
    let description = document.getElementById("description").value;

    if (!categoryId || !subcategoryId) {
        alert("Seleccione una categoría y subcategoría.");
        return;
    }

    fetch("/support/create_ticket", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            category_id: categoryId,
            subcategory_id: subcategoryId,
            description: description
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Ticket creado con éxito.");
                location.reload();
            } else {
                alert("Error al crear ticket: " + data.error);
            }
        })
        .catch(error => console.error("Error al enviar ticket:", error));
}

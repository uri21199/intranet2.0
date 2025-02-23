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


document.addEventListener("DOMContentLoaded", function () {
    loadUserTickets();
});

function loadUserTickets() {
    fetch("/support/get_user_tickets")
        .then(response => response.json())
        .then(data => {
            let tableBody = document.getElementById("ticket-table-body");
            tableBody.innerHTML = "";

            if (data.error) {
                tableBody.innerHTML = `<tr><td colspan="6">${data.error}</td></tr>`;
                return;
            }

            if (data.length === 0) {
                tableBody.innerHTML = `<tr><td colspan="6">No hay tickets creados.</td></tr>`;
                return;
            }

            data.forEach(ticket => {
                let row = `
                    <tr>
                        <td>${ticket.id}</td>
                        <td>${ticket.category}</td>
                        <td>${ticket.subcategory}</td>
                        <td>${ticket.description}</td>
                        <td>${ticket.status}</td>
                        <td>
                            <button class="button view-ticket" data-id="${ticket.id}">Ver</button>
                            <button class="button resend-ticket" data-id="${ticket.id}">Reenviar 📩</button>
                        </td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });

            // Agregar eventos a los botones
            document.querySelectorAll(".resend-ticket").forEach(button => {
                button.addEventListener("click", function () {
                    let ticketId = this.dataset.id;
                    resendTicket(ticketId);
                });
            });

            document.querySelectorAll(".view-ticket").forEach(button => {
                button.addEventListener("click", function () {
                    let ticketId = this.dataset.id;
                    openTicketModal(ticketId);
                });
            });

        })
        .catch(error => {
            console.error("Error al cargar los tickets:", error);
            document.getElementById("ticket-table-body").innerHTML = `<tr><td colspan="6">Error al cargar tickets.</td></tr>`;
        });
}

function resendTicket(ticketId) {
    alert(`Funcionalidad pendiente: Reenviar notificación para el ticket #${ticketId}`);
}

function openTicketModal(ticketId) {
    alert(`Funcionalidad pendiente: Mostrar detalles del ticket #${ticketId}`);
}

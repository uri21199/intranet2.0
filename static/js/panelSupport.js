document.addEventListener("DOMContentLoaded", function () {
    loadTickets();
    loadFilters();
});

async function loadTickets() {
    try {
        const response = await fetch("/support/get_tickets");
        const tickets = await response.json();
        console.log(tickets)
        const tbody = document.querySelector("#ticketsTable tbody");
        tbody.innerHTML = "";
        
        tickets.forEach(ticket => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${ticket.id}</td>
                <td>${ticket.category}</td>
                <td>${ticket.subcategory}</td>
                <td>${ticket.description}</td>
                <td>${ticket.status}</td>
                <td><button class="btn-view" data-id="${ticket.id}">Ver</button></td>
            `;
            tbody.appendChild(row);
        });

        document.querySelectorAll(".btn-view").forEach(button => {
            button.addEventListener("click", function () {
                openPanel(this.dataset.id);
            });
        });
    } catch (error) {
        console.error("Error cargando tickets:", error);
    }
}

async function loadFilters() {
    try {
        const response = await fetch("/support/get_ticket_filters");
        const filters = await response.json();
        
        populateFilter("categoryFilter", filters.categories);
        populateFilter("statusFilter", filters.statuses);
        populateFilter("assignedFilter", filters.support_users);
    } catch (error) {
        console.error("Error cargando filtros:", error);
    }
}

function populateFilter(filterId, data) {
    const select = document.getElementById(filterId);
    select.innerHTML = '<option value="">Todos</option>'; // Opción predeterminada

    data.forEach(item => {
        select.innerHTML += `<option value="${item.id}">${item.name}</option>`;
    });

    select.addEventListener("change", loadTickets);
}

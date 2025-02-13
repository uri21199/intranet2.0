document.addEventListener("DOMContentLoaded", function () {
    cargarSalas();  // Llenar el filtro de salas
    cargarReservas(); // Cargar todas las reservas al inicio
});

function cargarSalas() {
    fetch("/admin/get_rooms")
        .then(response => response.json())
        .then(data => {
            const filterRoom = document.getElementById("filterRoom");
            filterRoom.innerHTML = "<option value=''>Todas</option>";
            data.forEach(room => {
                const option = document.createElement("option");
                option.value = room.id;
                option.textContent = room.name;
                filterRoom.appendChild(option);
            });
        })
        .catch(error => console.error("Error cargando salas:", error));
}

function cargarReservas() {
    const roomId = document.getElementById("filterRoom").value;
    const status = document.getElementById("filterStatus").value;

    let url = `/rooms/get_reservations?room_id=${roomId}&status=${status}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => actualizarTablaReservas(data))
        .catch(error => console.error("Error cargando reservas:", error));
}

function actualizarTablaReservas(data) {
    const tbody = document.getElementById("tablaReservas");
    tbody.innerHTML = "";

    data.forEach(reserva => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${reserva.room_name}</td>
            <td>${reserva.reservation_date}</td>
            <td>${reserva.start_time}</td>
            <td>${reserva.end_time}</td>
            <td class="status-${reserva.status.toLowerCase()}">${reserva.status}</td>
            <td class="actions">
                ${reserva.status === "Pendiente" ? `<button onclick="editarReserva(${reserva.id}, '${reserva.reservation_date}', '${reserva.start_time}', '${reserva.end_time}')">✏️</button>` : ""}
                ${reserva.status === "Pendiente" ? `<button onclick="eliminarReserva(${reserva.id})">🗑️</button>` : ""}
            </td>
        `;
        tbody.appendChild(row);
    });
}


function editarReserva(id, fechaActual, horaInicioActual, horaFinActual) {
    const nuevaFecha = prompt("Ingrese la nueva fecha (YYYY-MM-DD):", fechaActual);
    if (!nuevaFecha) return;

    const nuevaHoraInicio = prompt("Ingrese la nueva hora de inicio (HH:MM):", horaInicioActual);
    if (!nuevaHoraInicio) return;

    const nuevaHoraFin = prompt("Ingrese la nueva hora de fin (HH:MM):", horaFinActual);
    if (!nuevaHoraFin) return;

    fetch("/rooms/update_reservation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            reservation_id: id,
            new_date: nuevaFecha,
            new_start_time: nuevaHoraInicio,
            new_end_time: nuevaHoraFin
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        cargarReservas();  // Actualizar tabla después de editar
    })
    .catch(error => console.error("Error al actualizar:", error));
}


function eliminarReserva(id) {
    if (!confirm("¿Estás seguro de que deseas eliminar esta reserva?")) return;

    fetch("/rooms/delete_reservation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reservation_id: id })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        cargarReservas();  // Actualizar tabla
    })
    .catch(error => console.error("Error al eliminar:", error));
}

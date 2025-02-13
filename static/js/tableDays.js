document.addEventListener("DOMContentLoaded", function () {
    cargarSolicitudes();
});

function cargarSolicitudes() {
    fetch("/days/get_days")
        .then(response => response.json())
        .then(data => actualizarTabla(data))
        .catch(error => console.error("Error al cargar solicitudes:", error));
}

function actualizarTabla(data) {
    const tbody = document.getElementById("tablaSolicitudes");
    tbody.innerHTML = "";

    data.forEach(day => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${obtenerNombreTipoDia(day.day_type)}</td>
            <td>${day.start_date}${day.end_date !== day.start_date ? " - " + day.end_date : ""}</td>
            <td>${day.reason || "-"}</td>
            <td class="status-${day.status.toLowerCase()}">${day.status}</td>
            <td class="file">
                ${day.status === "Aprobado" ? `<button onclick="subirArchivo(${day.id})">Subir</button>` : "-"}
            </td>
            <td class="actions">
                ${day.status === "Pendiente" ? `<button onclick="editarDia(${day.id}, '${day.start_date}')">✏️</button>` : ""}
                ${day.status === "Pendiente" ? `<button onclick="eliminarDia(${day.id})">🗑️</button>` : ""}
            </td>
        `;
        tbody.appendChild(row);
    });
}


function obtenerNombreTipoDia(dayTypeId) {
    const tipos = { "1": "Día de ausencia", "2": "Día de estudio", "3": "Día de home office", "4": "Días de vacaciones" };
    return tipos[dayTypeId] || "Desconocido";
}

function editarDia(dayId, fechaActual) {
    const nuevaFecha = prompt("Ingrese la nueva fecha (YYYY-MM-DD):", fechaActual);
    if (!nuevaFecha) return;

    fetch("/days/update_day", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ day_id: dayId, new_date: nuevaFecha })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        cargarSolicitudes();
    })
    .catch(error => console.error("Error al actualizar:", error));
}

function eliminarDia(dayId) {
    if (!confirm("¿Estás seguro de que deseas eliminar esta solicitud?")) return;

    fetch("/days/delete_day", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ day_id: dayId })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        cargarSolicitudes();
    })
    .catch(error => console.error("Error al eliminar:", error));
}





function subirArchivo(requestId) {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".pdf,.jpg,.jpeg,.png,.docx";
    input.onchange = () => {
        const file = input.files[0];
        if (file) {
            const formData = new FormData();
            formData.append("file", file);
            formData.append("request_id", requestId);

            fetch("/upload_file", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                cargarSolicitudes(); // Recargar la tabla
            })
            .catch(error => console.error("Error al subir archivo:", error));
        }
    };
    input.click();
}

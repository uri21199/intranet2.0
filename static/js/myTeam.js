function loadAbsencesSummary() {
    fetch("/myteam/absences-summary")
        .then(response => response.json())
        .then(data => {
            document.getElementById("weeklyAbsences").innerText = data.weekly_absences;
            document.getElementById("monthlyAbsences").innerText = data.monthly_absences;
        })
        .catch(error => console.error("Error al cargar ausencias:", error));
}

// Cargar los datos al abrir la página
document.addEventListener("DOMContentLoaded", loadAbsencesSummary);

function loadMonthlyAbsences() {
fetch("/myteam/monthly-absences")
    .then(response => response.json())
    .then(data => {
        let tableBody = document.querySelector("#monthlyAbsencesTable tbody");
        tableBody.innerHTML = "";  // Limpia la tabla antes de actualizar
        
        data.forEach(absence => {
            let row = `<tr>
                <td>${absence.name}</td>
                <td>${absence.start_date}</td>
                <td>${absence.absence_type}</td>
            </tr>`;
            tableBody.innerHTML += row;
        });
    })
    .catch(error => console.error("Error al cargar ausencias del mes:", error));
}

// Cargar la tabla al abrir la página
document.addEventListener("DOMContentLoaded", loadMonthlyAbsences);

function loadTeamAbsences() {
    fetch("/myteam/data")
        .then(response => response.json())
        .then(data => {
            let tableBody = document.querySelector("#teamAbsencesTable tbody");
            tableBody.innerHTML = ""; // Limpiar la tabla antes de actualizar
            
            data.forEach(employee => {
                let row = `<tr>
                    <td>${employee.name}</td>
                    <td>${employee.last_absence}</td>
                    <td>${employee.next_absence}</td>
                    <td>${employee.absence_count}</td>
                    <td>
                        <button onclick="viewEmployee(${employee.id})">📜 Ver empleado</button>
                    </td>
                </tr>`;
                tableBody.innerHTML += row;
            });
        })
        .catch(error => console.error("Error al cargar la tabla de empleados:", error));
}

// Cargar la tabla automáticamente al abrir la página
document.addEventListener("DOMContentLoaded", loadTeamAbsences);

let requestedDays = [];  // Variable global para almacenar los datos originales

function viewEmployee(employeeId) {
    console.log("Consultando datos del empleado con ID:", employeeId);

    fetch(`/myteam/employee/${employeeId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Datos recibidos:", data);
            requestedDays = data.requested_days; 
            mostrarEmpleado(data);
        })
        .catch(error => console.error("Error al obtener datos del empleado:", error));
}

function mostrarEmpleado(data) {
    const container = document.getElementById("empleadoDetalle");
    container.innerHTML = `
        <h3>Información del Empleado</h3>
        <p><strong>Nombre:</strong> ${data.employee.first_name} ${data.employee.last_name}</p>
        <p><strong>Email:</strong> ${data.employee.email}</p>
        <p><strong>Teléfono:</strong> ${data.employee.phone}</p>
        <p><strong>Dirección:</strong> ${data.employee.address}, ${data.employee.city}, ${data.employee.state}</p>
        <p><strong>CUIT:</strong> ${data.employee.tax_id}</p>
        <p><strong>Fecha de contratación:</strong> ${data.employee.hire_date}</p>
        <p><strong>Legajo:</strong> ${data.employee.record_number}</p>
                <h3>Filtros</h3>
        <label>Fecha solicitada: <input type="date" id="filterDate"></label>
        <label>Tipo de Día:
            <select id="filterType">
                <option value="">Todos</option>
                <option value="Ausencia">Ausencia</option>
                <option value="Estudio">Estudio</option>
                <option value="Home Office">Home Office</option>
                <option value="Vacaciones">Vacaciones</option>
            </select>
        </label>
        <label>Estado:
            <select id="filterStatus">
                <option value="">Todos</option>
                <option value="Pendiente">Pendiente</option>
                <option value="Aprobado">Aprobado</option>
                <option value="Rechazado">Rechazado</option>
            </select>
        </label>
        <button onclick="filtrarTabla()">Aplicar Filtros</button>
        <h3>Historial de Ausencias</h3>
        <table class="emails-table">
            <thead>
                <tr>
                    <th>Fecha Solicitada</th>
                    <th>Tipo de Día</th>
                    <th>Motivo</th>
                    <th>Estado</th>
                    <th>Fecha de Carga</th>
                </tr>
            </thead>
            <tbody>
            <tbody id="tablaRequestedDays">
                ${generarFilasTabla(requestedDays)}
            </tbody>
            </tbody>
        </table>
    `;

        // Agregar eventos para actualizar la tabla automáticamente al cambiar un filtro
        document.getElementById("filterDate").addEventListener("change", filtrarTabla);
        document.getElementById("filterType").addEventListener("change", filtrarTabla);
        document.getElementById("filterStatus").addEventListener("change", filtrarTabla);
}

function generarFilasTabla(data) {
    return data.length > 0 ? data.map(rd => `
        <tr>
            <td>${rd.start_date}</td>
            <td>${rd.day_type}</td>
            <td>${rd.reason}</td>
            <td>${rd.status}</td>
            <td>${rd.created_at}</td>
        </tr>
    `).join("") : "<tr><td colspan='6'>No hay registros</td></tr>";
}

function filtrarTabla() {
    const fechaFiltro = document.getElementById("filterDate").value;
    const tipoFiltro = document.getElementById("filterType").value;
    const estadoFiltro = document.getElementById("filterStatus").value;

    console.log(`Aplicando filtros: Fecha: ${fechaFiltro}, Tipo: ${tipoFiltro}, Estado: ${estadoFiltro}`);

    let datosFiltrados = requestedDays.filter(rd => {
        return (!fechaFiltro || rd.start_date === fechaFiltro) &&
               (!tipoFiltro || rd.day_type === tipoFiltro) &&
               (!estadoFiltro || rd.status === estadoFiltro);
    });

    document.getElementById("tablaRequestedDays").innerHTML = generarFilasTabla(datosFiltrados);
}
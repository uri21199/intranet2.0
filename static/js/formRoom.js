function cambiarFormulario() {
    const tipoSala = document.getElementById("typeRoom").value;
    const formulario = document.getElementById("formFields");

    formulario.innerHTML = ""; // Limpia el formulario

    if (tipoSala === "capacitaciones") {
        formulario.innerHTML = `
            <label for="area">Seleccionar Área</label>
            <select id="area" onchange="cargarEmpleados()">
                <option value="IT">IT</option>
                <option value="Marketing">Marketing</option>
                <option value="RRHH">RRHH</option>
            </select>

            <label for="empleados">Seleccionar Empleado</label>
            <select id="empleados">
                <option value="">Selecciona un área primero</option>
            </select>

            <button onclick="agregarEmpleado()">Añadir Empleado</button>
            
            <h3>Empleados seleccionados:</h3>
            <ul id="listaEmpleados"></ul>

            <label for="fecha">Fecha</label>
            <input type="date" id="fecha">

            <label for="horaInicio">Hora de Inicio</label>
            <input type="time" id="horaInicio">

            <label for="horaFin">Hora de Fin</label>
            <input type="time" id="horaFin">
        `;
    } else if (tipoSala === "reuniones") {
        formulario.innerHTML = `
            <label for="cliente">Es para un cliente?</label>
            <select id="cliente" onchange="toggleCliente()">
                <option value="no">No</option>
                <option value="si">Sí</option>
            </select>

            <div id="clienteSeleccion">
                <!-- Se agregará si el usuario elige "Sí" -->
            </div>

            <label for="motivo">Motivo</label>
            <input type="text" id="motivo" placeholder="Motivo">

            <label for="fecha">Fecha</label>
            <input type="date" id="fecha">

            <label for="horaInicio">Hora de Inicio</label>
            <input type="time" id="horaInicio">

            <label for="horaFin">Hora de Fin</label>
            <input type="time" id="horaFin">
        `;
    }
}

function toggleCliente() {
    const clienteSeleccion = document.getElementById("clienteSeleccion");
    const esCliente = document.getElementById("cliente").value;

    if (esCliente === "si") {
        clienteSeleccion.innerHTML = `
            <label for="clientesLista">Seleccionar Cliente</label>
            <select id="clientesLista">
                <option value="1">Cliente 1</option>
                <option value="2">Cliente 2</option>
                <option value="3">Cliente 3</option>
            </select>
        `;
    } else {
        clienteSeleccion.innerHTML = "";
    }
}

let empleadosSeleccionados = [];

function cargarEmpleados() {
    const area = document.getElementById("area").value;
    const empleadosSelect = document.getElementById("empleados");

    // Simulación de carga de empleados por área
    let empleadosPorArea = {
        "IT": ["Juan Pérez", "Ana Gómez", "Carlos López"],
        "Marketing": ["Luis Rodríguez", "María Sánchez"],
        "RRHH": ["Pedro Martínez", "Lucía Fernández"]
    };

    empleadosSelect.innerHTML = "";
    empleadosPorArea[area].forEach(emp => {
        let option = document.createElement("option");
        option.value = emp;
        option.textContent = emp;
        empleadosSelect.appendChild(option);
    });
}

function agregarEmpleado() {
    const empleado = document.getElementById("empleados").value;
    if (empleado && !empleadosSeleccionados.includes(empleado)) {
        empleadosSeleccionados.push(empleado);

        const lista = document.getElementById("listaEmpleados");
        const li = document.createElement("li");
        li.textContent = empleado;
        lista.appendChild(li);
    }
}

function enviarSolicitud() {
    console.log("Empleados seleccionados:", empleadosSeleccionados);
}

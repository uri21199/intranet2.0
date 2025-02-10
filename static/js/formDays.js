function cambiarFormulario() {
    // Obtener el valor seleccionado del tipo de día
    const tipoDia = document.getElementById("typeDay").value;
    // Obtener el contenedor donde se generarán los campos dinámicamente
    const formulario = document.getElementById("formFields");
    formulario.innerHTML = ""; // Limpiar el contenido antes de agregar nuevos elementos
    
    // Obtener la fecha actual
    const today = new Date();
    let minDate = ""; // Fecha mínima permitida
    let maxDate = ""; // Fecha máxima permitida
    
    if (tipoDia === "1") {
        // Configurar el rango de fechas: 1 mes antes y 1 mes después de la fecha actual
        minDate = new Date(today);
        minDate.setMonth(today.getMonth() - 1);
        maxDate = new Date(today);
        maxDate.setMonth(today.getMonth() + 1);
        
        // Insertar los campos específicos para ausencia
        formulario.innerHTML = `
            <label for="motivo">Motivo</label>
            <select id="motivo">
                <option value="enfermedad">Enfermedad</option>
                <option value="turno_medico">Turno médico</option>
                <option value="mudanza">Mudanza</option>
                <option value="problema_familiar">Problema familiar</option>
                <option value="otro">Otro</option>
            </select>
            <label for="fecha">Fecha</label>
            <input type="date" id="fecha" min="${minDate.toISOString().split('T')[0]}" max="${maxDate.toISOString().split('T')[0]}">
        `;
    } else if (tipoDia === "2") {
        // Configurar el rango de fechas: 1 mes antes y hasta 6 meses después
        minDate = new Date(today);
        minDate.setMonth(today.getMonth() - 1);
        maxDate = new Date(today);
        maxDate.setMonth(today.getMonth() + 6);
        
        // Insertar los campos específicos para estudio
        formulario.innerHTML = `
            <label for="motivo">Motivo</label>
            <select id="motivo">
                <option value="dia_examen">Día de examen</option>
                <option value="dia_estudio">Día de estudio</option>
                <option value="trabajo_practico">Trabajo práctico</option>
            </select>
            <label for="fecha">Fecha</label>
            <input type="date" id="fecha" min="${minDate.toISOString().split('T')[0]}" max="${maxDate.toISOString().split('T')[0]}">
            <button type="button" id="btnAgregarFecha">Agregar Fecha</button>
            <ul id="listaFechas"></ul>
        `;
        document.getElementById("btnAgregarFecha").addEventListener("click", agregarFecha);
    } else if (tipoDia === "3") {
        // Configurar el rango de fechas: 1 mes antes y hasta 2 meses después
        minDate = new Date(today);
        minDate.setMonth(today.getMonth() - 1);
        maxDate = new Date(today);
        maxDate.setMonth(today.getMonth() + 2);
        
        // Insertar los campos específicos para home office
        formulario.innerHTML = `
            <label for="fecha">Fecha o Fechas</label>
            <input type="date" id="fecha" multiple min="${minDate.toISOString().split('T')[0]}" max="${maxDate.toISOString().split('T')[0]}">
            <button type="button" id="btnAgregarFecha">Agregar Fecha</button>
            <ul id="listaFechas"></ul>
        `;
        document.getElementById("btnAgregarFecha").addEventListener("click", agregarFecha);
    } else if (tipoDia === "4") {
        // Configurar el rango de fechas: hasta 8 meses después de la fecha actual
        minDate = new Date(today);
        maxDate = new Date(today);
        maxDate.setMonth(today.getMonth() + 8);
        
        // Insertar los campos específicos para vacaciones
        formulario.innerHTML = `
            <label for="inicio">Fecha inicio</label>
            <input type="date" id="inicio" min="${today.toISOString().split('T')[0]}" max="${maxDate.toISOString().split('T')[0]}">
            <label for="fin">Fecha fin</label>
            <input type="date" id="fin" min="${today.toISOString().split('T')[0]}" max="${maxDate.toISOString().split('T')[0]}">
            <label for="asistencia">¿Requiere asistencia al viajero?</label>
            <select id="asistencia">
                <option value="no">No</option>
                <option value="si">Sí</option>
            </select>
        `;
    }
}


let fechasSeleccionadas = [];

function agregarFecha() {
    console.log("Evento agregarFecha activado");
    const fechaInput = document.getElementById("fecha");
    const fecha = fechaInput.value;
    
    if (!fecha || fechasSeleccionadas.includes(fecha)) {
        alert("Fecha inválida o ya seleccionada.");
        return;
    }

    fechasSeleccionadas.push(fecha);
    actualizarListaFechas();
}

function eliminarFecha(index) {
    fechasSeleccionadas.splice(index, 1);
    actualizarListaFechas();
}

function actualizarListaFechas() {
    const lista = document.getElementById("listaFechas");
    lista.innerHTML = "";

    fechasSeleccionadas.forEach((fecha, index) => {
        const item = document.createElement("li");
        item.innerHTML = `${fecha} <button type='button' onclick='eliminarFecha(${index})'>X</button>`;
        lista.appendChild(item);
    });
}



function enviarSolicitud(event) {
    event.preventDefault();

    const tipoDia = document.getElementById("typeDay").value;
    let fechas = [];
    let start_date = "";
    let end_date = "";
    let reason = "";
    let asistencia = null;

    if (tipoDia === "3" || tipoDia === "2") {
        fechas = fechasSeleccionadas;
    } else if (tipoDia === "4") {
        start_date = document.getElementById("inicio").value;
        end_date = document.getElementById("fin").value;
        asistencia = document.getElementById("asistencia").value;
    } else {
        start_date = document.getElementById("fecha").value;
    }

    if (!fechas.length && !start_date) {
        alert("Debe seleccionar al menos una fecha.");
        return;
    }

    const requestData = {
        day_type_id: tipoDia,
        fechas: fechas.length ? fechas : [start_date],
        end_date: end_date || start_date,
        reason: reason,
        asistencia: asistencia
    };

    fetch("/days_request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error("Error en la solicitud:", error));
}

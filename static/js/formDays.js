function cambiarFormulario() {
    const tipoDia = document.getElementById("typeDay").value;
    const formulario = document.getElementById("formFields");
    formulario.innerHTML = ""; 

    if (tipoDia === "ausencia") {
        formulario.innerHTML = `
            <label for="motivo">Motivo</label>
            <input type="text" id="motivo" placeholder="Motivo">
            <label for="fecha">Fecha</label>
            <input type="date" id="fecha">
        `;
    } else if (tipoDia === "home_office" || tipoDia === "estudio") {
        formulario.innerHTML = `
            <label for="fecha">Fecha o Fechas</label>
            <input type="date" id="fecha" multiple>
        `;
    } else if (tipoDia === "vacaciones") {
        formulario.innerHTML = `
            <label for="inicio">Fecha inicio</label>
            <input type="date" id="inicio">
            <label for="fin">Fecha fin</label>
            <input type="date" id="fin">
            <label for="asistencia">¿Requiere asistencia al viajero?</label>
            <select id="asistencia">
                <option value="no">No</option>
                <option value="si">Sí</option>
            </select>
        `;
    }
}
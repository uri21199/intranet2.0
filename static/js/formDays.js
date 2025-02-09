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
    
    if (tipoDia === "ausencia") {
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
    } else if (tipoDia === "estudio") {
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
        `;
    } else if (tipoDia === "home_office") {
        // Configurar el rango de fechas: 1 mes antes y hasta 2 meses después
        minDate = new Date(today);
        minDate.setMonth(today.getMonth() - 1);
        maxDate = new Date(today);
        maxDate.setMonth(today.getMonth() + 2);
        
        // Insertar los campos específicos para home office
        formulario.innerHTML = `
            <label for="fecha">Fecha o Fechas</label>
            <input type="date" id="fecha" multiple min="${minDate.toISOString().split('T')[0]}" max="${maxDate.toISOString().split('T')[0]}">
        `;
    } else if (tipoDia === "vacaciones") {
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

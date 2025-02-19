document.addEventListener("DOMContentLoaded", function () {
    const openButtons = document.querySelectorAll(".open-modal");
    const closeButtons = document.querySelectorAll(".close");
    const modals = document.querySelectorAll(".modal");

    openButtons.forEach(button => {
        button.addEventListener("click", function () {
            const modalId = this.getAttribute("data-modal");
            document.getElementById(modalId).style.display = "flex";
        });
    });

    closeButtons.forEach(button => {
        button.addEventListener("click", function () {
            this.parentElement.parentElement.style.display = "none";
        });
    });

    window.addEventListener("click", function (event) {
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const areaSelect = document.getElementById("areaEmployees");
    const employeeSelect = document.getElementById("employees");
    const employeeInfoContainer = document.getElementById("employee-info");

    /**
     * Función para cargar las áreas desde el backend
     */
    function loadAreas() {
        fetch("/admin/get_areas")
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error en la respuesta del servidor: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                areaSelect.innerHTML = "";
                if (data.length === 0) {
                    console.warn("No se encontraron áreas en la base de datos.");
                    return;
                }

                data.forEach(area => {
                    const option = document.createElement("option");
                    option.value = area.id;
                    option.textContent = area.name;
                    areaSelect.appendChild(option);
                });

                console.log("Áreas cargadas correctamente:", data);

                // Cargar empleados del primer área por defecto
                loadEmployees(areaSelect.value);
            })
            .catch(error => console.error("Error cargando áreas:", error));
    }

    /**
     * Función para cargar los empleados de un área específica
     * @param {string} areaId - ID del área seleccionada
     */
    function loadEmployees(areaId) {
        if (!areaId) {
            console.warn("No se proporcionó un ID de área.");
            return;
        }

        fetch(`/admin/get_employees?area_id=${areaId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error en la respuesta del servidor: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                employeeSelect.innerHTML = "";
                if (data.length === 0) {
                    console.warn(`No se encontraron empleados para el área con ID ${areaId}.`);
                    return;
                }

                data.forEach(emp => {
                    const option = document.createElement("option");
                    option.value = emp.id;
                    option.textContent = emp.name;
                    employeeSelect.appendChild(option);
                });

                console.log(`Empleados cargados para área ${areaId}:`, data);

                // Cargar los datos del primer empleado por defecto
                if (data.length > 0) {
                    loadEmployeeInfo(data[0].id);
                }
            })
            .catch(error => console.error("Error cargando empleados:", error));
    }

    /**
     * Función para obtener y mostrar la información de un empleado
     * @param {string} employeeId - ID del empleado seleccionado
     */
    function loadEmployeeInfo(employeeId) {
        if (!employeeId) {
            console.warn("No se proporcionó un ID de empleado.");
            return;
        }

        fetch(`/admin/get_employee_info?employee_id=${employeeId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error en la respuesta del servidor: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    console.error("Error en la respuesta del servidor:", data.error);
                    employeeInfoContainer.innerHTML = `<p>Error: ${data.error}</p>`;
                    return;
                }

                employeeInfoContainer.innerHTML = `
                    <h3>${data.name}</h3>
                    <p><strong>Área:</strong> ${data.department}</p>
                    <p><strong>Cargo:</strong> ${data.cargo}</p>
                `;

                console.log(`Información del empleado ${employeeId} cargada correctamente:`, data);
            })
            .catch(error => console.error("Error cargando información del empleado:", error));
    }

    /**
     * Evento: Cambio en la selección de área
     */
    areaSelect.addEventListener("change", function () {
        loadEmployees(this.value);
    });

    /**
     * Evento: Cambio en la selección de empleado
     */
    employeeSelect.addEventListener("change", function () {
        loadEmployeeInfo(this.value);
    });

    // Iniciar carga de datos al cargar la página
    loadAreas();
});



document.addEventListener("DOMContentLoaded", function () {
    const employeeSelect = document.getElementById("employees");
    const daysContainer = document.getElementById("requested-days");
    const modalDaysContainer = document.getElementById("modal-days-content");

    function clearRequestedDays() {
        document.getElementById("requested-days").innerHTML = `
            <tr><td colspan="4">Cargando...</td></tr>`;
        document.getElementById("modal-days-content").innerHTML = `
            <tr><td colspan="4">Cargando...</td></tr>`;
    }
    

    /**
     * Función para cargar los días solicitados de un empleado
     * @param {string} employeeId - ID del empleado seleccionado
     */
    function loadRequestedDays(employeeId) {
        if (!employeeId) {
            console.warn("No se proporcionó un ID de empleado.");
            return;
        }
        clearRequestedDays();


        fetch(`/get_requested_days?employee_id=${employeeId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("Error en la respuesta del servidor:", data.error);
                    daysContainer.innerHTML = `<tr><td colspan="4">Error: ${data.error}</td></tr>`;
                    return;
                }

                if (data.message) {
                    daysContainer.innerHTML = `<tr><td colspan="4">No hay días solicitados.</td></tr>`;
                    modalDaysContainer.innerHTML = `<tr><td colspan="4">No hay más registros.</td></tr>`;
                    return;
                }

                console.log(`Días solicitados de ${employeeId}:`, data);

                // Mostrar los 2 últimos en la card
                daysContainer.innerHTML = data.slice(0, 2).map(day => `
                    <tr>
                        <td>${day.day_type}</td>
                        <td>${day.start_date}</td>
                        <td>${day.end_date}</td>
                        <td><span class="status ${day.status.toLowerCase()}">${day.status}</span></td>
                    </tr>
                `).join("");

                // Mostrar todos en el modal
                modalDaysContainer.innerHTML = data.map(day => `
                    <tr>
                        <td>${day.day_type}</td>
                        <td>${day.start_date}</td>
                        <td>${day.end_date}</td>
                        <td><span class="status ${day.status.toLowerCase()}">${day.status}</span></td>
                    </tr>
                `).join("");
            })
            .catch(error => {
                console.error("Error cargando días solicitados:", error);
                daysContainer.innerHTML = `<tr><td colspan="4">Error al cargar datos.</td></tr>`;
            });
    }

    // Evento: Cambio de empleado
    employeeSelect.addEventListener("change", function () {
        loadRequestedDays(this.value);
    });

    // Cargar los datos del empleado seleccionado por defecto
    loadRequestedDays(employeeSelect.value);
});


document.getElementById("areaEmployees").addEventListener("change", function () {
    const firstEmployee = document.getElementById("employees").options[0].value;
    
    if (firstEmployee) {
        document.getElementById("employees").value = firstEmployee; // Seleccionar primer empleado de la lista
        loadRequestedDays(firstEmployee); // Cargar datos del nuevo empleado
    }
});

/**
 * Evento cuando se cambia de empleado: cargar sus datos
 */
document.getElementById("employees").addEventListener("change", function () {
    loadRequestedDays(this.value);
});

/**
 * Cargar los datos del empleado seleccionado por defecto al cargar la página
 */
const defaultEmployee = document.getElementById("employees").value;
if (defaultEmployee) {
    loadRequestedDays(defaultEmployee);
}
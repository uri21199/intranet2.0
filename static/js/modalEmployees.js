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

const reportFilters = {
    "employees_status": {
        roles: {
            "administrador general": ["areaFilterContainer", "roleFilterContainer", "employeeFilterContainer"],
            "recursos humanos": ["areaFilterContainer", "roleFilterContainer", "employeeFilterContainer"],
            "jefe de area": ["employeeFilterContainer"]
        }
    },
    "requested_days": {
        roles: {
            "administrador general": ["areaFilterContainer", "roleFilterContainer", "dateRangeContainer", "employeeFilterContainer"],
            "recursos humanos": ["dateRangeContainer", "employeeFilterContainer"],
            "jefe de area": ["employeeFilterContainer", "dateRangeContainer"]
        }
    },
    "trainings": {
        roles: {
            "administrador general": ["areaFilterContainer", "roleFilterContainer", "dateRangeContainer", "employeeFilterContainer", "statusFilterContainer"],
            "recursos humanos": ["areaFilterContainer", "roleFilterContainer", "dateRangeContainer", "employeeFilterContainer", "statusFilterContainer"]
        }
    },
    "trainings_list": {
        roles: {
            "administrador general": ["areaFilterContainer", "roleFilterContainer", "dateRangeContainer", "statusFilterContainer"],
            "recursos humanos": ["areaFilterContainer", "roleFilterContainer", "dateRangeContainer", "statusFilterContainer"]
        }
    },
    "salary_receipts": {
        roles: {
            "administrador general": ["employeeFilterContainer","dateRangeContainer", "statusFilterContainer"],
            "recursos humanos": ["employeeFilterContainer","dateRangeContainer", "statusFilterContainer"]
        }
    },
    "equipments": {
        roles: {
            "administrador general": ["areaFilterContainer", "roleFilterContainer", "dateRangeContainer", "employeeFilterContainer", "statusFilterContainer"],
            "recursos humanos": ["areaFilterContainer", "roleFilterContainer", "dateRangeContainer", "employeeFilterContainer", "statusFilterContainer"]
        }
    },
    "room_reservations": {
        roles: {
            "administrador general": ["dateRangeContainer", "statusFilterContainer", "employeeFilterContainer"],
            "recursos humanos": ["dateRangeContainer", "statusFilterContainer", "employeeFilterContainer"]
        }
    },
    "document_versions": {
        roles: {
            "administrador general": [],
            "recursos humanos": []
        }
    },
    "access_logs": {
        roles: {
            "administrador general": ["areaFilterContainer", "roleFilterContainer", "dateRangeContainer", "employeeFilterContainer"],
            "recursos humanos": ["areaFilterContainer", "roleFilterContainer", "dateRangeContainer", "employeeFilterContainer"]
        }
    },
    "system_tickets": {
        roles: {
            "administrador general": ["areaFilterContainer", "roleFilterContainer", "dateRangeContainer", "employeeFilterContainer", "statusFilterContainer"],
            "recursos humanos": ["areaFilterContainer", "roleFilterContainer", "dateRangeContainer", "employeeFilterContainer", "statusFilterContainer"],
            "soporte tecnico": ["areaFilterContainer", "roleFilterContainer", "dateRangeContainer", "employeeFilterContainer", "statusFilterContainer"]
        }
    }
};


function mostrarFiltros(reporteSeleccionado) {
    // Ocultamos todos los filtros
    document.querySelectorAll("#filtersContainer .form-group").forEach(el => el.classList.add("hidden"));

    if (!reportFilters[reporteSeleccionado]) return;
    
    // Buscar los roles permitidos para este reporte
    let filtrosPermitidos = new Set(); // Usamos un Set para evitar duplicados

    window.userRoles.forEach(rol => {
        if (reportFilters[reporteSeleccionado].roles[rol]) {
            reportFilters[reporteSeleccionado].roles[rol].forEach(filtro => filtrosPermitidos.add(filtro));
        }
    });

    // Mostrar los filtros que el usuario tiene permiso de ver
    filtrosPermitidos.forEach(filtro => {
        document.getElementById(filtro).classList.remove("hidden");
        document.getElementById("generateReport").classList.remove("hidden");
    });

    // Mostrar el contenedor de filtros si hay alguno visible
    if (filtrosPermitidos.size > 0) {
        document.getElementById("filtersContainer").classList.remove("hidden");
        document.getElementById("generateReport").classList.remove("hidden");
    }
}


// Evento para detectar cambios en el select de reportes
document.getElementById("reportType").addEventListener("change", function() {
    const reporteSeleccionado = this.value;

    if (!window.userRoles || window.userRoles.length === 0) {
        console.warn("No se han cargado los roles del usuario.");
        return;
    }

    mostrarFiltros(reporteSeleccionado);
});


async function cargarUsuario() {

    try {
        const response = await fetch("/admin/get_user_info");
        console.log("Response recibida:", response);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const userData = await response.json();
        console.log("Datos del usuario:", userData);

        // Guardamos roles y área en variables globales
        window.userRoles = userData.roles || [];
        window.userDepartmentId = userData.department_id;

        console.log("Roles del usuario almacenados:", window.userRoles);
    } catch (error) {
        console.error("Error en cargarUsuario():", error);
    }
}


async function cargarAreasRoles() {
    const areasResponse = await fetch("/admin/get_areas");
    const rolesResponse = await fetch("/admin/get_roles");

    const areas = await areasResponse.json();
    const roles = await rolesResponse.json();
    console.log("Estos son las areas:", areas);
    console.log("Estos son los roles:", roles);
    const areaSelect = document.getElementById("areaFilter");
    const roleSelect = document.getElementById("roleFilter");

    areas.forEach(area => {
        areaSelect.innerHTML += `<option value="${area.id}">${area.name}</option>`;
    });

    roles.forEach(role => {
        roleSelect.innerHTML += `<option value="${role.id}">${role.name}</option>`;
    });
}

async function cargarEmpleados() {
    const areaFilter = document.getElementById("areaFilter");
    const roleFilter = document.getElementById("roleFilter");

    let areaId = areaFilter.value;
    let roleId = roleFilter.value;
    console.log(window.userRoles)
    // 💡 Asegurar que window.userRoles está definido
    if (!window.userRoles || !Array.isArray(window.userRoles)) {
        console.error("❌ Error: window.userRoles no está definido o no es un array");
        return;
    }

    // Si el usuario es Jefe de Área y NO es Admin General ni RRHH
    if (
        window.userRoles.includes("jefe de area") &&
        !window.userRoles.includes("administrador general") &&
        !window.userRoles.includes("recursos humanos")
    ) {
        areaId = window.userDepartmentId; // Se fuerza el área del usuario
        areaFilter.value = areaId; // Se muestra el área correcta en el select
        areaFilter.disabled = true; // Se bloquea la edición del área
    }

    let url = `/admin/get_employees?`;
    if (areaId !== "all") url += `area_id=${areaId}&`;
    if (roleId !== "all") url += `role_id=${roleId}`;

    try {
        const response = await fetch(url);
        const employees = await response.json();

        const employeeSelect = document.getElementById("employeeFilter");
        employeeSelect.innerHTML = `<option value="all">Todos</option>`; // Reset

        employees.forEach(emp => {
            employeeSelect.innerHTML += `<option value="${emp.id}">${emp.name}</option>`;
        });
    } catch (error) {
        console.error("Error al cargar empleados:", error);
    }
}


document.getElementById("areaFilter").addEventListener("change", cargarEmpleados);
document.getElementById("roleFilter").addEventListener("change", cargarEmpleados);
document.addEventListener("DOMContentLoaded", async function () {
    console.log("El DOM está completamente cargado");
    await cargarUsuario();  // Llamamos a la función cuando el HTML ya está listo
    cargarEmpleados();
    cargarAreasRoles();
});



document.getElementById("generateReport").addEventListener("click", async function() {
    const reportType = document.getElementById("reportType").value;
    const areaFilter = document.getElementById("areaFilter").value;
    const roleFilter = document.getElementById("roleFilter").value;
    const employeeFilter = document.getElementById("employeeFilter").value;
    const startDate = document.getElementById("startDate").value;
    const endDate = document.getElementById("endDate").value;
    const statusFilter = document.getElementById("statusFilter").value;

    const params = {
        reportType,
        areaFilter,
        roleFilter,
        employeeFilter,
        startDate,
        endDate,
        statusFilter
    };

    try {
        const response = await fetch("/reporting/generate_report", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(params)
        });

        const data = await response.json();

        if (response.ok) {
            console.log("Reporte generado:", data);
            mostrarReporte(data); // Función para renderizar los datos en el frontend
        } else {
            console.error("Error al generar el reporte:", data.error);
        }

    } catch (error) {
        console.error("Error en la solicitud:", error);
    }
});

function mostrarReporte(data) {
    const reportResults = document.getElementById("reportResults");
    reportResults.innerHTML = "<h3>Resultados del Reporte</h3>";

    if (data.length === 0) {
        reportResults.innerHTML += "<p>No hay datos para mostrar.</p>";
        return;
    }

    let table = "<table border='1'><tr>";
    for (let key in data[0]) {
        table += `<th>${key}</th>`;
    }
    table += "</tr>";

    data.forEach(row => {
        table += "<tr>";
        for (let key in row) {
            table += `<td>${row[key]}</td>`;
        }
        table += "</tr>";
    });

    table += "</table>";
    reportResults.innerHTML += table;
}

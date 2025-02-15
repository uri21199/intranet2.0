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
            "jefe de area": ["employeeFilterContainer"]
        }
    },
    "trainings": {
        roles: {
            "administrador general": ["dateRangeContainer", "statusFilterContainer"],
            "recursos humanos": ["dateRangeContainer", "statusFilterContainer"]
        }
    },
    "trainings_list": {
        roles: {
            "administrador general": ["dateRangeContainer", "statusFilterContainer"],
            "recursos humanos": ["dateRangeContainer", "statusFilterContainer"]
        }
    },
    "salary_receipts": {
        roles: {
            "administrador general": ["dateRangeContainer", "statusFilterContainer"],
            "recursos humanos": ["dateRangeContainer", "statusFilterContainer"]
        }
    },
    "equipments": {
        roles: {
            "administrador general": ["dateRangeContainer", "statusFilterContainer"],
            "recursos humanos": ["dateRangeContainer", "statusFilterContainer"]
        }
    },
    "room_reservations": {
        roles: {
            "administrador general": ["dateRangeContainer", "statusFilterContainer"],
            "recursos humanos": ["dateRangeContainer", "statusFilterContainer"]
        }
    },
    "document_versions": {
        roles: {
            "administrador general": ["dateRangeContainer", "statusFilterContainer"],
            "recursos humanos": ["dateRangeContainer", "statusFilterContainer"]
        }
    },
    "access_logs": {
        roles: {
            "administrador general": ["dateRangeContainer", "statusFilterContainer"],
            "recursos humanos": ["dateRangeContainer", "statusFilterContainer"]
        }
    },
    "system_tickets": {
        roles: {
            "administrador general": ["dateRangeContainer", "statusFilterContainer", "areaFilterContainer"],
            "recursos humanos": ["dateRangeContainer", "statusFilterContainer"],
            "soporte tecnico": ["dateRangeContainer", "statusFilterContainer"]
        }
    }
};


function mostrarFiltros(reporteSeleccionado) {
    // Ocultamos todos los filtros
    document.querySelectorAll("#filtersContainer .form-group").forEach(el => el.classList.add("hidden"));

    if (!reportFilters[reporteSeleccionado]) return;

    // Obtener los filtros asociados a ese reporte
    const filtros = reportFilters[reporteSeleccionado].filters;
    
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
console.log("Esto es previo a cargarUsuario()")

async function cargarUsuario() {
    console.log("Ejecutando cargarUsuario()...");

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
document.addEventListener("DOMContentLoaded", function () {
    console.log("El DOM está completamente cargado");
    cargarUsuario();  // Llamamos a la función cuando el HTML ya está listo
    cargarEmpleados();
    cargarAreasRoles();
});

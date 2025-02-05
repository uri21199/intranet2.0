function updateFilters() {
    const reportType = document.getElementById("reportType").value;
    const filterTypeContainer = document.getElementById("filterTypeContainer");
    const filterType = document.getElementById("filterType");
    const subFilterContainer = document.getElementById("subFilterContainer");
    const subFilter = document.getElementById("subFilter");

    // Limpiar valores anteriores
    filterType.innerHTML = "";
    subFilter.innerHTML = "";
    subFilterContainer.classList.add("hidden");

    if (!reportType) {
        filterTypeContainer.classList.add("hidden");
        return;
    }

    let filters = [];
    
    if (reportType === "employees_status") {
        filters = [
            { value: "none", text: "Sin filtro" },
            { value: "active", text: "Empleados activos" },
            { value: "inactive", text: "Empleados inactivos" },
            { value: "area", text: "Empleados de un área" }
        ];
    } else if (reportType === "requested_days") {
        filters = [
            { value: "none", text: "Sin filtro" },
            { value: "area", text: "Empleados de un área" },
            { value: "day_type", text: "Por tipo de día" }
        ];
    } else if (reportType === "trainings") {
        filters = [
            { value: "none", text: "Sin filtro" },
            { value: "area", text: "Capacitaciones por área" },
            { value: "role", text: "Por rol" },
            { value: "status", text: "Por estado" }
        ];
    }

    filters.forEach(option => {
        let opt = document.createElement("option");
        opt.value = option.value;
        opt.textContent = option.text;
        filterType.appendChild(opt);
    });

    filterTypeContainer.classList.remove("hidden");
}

function updateSubFilters() {
    const filterType = document.getElementById("filterType").value;
    const subFilterContainer = document.getElementById("subFilterContainer");
    const subFilter = document.getElementById("subFilter");

    subFilter.innerHTML = "";
    
    let subFilters = [];

    if (filterType === "area") {
        subFilters = [
            { value: "HR", text: "Recursos Humanos" },
            { value: "IT", text: "IT" },
            { value: "Finance", text: "Finanzas" }
        ];
    } else if (filterType === "day_type") {
        subFilters = [
            { value: "vacaciones", text: "Vacaciones" },
            { value: "ausencia", text: "Ausencia" },
            { value: "home_office", text: "Home Office" }
        ];
    } else if (filterType === "role") {
        subFilters = [
            { value: "admin", text: "Administrador" },
            { value: "supervisor", text: "Supervisor" },
            { value: "empleado", text: "Empleado" }
        ];
    } else if (filterType === "status") {
        subFilters = [
            { value: "completado", text: "Completado" },
            { value: "pendiente", text: "Pendiente" }
        ];
    } else {
        subFilterContainer.classList.add("hidden");
        return;
    }

    subFilters.forEach(option => {
        let opt = document.createElement("option");
        opt.value = option.value;
        opt.textContent = option.text;
        subFilter.appendChild(opt);
    });

    subFilterContainer.classList.remove("hidden");
}

    function generateReport() {
        alert("Generando reporte...");
    }
document.addEventListener("DOMContentLoaded", function () {
    const roomSelect = document.getElementById("typeRoom");
    const clientSection = document.getElementById("clientSection");
    const reasonSection = document.getElementById("reasonSection");
    const clientSelect = document.getElementById("client");
    
    function cargarSalas() {
        console.log("📡 Solicitando salas...");
        fetch("/admin/get_rooms")
            .then(response => {
                console.log("🔍 Estado de la respuesta:", response.status);
                return response.json();
            })
            .then(data => {
                console.log("📥 Datos recibidos:", data);
                roomSelect.innerHTML = "<option value=''>Elija una sala</option>";
                data.forEach(room => {
                    const option = document.createElement("option");
                    option.value = room.id;
                    option.textContent = room.name;
                    roomSelect.appendChild(option);
                });
            })
            .catch(error => console.error("❌ Error cargando salas:", error));
    }
    


    function cambiarFormulario() {
        const selectedRoom = roomSelect.value;
        if (selectedRoom === "2") {
            clientSection.style.display = "block";
            reasonSection.style.display = "block";
            cargarClientes();
        } else {
            clientSection.style.display = "none";
            reasonSection.style.display = "none";
        }
    }

    function cargarClientes() {
        fetch("/admin/get_clients")
            .then(response => response.json())
            .then(data => {
                clientSelect.innerHTML = "";
                data.forEach(client => {
                    const option = document.createElement("option");
                    option.value = client.id;
                    option.textContent = client.name;
                    clientSelect.appendChild(option);
                });
            })
            .catch(error => console.error("Error cargando clientes:", error));
    }

    window.enviarSolicitud = function () {
        const formData = {
            room_id: roomSelect.value,
            reserved_by: 1,  // Este ID debe obtenerse dinámicamente
            client_id: clientSection.style.display === "block" ? clientSelect.value : null,
            use: "Reservación de sala",
            justification: reasonSection.style.display === "block" ? document.getElementById("reason").value : "",
            reservation_date: document.getElementById("date").value,
            start_time: document.getElementById("start_time").value,
            end_time: document.getElementById("end_time").value
        };

        fetch("/rooms/create_reservation", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => alert(data.message || data.error))
        .catch(error => console.error("Error en la reserva:", error));
    };
    cargarSalas();
    cargarClientes();
    roomSelect.addEventListener("change", cambiarFormulario);
});

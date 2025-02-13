document.getElementById("settingsForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Evita el envío tradicional del formulario

    const formData = {
        currentPassword: document.getElementById("currentPassword").value,
        newPassword: document.getElementById("newPassword").value,
        confirmPassword: document.getElementById("confirmPassword").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        state: document.getElementById("state").value,
        city: document.getElementById("city").value,
        address: document.getElementById("address").value
    };

    console.log("📤 Enviando datos al servidor:", formData); // Verificar qué valores se están enviando

    try {
        const response = await fetch("/settings/update", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        });

        console.log("Response Status:", response.status); // Ver el código de respuesta HTTP

        const result = await response.json();
        console.log("Response Data:", result); // Ver el contenido de la respuesta en la consola

        alert(result.message); // Mostrar mensaje de respuesta

    } catch (error) {
        console.error("Error al actualizar la configuración:", error);
        alert("Ocurrió un error al actualizar los datos.");
    }
});



async function fetchUserData() {
    try {
        const response = await fetch("/settings/user-info");
        console.log("Response Status:", response.status); // Ver el código de respuesta HTTP
        
        if (!response.ok) {
            const errorMessage = await response.json();
            console.error("Error en la respuesta:", errorMessage);
            throw new Error(errorMessage.message || "Error al obtener los datos del usuario.");
        }

        const userData = await response.json();
        console.log("Datos del usuario:", userData); // Ver los datos en la consola

        // Rellenar los campos con los datos del usuario
        document.getElementById("email").value = userData.email || "";
        document.getElementById("phone").value = userData.phone || "";
        document.getElementById("state").value = userData.state || "";
        document.getElementById("city").value = userData.city || "";
        document.getElementById("address").value = userData.address || "";

    } catch (error) {
        console.error("Error capturado:", error);
        alert("No se pudo obtener la información del usuario.");
    }
}

// Llamamos a la función cuando la página cargue
document.addEventListener("DOMContentLoaded", fetchUserData);

-- ESQUEMA CAPACITACIONES
--DROP SCHEMA IF EXISTS trainings;
CREATE SCHEMA trainings;
-- ESQUEMA DOCUMENTOS
--DROP SCHEMA IF EXISTS documents;
CREATE SCHEMA documents;
-- ESQUEMA TICKETS
--DROP SCHEMA IF EXISTS tickets;
CREATE SCHEMA tickets;
-- ESQUEMA SALAS
--DROP SCHEMA IF EXISTS rooms;
CREATE SCHEMA rooms;
-- ESQUEMA LOGS
--DROP SCHEMA IF EXISTS logs;
CREATE SCHEMA logs;
-- ESQUEMA GENERAL
--DROP SCHEMA IF EXISTS general;
CREATE SCHEMA general;
-- ESQUEMA ENCUESTAS
--DROP SCHEMA IF EXISTS surveys;
CREATE SCHEMA surveys;
-- ESQUEMA RECURSOS HUMANOS
--DROP SCHEMA IF EXISTS hr;
CREATE SCHEMA hr;


CREATE TABLE general.roles (
    id SERIAL PRIMARY KEY, -- Identificador único del rol
    name VARCHAR(100) NOT NULL, -- Nombre del rol
    description TEXT, -- Descripción del rol
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Fecha de última actualización
);

CREATE TABLE general.departments (
    id SERIAL PRIMARY KEY, -- Identificador único
    name VARCHAR(100) NOT NULL, -- Nombre del departamento o área
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Fecha de última actualización
);


CREATE TABLE general.day_types (
    id SERIAL PRIMARY KEY, -- Identificador único del tipo de día
    name VARCHAR(100) NOT NULL, -- Nombre del tipo de día
    requires_file BOOLEAN DEFAULT FALSE, -- Indica si requiere un archivo justificativo
    description TEXT, -- Descripción del tipo de día
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Fecha de última actualización
);


CREATE TABLE rooms.rooms (
    id SERIAL PRIMARY KEY, -- Identificador único de la sala
    name VARCHAR(150) NOT NULL, -- Nombre de la sala
    capacity INT NOT NULL, -- Capacidad máxima de la sala
    location VARCHAR(255), -- Ubicación de la sala (puede ser NULL)
    description TEXT, -- Descripción de la sala (opcional)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Última fecha de actualización
);


CREATE TABLE general.clients (
    id SERIAL PRIMARY KEY, -- Identificador único del cliente
    name VARCHAR(150) NOT NULL, -- Nombre del cliente
    country VARCHAR(100), -- País del cliente
    main_contact VARCHAR(150), -- Nombre del contacto principal
    phone VARCHAR(50), -- Teléfono de contacto
    email VARCHAR(150), -- Email del contacto principal
    active BOOLEAN DEFAULT TRUE, -- Estado del cliente (activo o inactivo)
    services TEXT, -- Servicios contratados o asociados
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Fecha de última actualización
);


CREATE TABLE hr.employees (
    id SERIAL PRIMARY KEY,
    tax_id VARCHAR(100) NOT NULL, -- CUIT
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    hire_date DATE NOT NULL,
    record_number INT NOT NULL, -- Legajo
    gender VARCHAR(5),
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    state VARCHAR(100), -- Provincia
    city VARCHAR(100), -- Localidad
    address VARCHAR(100),
    union_agreement BOOLEAN DEFAULT TRUE NOT NULL, -- Convenio
    health_insurance BOOLEAN DEFAULT TRUE NOT NULL, -- Prepaga
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Última fecha de actualización
    department_id INT, -- Relación con tabla de Áreas
    active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (department_id) REFERENCES general.departments (id) ON DELETE SET NULL -- Relación opcional con Áreas
);

CREATE TABLE tickets.ticket_categories (
    id SERIAL PRIMARY KEY, -- Identificador único de la categoría
    name VARCHAR(100) NOT NULL, -- Nombre de la categoría
    description TEXT, -- Descripción de la categoría
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Fecha de última actualización
);


CREATE TABLE tickets.ticket_subcategories (
    id SERIAL PRIMARY KEY, -- Identificador único de la subcategoría
    category_id INT NOT NULL, -- Relación con la tabla Ticket_Categories
    name VARCHAR(100) NOT NULL, -- Nombre de la subcategoría
    description TEXT, -- Descripción de la subcategoría
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de última actualización
    FOREIGN KEY (category_id) REFERENCES tickets.ticket_categories (id) ON DELETE CASCADE -- Relación con Ticket_Categories
);



CREATE TABLE general.permissions (
    id SERIAL PRIMARY KEY, -- Identificador único del permiso
    permission_name VARCHAR(150) NOT NULL, -- Nombre del permiso
    role_id INT NOT NULL, -- Relación con la tabla Roles
    active BOOLEAN DEFAULT TRUE, -- Estado del permiso (activo o inactivo)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de última actualización
    FOREIGN KEY (role_id) REFERENCES general.roles (id) ON DELETE CASCADE -- Relación con Roles
);


CREATE TABLE hr.employee_roles (
    id SERIAL PRIMARY KEY, -- Identificador único de la relación
    employee_id INT NOT NULL, -- Relación con la tabla Employees
    role_id INT NOT NULL, -- Relación con la tabla Roles
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    FOREIGN KEY (employee_id) REFERENCES hr.employees (id) ON DELETE CASCADE, -- Relación con Employees
    FOREIGN KEY (role_id) REFERENCES general.roles (id) ON DELETE CASCADE -- Relación con Roles
);


CREATE TABLE general.employee_areas (
    id SERIAL PRIMARY KEY, -- Identificador único de la relación
    user_id INT NOT NULL, -- Relación con la tabla Employees
    area_id INT NOT NULL, -- Relación con la tabla Departments
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    FOREIGN KEY (user_id) REFERENCES hr.employees (id) ON DELETE CASCADE, -- Relación con Employees
    FOREIGN KEY (area_id) REFERENCES general.departments (id) ON DELETE CASCADE -- Relación con Departments
);


CREATE TABLE rooms.room_reservations (
    id SERIAL PRIMARY KEY, -- Identificador único de la reserva
    room_id INT NOT NULL, -- Relación con la tabla Rooms
    reserved_by INT NOT NULL, -- Empleado que realizó la reserva
    client_id INT, -- Relación con la tabla Clients (opcional, si la reserva es para un cliente)
	use VARCHAR(100) DEFAULT 'Capacitación',
    justification TEXT, -- Justificación del uso de la sala
    status VARCHAR(50) DEFAULT 'Pending', -- Estado de la reserva (Pending, Approved, Rejected, etc.)
    authorized_by INT, -- Relación con el empleado que aprobó la reserva
    reservation_date DATE NOT NULL, -- Fecha de la reserva
    start_time TIME NOT NULL, -- Hora de inicio
    end_time TIME NOT NULL, -- Hora de fin
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Última fecha de actualización
    FOREIGN KEY (room_id) REFERENCES rooms.rooms (id) ON DELETE CASCADE, -- Relación con la tabla Rooms
    FOREIGN KEY (reserved_by) REFERENCES hr.employees (id) ON DELETE SET NULL, -- Relación con quien reservó
    FOREIGN KEY (client_id) REFERENCES general.clients (id) ON DELETE SET NULL, -- Relación con el cliente (si aplica)
    FOREIGN KEY (authorized_by) REFERENCES hr.employees (id) ON DELETE SET NULL -- Relación con el empleado que autorizó la reserva
);

CREATE TABLE hr.equipment (
    id SERIAL PRIMARY KEY, -- Identificador único
    equipment_type VARCHAR(100) NOT NULL, -- Tipo de equipo (ejemplo: Laptop, Desktop, Monitor)
    equipment_id VARCHAR(100) NOT NULL UNIQUE, -- Identificador del equipo (ejemplo: código interno)
    status VARCHAR(50) DEFAULT 'Available', -- Estado del equipo (ejemplo: Available, Assigned, Maintenance)
    location VARCHAR(100), -- Ubicación del equipo (puede ser NULL)
    user_id INT, -- Relación con la tabla Employees (usuario actual del equipo)
    anydesk VARCHAR(100), -- ID de AnyDesk del equipo
    serial_number VARCHAR(100), -- Número de serie del equipo
    brand VARCHAR(100), -- Marca del equipo
    model VARCHAR(100), -- Modelo del equipo
    file_path TEXT, -- Ruta del archivo relacionado (por ejemplo, ficha técnica)
    area_id INT, -- Relación con la tabla Departments (área asociada al equipo)
    client_id INT, -- Relación con la tabla Clients (si el equipo está asociado a un cliente)
    comments TEXT, -- Comentarios adicionales sobre el equipo
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de última actualización
    FOREIGN KEY (user_id) REFERENCES hr.employees (id) ON DELETE SET NULL, -- Relación con Employees
    FOREIGN KEY (area_id) REFERENCES general.departments (id) ON DELETE SET NULL, -- Relación con Departments
    FOREIGN KEY (client_id) REFERENCES general.clients (id) ON DELETE SET NULL -- Relación con Clients
);


CREATE TABLE hr.lunch_schedules (
    id SERIAL PRIMARY KEY, -- Identificador único del horario
    employee_id INT NOT NULL, -- Relación con la tabla Employees
    day_of_week VARCHAR(20) NOT NULL, -- Día de la semana (ejemplo: "Lunes", "Martes")
    start_time TIME NOT NULL, -- Hora de inicio del almuerzo
    end_time TIME NOT NULL, -- Hora de fin del almuerzo
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de última actualización
    FOREIGN KEY (employee_id) REFERENCES hr.employees (id) ON DELETE CASCADE -- Relación con Employees
);

CREATE TABLE hr.credentials (
    id SERIAL PRIMARY KEY, -- Identificador único
    employee_id INT NOT NULL, -- Relación con la tabla Employees
    cuil VARCHAR(20) NOT NULL UNIQUE, -- CUIL del empleado
    password VARCHAR(255) NOT NULL, -- Contraseña (debe almacenarse encriptada)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de última actualización
    FOREIGN KEY (employee_id) REFERENCES hr.employees (id) ON DELETE CASCADE -- Relación con Employees
);

CREATE TABLE documents.documents (
    id SERIAL PRIMARY KEY, -- Identificador único del documento
    title VARCHAR(150) NOT NULL, -- Título del documento
    description TEXT, -- Descripción del documento
    file_path TEXT NOT NULL, -- Ruta donde está almacenado el archivo
    document_type VARCHAR(50) NOT NULL, -- Tipo de documento (ej. "Manual", "Política", etc.)
    created_by INT NOT NULL, -- Empleado que creó el documento
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de última modificación
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación del registro
    FOREIGN KEY (created_by) REFERENCES hr.employees (id) ON DELETE SET NULL -- Relación con tabla Employees
);

CREATE TABLE documents.document_versions (
    id SERIAL PRIMARY KEY, -- Identificador único de la versión
    document_id INT NOT NULL, -- Relación con la tabla Documents
    version_number INT NOT NULL, -- Número de versión del documento
    file_path TEXT NOT NULL, -- Ruta donde se almacena esta versión
    created_by INT NOT NULL, -- Relación con la tabla Employees (quién creó esta versión)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación de la versión
    FOREIGN KEY (document_id) REFERENCES documents.documents (id) ON DELETE CASCADE, -- Relación con Documents
    FOREIGN KEY (created_by) REFERENCES hr.employees (id) ON DELETE SET NULL -- Relación con Employees
);

CREATE TABLE documents.document_roles (
    id SERIAL PRIMARY KEY, -- Identificador único de la relación
    document_id INT NOT NULL, -- Relación con la tabla Documents
    role_id INT NOT NULL, -- Relación con la tabla Roles
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    FOREIGN KEY (document_id) REFERENCES documents.documents (id) ON DELETE CASCADE, -- Relación con Documents
    FOREIGN KEY (role_id) REFERENCES general.roles (id) ON DELETE CASCADE -- Relación con Roles
);


CREATE TABLE documents.document_areas (
    id SERIAL PRIMARY KEY, -- Identificador único de la relación
    document_id INT NOT NULL, -- Relación con la tabla Documents
    department_id INT NOT NULL, -- Relación con la tabla Departments
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    FOREIGN KEY (document_id) REFERENCES documents.documents (id) ON DELETE CASCADE, -- Relación con Documents
    FOREIGN KEY (department_id) REFERENCES general.departments (id) ON DELETE CASCADE -- Relación con Departments
);

CREATE TABLE tickets.system_tickets (
    id SERIAL PRIMARY KEY, -- Identificador único del ticket
    employee_id INT NOT NULL, -- Relación con la tabla Employees (quién crea el ticket)
    category_id INT NOT NULL, -- Relación con la tabla Ticket_Categories
    subcategory_id INT, -- Relación con la tabla Ticket_Subcategories (opcional)
    description TEXT NOT NULL, -- Descripción del problema
    status VARCHAR(50) DEFAULT 'Open', -- Estado del ticket (Open, In Progress, Closed)
    assigned_to INT, -- Relación con la tabla Employees (quién gestiona el ticket)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    closed_at TIMESTAMP, -- Fecha de cierre (puede ser NULL si está abierto)
    FOREIGN KEY (employee_id) REFERENCES hr.employees (id) ON DELETE CASCADE, -- Relación con Employees
    FOREIGN KEY (category_id) REFERENCES tickets.ticket_categories (id) ON DELETE CASCADE, -- Relación con Ticket_Categories
    FOREIGN KEY (subcategory_id) REFERENCES tickets.ticket_subcategories (id) ON DELETE SET NULL, -- Relación con Ticket_Subcategories
    FOREIGN KEY (assigned_to) REFERENCES hr.employees (id) ON DELETE SET NULL -- Relación con Employees
);

CREATE TABLE tickets.ticket_updates (
    id SERIAL PRIMARY KEY, -- Identificador único de la actualización
    ticket_id INT NOT NULL, -- Relación con la tabla System_Tickets
    updated_by INT NOT NULL, -- Relación con la tabla Employees (quién realizó la actualización)
    description TEXT NOT NULL, -- Descripción de la actualización
    previous_status VARCHAR(50), -- Estado anterior del ticket
    current_status VARCHAR(50) NOT NULL, -- Estado actual del ticket
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora de la actualización
    FOREIGN KEY (ticket_id) REFERENCES tickets.system_tickets (id) ON DELETE CASCADE, -- Relación con System_Tickets
    FOREIGN KEY (updated_by) REFERENCES hr.employees (id) ON DELETE SET NULL -- Relación con Employees
);

CREATE TABLE tickets.ticket_files (
    id SERIAL PRIMARY KEY, -- Identificador único del archivo
    ticket_id INT NOT NULL, -- Relación con la tabla System_Tickets
    file_name VARCHAR(150) NOT NULL, -- Nombre del archivo
    file_path TEXT NOT NULL, -- Ruta donde se almacena el archivo
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de carga del archivo
    FOREIGN KEY (ticket_id) REFERENCES tickets.system_tickets (id) ON DELETE CASCADE -- Relación con System_Tickets
);

CREATE TABLE documents.files (
    id SERIAL PRIMARY KEY, -- Identificador único del archivo
    file_name VARCHAR(150) NOT NULL, -- Nombre del archivo
    file_path TEXT NOT NULL, -- Ruta donde está almacenado el archivo
    request_id INT NOT NULL, -- Relación con la tabla Dias_Solicitados
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Fecha y hora de carga
);

CREATE TABLE hr.requested_days (
    id SERIAL PRIMARY KEY, -- Identificador único
    employee_id INT NOT NULL, -- Relación con la tabla Employees
    day_type_id INT NOT NULL, -- Relación con la tabla Day_Types
    start_date DATE NOT NULL, -- Fecha de inicio del día solicitado
    end_date DATE NOT NULL, -- Fecha de fin del día solicitado
    reason TEXT, -- Motivo de la solicitud
    status VARCHAR(50) DEFAULT 'Pending', -- Estado de la solicitud (ejemplo: Pending, Approved, Rejected)
    file_id INT, -- Relación con la tabla Files (si requiere justificativo)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de última actualización
    FOREIGN KEY (employee_id) REFERENCES hr.employees (id) ON DELETE CASCADE, -- Relación con Employees
    FOREIGN KEY (day_type_id) REFERENCES general.day_types (id) ON DELETE CASCADE, -- Relación con Day_Types
    FOREIGN KEY (file_id) REFERENCES documents.files (id) ON DELETE SET NULL -- Relación con Files
);

CREATE TABLE hr.salary_receipts (
    id SERIAL PRIMARY KEY, -- Identificador único del recibo
    employee_id INT NOT NULL, -- Relación con la tabla Employees
    month INT NOT NULL, -- Mes del recibo (1-12)
    year INT NOT NULL, -- Año del recibo
    amount NUMERIC(12, 2) NOT NULL, -- Monto del recibo
    signed BOOLEAN DEFAULT FALSE, -- Indica si el recibo ha sido firmado
    file_path TEXT, -- Ruta del archivo del recibo
    signature_date TIMESTAMP, -- Fecha en que se firmó el recibo (puede ser NULL)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de última actualización
    FOREIGN KEY (employee_id) REFERENCES hr.employees (id) ON DELETE CASCADE -- Relación con Employees
);

CREATE TABLE logs.audit_receipts (
    id SERIAL PRIMARY KEY, -- Identificador único de la auditoría
    receipt_id INT NOT NULL, -- Relación con la tabla Recibos
    action VARCHAR(50) NOT NULL, -- Acción realizada (ejemplo: "Crear", "Actualizar", "Eliminar")
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora de la acción
    employee_id INT NOT NULL, -- Relación con la tabla Employees (quién realizó la acción)
    FOREIGN KEY (receipt_id) REFERENCES hr.salary_receipts (id) ON DELETE CASCADE, -- Relación con Recibos
    FOREIGN KEY (employee_id) REFERENCES hr.employees (id) ON DELETE SET NULL -- Relación con Employees
);

CREATE TABLE surveys.surveys (
    id SERIAL PRIMARY KEY, -- Identificador único de la encuesta
    title VARCHAR(150) NOT NULL, -- Título de la encuesta
    description TEXT, -- Descripción de la encuesta
    start_date DATE NOT NULL, -- Fecha de inicio de la encuesta
    end_date DATE NOT NULL, -- Fecha de fin de la encuesta
    status VARCHAR(50) DEFAULT 'Active', -- Estado de la encuesta (Active, Closed, etc.)
    created_by INT NOT NULL, -- Relación con la tabla Employees (quien crea la encuesta)
    responses_count INT DEFAULT 0, -- Cantidad de respuestas registradas
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación del registro
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Última fecha de actualización
    FOREIGN KEY (created_by) REFERENCES hr.employees (id) ON DELETE SET NULL -- Relación con el creador
);

CREATE TABLE surveys.survey_questions (
    id SERIAL PRIMARY KEY, -- Identificador único de la pregunta
    survey_id INT NOT NULL, -- Relación con la tabla Surveys
    question_text TEXT NOT NULL, -- Texto de la pregunta
    question_type VARCHAR(50) NOT NULL, -- Tipo de pregunta (Texto, Selección, Escala, etc.)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    FOREIGN KEY (survey_id) REFERENCES surveys.surveys (id) ON DELETE CASCADE -- Relación con Surveys
);

CREATE TABLE surveys.survey_responses (
    id SERIAL PRIMARY KEY, -- Identificador único de la respuesta
    survey_id INT NOT NULL, -- Relación con la tabla Surveys
    employee_id INT NOT NULL, -- Relación con la tabla Employees (quien responde)
    response TEXT NOT NULL, -- Respuesta del empleado
    response_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de la respuesta
    FOREIGN KEY (survey_id) REFERENCES surveys.surveys (id) ON DELETE CASCADE, -- Relación con Surveys
    FOREIGN KEY (employee_id) REFERENCES hr.employees (id) ON DELETE CASCADE -- Relación con Employees
);

CREATE TABLE surveys.survey_roles (
    id SERIAL PRIMARY KEY, -- Identificador único de la relación
    survey_id INT NOT NULL, -- Relación con la tabla Surveys
    role_id INT NOT NULL, -- Relación con la tabla Roles
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    FOREIGN KEY (survey_id) REFERENCES surveys.surveys (id) ON DELETE CASCADE, -- Relación con Surveys
    FOREIGN KEY (role_id) REFERENCES general.roles (id) ON DELETE CASCADE -- Relación con Roles
);

CREATE TABLE surveys.survey_areas (
    id SERIAL PRIMARY KEY, -- Identificador único de la relación
    survey_id INT NOT NULL, -- Relación con la tabla Surveys
    department_id INT NOT NULL, -- Relación con la tabla Departments
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    FOREIGN KEY (survey_id) REFERENCES surveys.surveys (id) ON DELETE CASCADE, -- Relación con Surveys
    FOREIGN KEY (department_id) REFERENCES general.departments (id) ON DELETE CASCADE -- Relación con Departments
);

CREATE TABLE surveys.survey_answers (
    id SERIAL PRIMARY KEY, -- Identificador único de la respuesta
    question_id INT NOT NULL, -- Relación con la tabla Survey_Questions
    employee_id INT NOT NULL, -- Relación con la tabla Employees (quién responde)
    answer_text TEXT, -- Respuesta de texto (si aplica)
    answer_option INT, -- Respuesta seleccionada (si aplica a preguntas de selección)
    response_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de la respuesta
    FOREIGN KEY (question_id) REFERENCES surveys.survey_questions (id) ON DELETE CASCADE, -- Relación con Survey_Questions
    FOREIGN KEY (employee_id) REFERENCES hr.employees (id) ON DELETE CASCADE -- Relación con Employees
);

CREATE TABLE logs.notifications (
    id SERIAL PRIMARY KEY, -- Identificador único de la notificación
    employee_id INT, -- Relación con la tabla Employees (notificación personal)
    role_id INT, -- Relación con la tabla Roles (notificación para un rol)
    department_id INT, -- Relación con la tabla Departments (notificación para un área)
    message TEXT NOT NULL, -- Mensaje de la notificación
    notification_type VARCHAR(50) NOT NULL, -- Tipo de notificación (ejemplo: "Sistema", "Capacitación", etc.)
    status VARCHAR(20) DEFAULT 'Unread', -- Estado de la notificación (Unread, Read)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    FOREIGN KEY (employee_id) REFERENCES hr.employees (id) ON DELETE CASCADE, -- Relación con Employees
    FOREIGN KEY (role_id) REFERENCES general.roles (id) ON DELETE CASCADE, -- Relación con Roles
    FOREIGN KEY (department_id) REFERENCES general.departments (id) ON DELETE CASCADE -- Relación con Departments
);

CREATE TABLE logs.change_history (
    id SERIAL PRIMARY KEY, -- Identificador único del cambio
    table_name VARCHAR(150) NOT NULL, -- Nombre de la tabla donde ocurrió el cambio
    record_id INT NOT NULL, -- Identificador del registro modificado
    action VARCHAR(50) NOT NULL, -- Acción realizada (ejemplo: "Insert", "Update", "Delete")
    changed_by INT NOT NULL, -- Relación con la tabla Employees (quién realizó el cambio)
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora del cambio
    details TEXT, -- Detalles del cambio (puede ser un JSON o texto descriptivo)
    FOREIGN KEY (changed_by) REFERENCES hr.employees (id) ON DELETE SET NULL -- Relación con Employees
);


CREATE TABLE logs.user_logins (
    id SERIAL PRIMARY KEY, -- Identificador único del logueo
    employee_id INT NOT NULL, -- Relación con la tabla Employees
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora del intento de logueo
    success BOOLEAN NOT NULL, -- Indica si el intento fue exitoso
    FOREIGN KEY (employee_id) REFERENCES hr.employees (id) ON DELETE CASCADE -- Relación con Employees
);

CREATE TABLE trainings.trainings (
    id SERIAL PRIMARY KEY, -- Identificador único
    name VARCHAR(150) NOT NULL, -- Nombre de la capacitación
    description TEXT, -- Descripción de la capacitación
    training_date DATE NOT NULL, -- Fecha en la que se realizará la capacitación
    duration_hours INT NOT NULL, -- Duración en horas
    responsible_employee_id INT NOT NULL, -- Empleado responsable de la capacitación
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación del registro
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Última fecha de actualización
    FOREIGN KEY (responsible_employee_id) REFERENCES hr.employees (id) ON DELETE SET NULL -- Relación con tabla Employees
);

CREATE TABLE trainings.trained_employees (
    id SERIAL PRIMARY KEY, -- Identificador único del registro
    employee_id INT NOT NULL, -- Relación con la tabla Employees
    training_id INT NOT NULL, -- Relación con la tabla Trainings
    attendance_date DATE NOT NULL, -- Fecha de asistencia a la capacitación
    observations TEXT, -- Observaciones del capacitador (opcional)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación del registro
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Última fecha de actualización
    FOREIGN KEY (employee_id) REFERENCES hr.employees (id) ON DELETE CASCADE, -- Relación con Employees
    FOREIGN KEY (training_id) REFERENCES trainings.trainings (id) ON DELETE CASCADE -- Relación con Trainings
);

CREATE TABLE trainings.training_materials (
    id SERIAL PRIMARY KEY, -- Identificador único del material
    training_id INT NOT NULL, -- Relación con la tabla Trainings
    material_name VARCHAR(150) NOT NULL, -- Nombre del material
    material_type VARCHAR(50) NOT NULL, -- Tipo de material (PDF, Video, Enlace)
    material_url TEXT, -- Ruta o URL del material
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    FOREIGN KEY (training_id) REFERENCES trainings.trainings (id) ON DELETE CASCADE -- Relación con Trainings
);

CREATE TABLE tickets.abm_requests (
    id SERIAL PRIMARY KEY, -- Identificador único de la solicitud
    employee_id INT NOT NULL, -- Relación con la tabla Employees (quién realiza la solicitud)
    request_type VARCHAR(50) NOT NULL, -- Tipo de solicitud (ejemplo: Alta, Baja, Modificación)
    description TEXT NOT NULL, -- Descripción de la solicitud
    status VARCHAR(50) DEFAULT 'Pending', -- Estado de la solicitud (Pending, Approved, Rejected)
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora de la solicitud
    processed_by INT, -- Relación con la tabla Employees (quién procesó la solicitud)
    FOREIGN KEY (employee_id) REFERENCES hr.employees (id) ON DELETE CASCADE, -- Relación con Employees
    FOREIGN KEY (processed_by) REFERENCES hr.employees (id) ON DELETE SET NULL -- Relación con Employees
);


CREATE TABLE general.department_heads (
    id SERIAL PRIMARY KEY, -- Identificador único de la relación
    department_id INT NOT NULL, -- Relación con la tabla de áreas
    employee_id INT NOT NULL, -- Relación con la tabla de empleados
    start_date DATE NOT NULL, -- Fecha en que el empleado comenzó como jefe del área
    end_date DATE, -- Fecha en que dejó de ser jefe (opcional, puede ser NULL si aún es jefe)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación del registro
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Última fecha de actualización
    FOREIGN KEY (department_id) REFERENCES general.departments (id) ON DELETE CASCADE, -- Relación con áreas
    FOREIGN KEY (employee_id) REFERENCES hr.employees (id) ON DELETE CASCADE -- Relación con empleados
);

CREATE TABLE general.mails (
    id SERIAL PRIMARY KEY, -- Identificador único del mail
    email VARCHAR(150) NOT NULL UNIQUE, -- Dirección de correo
    password VARCHAR(255) NOT NULL, -- Contraseña del correo (debería almacenarse encriptada)
    description TEXT, -- Descripción del uso del correo (opcional)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Fecha de última actualización
);

CREATE TABLE general.areas_mails (
    id SERIAL PRIMARY KEY, -- Identificador único de la relación
    area_id INT NOT NULL, -- Relación con la tabla Departments
    mail_id INT NOT NULL, -- Relación con la tabla Mails
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    FOREIGN KEY (area_id) REFERENCES general.departments (id) ON DELETE CASCADE, -- Relación con la tabla Departments
    FOREIGN KEY (mail_id) REFERENCES general.mails (id) ON DELETE CASCADE -- Relación con la tabla Mails
);



CREATE TABLE general.internal_news (
    id SERIAL PRIMARY KEY, -- Identificador único de la noticia
    title VARCHAR(150) NOT NULL, -- Título de la noticia
    content TEXT NOT NULL, -- Contenido de la noticia
    publication_date DATE NOT NULL, -- Fecha de publicación
    author_id INT NOT NULL, -- Relación con la tabla Employees (autor de la noticia)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Última fecha de actualización
    FOREIGN KEY (author_id) REFERENCES hr.employees (id) ON DELETE SET NULL -- Relación con el empleado autor
);

CREATE TABLE general.news_roles (
    id SERIAL PRIMARY KEY, -- Identificador único de la relación
    news_id INT NOT NULL, -- Relación con la tabla Internal_News
    role_id INT NOT NULL, -- Relación con la tabla Roles
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    FOREIGN KEY (news_id) REFERENCES general.internal_news (id) ON DELETE CASCADE, -- Relación con Internal_News
    FOREIGN KEY (role_id) REFERENCES general.roles (id) ON DELETE CASCADE -- Relación con Roles
);

CREATE TABLE general.news_areas (
    id SERIAL PRIMARY KEY, -- Identificador único de la relación
    news_id INT NOT NULL, -- Relación con la tabla Internal_News
    department_id INT NOT NULL, -- Relación con la tabla Departments
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    FOREIGN KEY (news_id) REFERENCES general.internal_news (id) ON DELETE CASCADE, -- Relación con Internal_News
    FOREIGN KEY (department_id) REFERENCES general.departments (id) ON DELETE CASCADE -- Relación con Departments
);





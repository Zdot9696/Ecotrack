#Documentación Técnica - Proyecto EcoTrack

## 1. Introducción

EcoTrack es una aplicación web diseñada para gestionar y monitorear hábitos ecológicos de los usuarios.  
Cuenta con un frontend interactivo y un backend basado en FastAPI, con persistencia de datos en MongoDB, ofreciendo una solución escalable y moderna para seguimiento personalizado.

---

## 2. Arquitectura del Sistema

- **Frontend:** Aplicación web estática desarrollada en HTML, CSS y JavaScript, que consume las APIs REST del backend.  
- **Backend:** Servicio API REST construido con FastAPI en Python, que expone endpoints para manejo de usuarios, hábitos y consejos.  
- **Base de datos:** MongoDB, base de datos NoSQL orientada a documentos, que almacena toda la información en colecciones flexibles para mejorar rendimiento y escalabilidad.  
- **Despliegue:** El backend y frontend pueden ser desplegados en servicios como Render, Railway o Vercel, utilizando variables de entorno para configuraciones sensibles.

---

## 3. Estructura del Proyecto

```plaintext
/backend
  ├── main.py           # Archivo principal del servidor FastAPI
  ├── models.py         # Modelos de datos con Pydantic y ODMantic/Motor
  ├── database.py       # Configuración y conexión a MongoDB
  ├── routes/           # Endpoints organizados por módulos
  ├── scraping.py       # Módulo para scraping de consejos
  ├── requirements.txt  # Dependencias Python
/frontend
  ├── index.html        # Login y registro
  ├── dashboard.html    # Interfaz principal de usuario
  ├── css/
  │   └── styles.css    # Estilos generales
  ├── js/
      ├── auth.js
      ├── habits.js
      └── consejos.js
```
## 4. Tecnologías Utilizadas

- **Python 3.10+**  
- **FastAPI:** Framework moderno para construir APIs web rápidas y fáciles de mantener.  
- **MongoDB:** Base NoSQL orientada a documentos, que permite almacenamiento flexible con alta escalabilidad.  
- **Motor / ODMantic:** Librerías asíncronas para integración eficiente con MongoDB en Python.  
- **JavaScript, HTML5, CSS3:** Para el frontend.  
- **Fetch API:** Comunicación asíncrona entre frontend y backend.  
- **Uvicorn:** Servidor ASGI para correr la app FastAPI.

---

## 5. Base de Datos

Se utiliza MongoDB para almacenar datos en colecciones:

- **Usuarios:** Datos personales y credenciales.  
- **Hábitos:** Documentos que contienen el nombre, frecuencia, y estado del hábito.  
- **Consejos:** Documentos con textos generados por scraping para sugerencias saludables.

MongoDB permite:

- Estructuras flexibles JSON.  
- Consultas rápidas con índices.  
- Escalabilidad horizontal sencilla.  
- Replicación y alta disponibilidad.

---

## 6. Configuración y Despliegue

- El URI de conexión a MongoDB se define en variables de entorno para seguridad.  
- El backend se ejecuta con Uvicorn, escuchando en un puerto configurable.  
- El frontend es estático y puede ser desplegado en servicios de hosting o CDN.  
- Se recomienda usar MongoDB Atlas o servicio gestionado para producción.  
- Realizar backups automáticos y monitoreo para evitar pérdidas.

---

## 7. Seguridad

- Autenticación basada en tokens JWT almacenados en `localStorage`.  
- Protección de rutas en backend verificando token.  
- Uso de HTTPS obligatorio en producción.  
- Sanitización de datos de entrada y validación con Pydantic.  
- Control de acceso a recursos sensibles.

---

## 8. Funcionalidades Principales

- Registro y login de usuarios.  
- CRUD de hábitos con frecuencias (diaria, semanal, mensual).  
- Visualización dinámica y colorida según frecuencia.  
- Consulta y visualización de consejos saludables extraídos vía scraping.  
- Interfaz intuitiva y responsive para desktop y móvil.

---

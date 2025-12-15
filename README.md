# 📘 Braian Web API

Esta API funciona como backend del sitio web personal y permite administrar todo el contenido que se muestra públicamente:

- Información del usuario  
- Tecnologías utilizadas  
- Proyectos del portfolio  
- Características e información técnica por proyecto
- Imágenes asociadas  
- Relaciones entre entidades  

El diseño está orientado a mantener una estructura clara y cómoda para desarrollar, separando responsabilidades en diferentes capas: **rutas**, **servicios**, **DAOs**, **modelos** y **utilidades**.  

---

## 🧩 Características principales

- Gestión completa tanto del portfolio como de cada proyecto (CRUD). 
- Manejo de imágenes con almacenamiento en disco.
- Autenticación basada en JWT
- Rutas de administración protegidas con access token.

---

## 📡 Endpoints principales

La estructura de los endpoints y métodos HTTP busca seguir los principios de **estilo REST**.

### 🧾 Autenticación
- `POST /login` – Genera Access y Refresh Tokens.  
- `POST /refresh` – Renueva tokens.

---

### 👤 Portfolio
- `GET /portfolio`  
- `POST /portfolio` *(protegido)*  
- `PUT /portfolio` *(protegido)*  
- `PUT /portfolio/{id}/user-photo` *(protegido)*  

---

### 📁 Proyectos
- `GET /project/{id}`  
- `GET /project/{id}/features` *(protegido)*  
- `GET /project/{id}/technical-info` *(protegido)*  
- `GET /project/{id}/images` *(protegido)*  
- `POST /project` *(protegido, con imagen)*  
- `PUT /project/{id}` *(protegido)*  
- `DELETE /project/{id}` *(protegido)*  

---

### 🔧 Tecnologías
- `GET /technology` *(protegido)*  
- `POST /technology` *(protegido, con imagen)*  
- `PUT /technology/{tech_id}` *(protegido)*  
- `DELETE /technology/{tech_id}` *(protegido)*  

---

## 🗄️ Base de datos

Las tablas de la base de datos son:

- **Portfolio**
- **Project**
- **Technology**
- **Feature**
- **TechnicalInfo**
- **ProjectImage**
- **EntityTechnology** (tabla intermedia)
- **Admin**
- **RefreshToken**

Incluye claves foráneas, eliminación en cascada y validaciones integradas.

---

## 📂 Manejo de archivos

La API soporta subida de imágenes para:

- Foto del usuario  
- Iconos de tecnologías  
- Portadas de proyectos  
- Galerías de proyectos  

Las imagenes se almacenan en carpetas locales expuestas a través de `/static`.
Las rutas de subida utilizan **multipart/form-data**, permitiendo enviar metadatos junto con archivos.

---

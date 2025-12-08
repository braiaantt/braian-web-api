# 🚀 Update Server API

## 📌 Descripción breve
Esta API fue diseñada como un servidor liviano de actualizaciones. Como está pensada para operar solo en momentos puntuales, toda la información necesaria —nombre de la aplicación, versiones y ruta del archivo físico— se almacena temporalmente en memoria para simplificar el ciclo de uso.

El objetivo principal es facilitar la distribución de actualizaciones de la aplicación EzWork: cuando necesito publicar una nueva versión, levanto el servidor, registro la aplicación junto con el número de versión y la ubicación del archivo a descargar, y la API se encarga de exponer los metadatos necesarios para que el cliente obtenga la actualización.

---

## ✨ Características principales
- Obtener listado de aplicaciones disponibles.
- Consultar versiones de una aplicación específica.
- Descargar archivos por versión o la última versión disponible.
- Subir aplicaciones nuevas.
- Registrar nuevas versiones de una app existente.

---

# 📡 Endpoints
## 🟢 Estado del servidor
### **GET `/ping`**
Verifica conectividad con el servidor.

---

## 📁 Aplicaciones
### **GET `/apps`**
Obtiene la lista de aplicaciones alojadas en el servidor.

### **GET `/apps/{app_name}`**
Obtiene todas las versiones disponibles de una aplicación específica.

### **POST `/apps`**
Registra una nueva aplicación en el servidor junto con su numero de versión.

---

## 🔄 Versiones de aplicaciones
### **GET `/apps/{app_name}/latest`**
Obtiene el archivo correspondiente a la última versión disponible de una aplicación.

### **GET `/apps/{app_name}/latest/metadata`**
Obtiene información relacionada con la última versión de una aplicación.

### **GET `/apps/{app_name}/{app_version}`**
Obtiene el archivo correspondiente a una versión específica de una aplicación.

### **POST `/apps/{app_name}/versions`**
Agrega una nueva versión a una aplicación ya existente.

---

## 📝 Logging
### **POST `/log`**
Registra un mensaje enviado por el cliente.

---

## 🗂️ Documentación interna adicional
La API incluye:
- Validación automática de datos con modelos Pydantic.
- Manejadores personalizados para errores (`HTTPException`, `ValidationError`, excepciones generales). 
- Devolución de archivos mediante `FileResponse` para descargas directas.

---



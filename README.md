# Gestión de Películas API

Una API para gestionar películas y listas, desarrollada con FastAPI en Python.  
Esta API implementa operaciones CRUD para películas y listas, cuenta con autenticación mediante JWT y utiliza una base de datos SQLite. Además, se integra con una [aplicación Flutter](https://github.com/AngelChv/proyecto_flutter.git) (modo web) que consume la API, mientras que en dispositivos móviles se utiliza una base de datos SQLite local.

## Enlace a la Memoria del Proyecto

Accede a la memoria completa del proyecto en formato PDF:  
[Memoria del Proyecto (PDF)](https://github.com/AngelChv/filmsFastApi/blob/master/Chicote_Veganzones_Angel_Memoria_ProyectoFinal_DAM24.pdf)

---

## Instalación

### Requisitos Previos

- **Python:** Asegúrate de tener instalada una versión reciente de Python (3.x).
- **Librerías Necesarias:** Las dependencias se instalarán mediante `pip` utilizando el archivo `requirements.txt`.
- **Git:** Configura Git en tu sistema y clona el repositorio.

---

### Pasos para Desplegar la API

1. **Clonar el Repositorio:**

   Para clonar el repositorio, ejecuta el siguiente comando en tu terminal:
   ```git clone https://github.com/AngelChv/filmsFastApi.git```
   

2. **Instalación de Dependencias:**

Navega a la carpeta del proyecto y ejecuta:
```pip install -r requirements.txt```


3. **Configuración del Archivo de Configuración:**

Configura el archivo `config.py` (o utiliza el archivo `.env`) con los parámetros necesarios:
- Parámetros de la base de datos.
- Clave secreta para JWT.

4. **Ejecución del Servidor:**

Inicia la API ejecutando el siguiente comando:
```uvicorn main:app --reload```

*También es posible ejecutar la API desde `main.py` directamente.*

---

### Pasos para Desplegar la Aplicación Flutter

1. **Instalación de Flutter y Configuración del IDE:**

Instala Flutter y configura tu entorno de desarrollo con IntelliJ, Android Studio o Visual Studio Code.

2. **Verificar la Instalación de Flutter:**

Ejecuta el siguiente comando para asegurarte de que Flutter está correctamente instalado:

```flutter doctor```

3. **Instalación de un Navegador Compatible:**

Dado que solo se requiere la parte web de la aplicación, asegúrate de tener instalado **Chrome** o **Edge**.

4. **Clonación del Repositorio (Rama `fastApi`):**

Clona el repositorio asegurándote de utilizar la rama `fastApi`:

```git clone https://github.com/AngelChv/proyecto_flutter.git```

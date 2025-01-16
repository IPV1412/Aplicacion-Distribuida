# Juego del Gato Distribuido 🐱

Este proyecto implementa un juego del Gato (Tres en Raya) distribuido utilizando contenedores Docker.
La arquitectura consta de tres contenedores: un servidor y dos clientes (X y O). 
El servidor asigna automáticamente los roles de los jugadores y controla el estado del juego.

## 🛠 Requisitos Previos

- [Docker](https://www.docker.com/get-started) instalado en tu máquina.
- [Docker Compose](https://docs.docker.com/compose/install/) configurado.
- Git instalado en tu máquina.

---

## 📥 Instrucciones de Instalación

### 1. Clonar el Repositorio
Abre una terminal y ejecuta el siguiente comando para clonar el proyecto:
```bash
git clone https://github.com/IPV1412/Aplicacion-Distribuida.git
```

### 2. Navegar al Directorio del Proyecto
```bash
cd Aplicacion-Distribuida
```

### 3. Construir los Contenedores
Ejecuta el siguiente comando para construir las imágenes Docker:
```bash
docker-compose build
```

---

## 🚀 Iniciar el Juego

1. Inicia los contenedores con Docker Compose:
   ```bash
   docker-compose up
   ```

2. Verifica que los contenedores se están ejecutando:
   ```bash
   docker ps
   ```
   Deberías ver tres contenedores activos: `Gato_Servidor`, `Gato_Cliente_1` y `Gato_Cliente_2`.

3. Revisa los logs del servidor para confirmar las conexiones:
   ```bash
   docker logs Gato_Servidor
   ```

---

## 🕹 Cómo Jugar

1. El servidor asignará automáticamente los roles de jugador (`X` y `O`) al primer y segundo cliente que se conecten.
2. En la terminal de cada cliente, ingresa la posición donde deseas jugar (0-8) y observa el tablero actualizado.
3. El juego terminará automáticamente si hay un ganador (`WIN`) o un empate (`DRAW`).

---

## 🧹 Detener los Contenedores
Para detener y eliminar los contenedores creados, utiliza:
```bash
docker-compose down
```

---

## 🗂 Estructura del Proyecto

```
Aplicacion-Distribuida/
├── docker-compose.yml          # Configuración de Docker Compose
├── dockerfile.servidor.dockerfile # Dockerfile del servidor
├── dockerfile.cliente.dockerfile # Dockerfile del cliente
├── Gato_Server.py              # Código del servidor
├── Gato_Cliente.py             # Código del cliente
└── README.md                   # Documentación del proyecto
```

---

## 🤝 Contribuciones

1. Haz un fork de este repositorio.
2. Crea una rama para tu feature o corrección: `git checkout -b mi-feature`.
3. Realiza tus cambios y haz un commit: `git commit -m 'Agregué mi feature'`.
4. Sube tus cambios: `git push origin mi-feature`.
5. Crea un Pull Request.

---

## 📄 Licencia

Este proyecto aprobado por mi :).

---


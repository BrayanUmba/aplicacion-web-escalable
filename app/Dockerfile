# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo los archivos necesarios para instalar las dependencias
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instala wait-for-it para esperar a que la base de datos esté lista
RUN apt-get update && apt-get install -y wait-for-it

# Copia el resto de los archivos de la aplicación
COPY . .

# Exponer el puerto 5000
EXPOSE 5000

# Establece la instrucción de inicio con espera activa a la base de datos
CMD ["wait-for-it", "db:5432", "--", "python", "app.py"]

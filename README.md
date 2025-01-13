# Documentación - Aplicación Web con Monitoreo

## Requisitos Previos
- Docker y Docker Compose
- Kubernetes (Minikube para desarrollo local)
- kubectl
- Cuenta en GitHub
- Cuenta en DockerHub

## Despliegue Rápido

### 1. Configuración Local
```bash
# Clonar repositorio
git clone <url-repositorio>
cd aplicacion-web-escalable

# Iniciar Minikube
minikube start --driver=docker

# Desplegar aplicación
kubectl apply -f k8s/deployment.yaml
```

### 2. Verificar Despliegue
```bash
kubectl get pods
kubectl get services
```

## Componentes Principales

### Base de Datos (PostgreSQL)
- **Credenciales**:
  - Usuario: postgres
  - Contraseña: password
  - Base de datos: mydb
  - Puerto: 5432
- **Almacenamiento**: 1Gi PersistentVolumeClaim

### Aplicación Flask
- 3 réplicas por defecto
- Imagen: brayanumba/flask-app
- Puerto: 5000

### Monitoreo
- **Prometheus**: puerto 9090
- **Grafana**: 
  - Puerto: 3000
  - Usuario: admin
  - Contraseña: admin

## Acceso a la Aplicación

1. Agregar al archivo `/etc/hosts`:
```
127.0.0.1 flask-app.local
127.0.0.1 grafana.local
127.0.0.1 prometheus.local
```

2. Acceder mediante:
- Aplicación: http://flask-app.local
- Grafana: http://grafana.local
- Prometheus: http://prometheus.local

## CI/CD Pipeline

### Configuración Requerida
1. En GitHub, configurar secrets:
   - DOCKER_USERNAME
   - DOCKER_PASSWORD

### Pipeline Ejecuta:
1. Construye imagen Docker
2. Publica en DockerHub
3. Despliega en Kubernetes

## Solución de Problemas

### Verificar Estado
```bash
# Logs de aplicación
kubectl logs deployment/flask-app

# Estado de base de datos
kubectl logs deployment/postgres

# Estado de servicios
kubectl get svc
```

## Seguridad

Acciones requeridas antes de producción:
1. Cambiar todas las contraseñas por defecto
2. Configurar SSL/TLS
3. Implementar respaldos automáticos
4. Configurar políticas de red

## Mantenimiento

### Actualizaciones
```bash
# Actualizar deployment
kubectl apply -f k8s/deployment.yaml

# Escalar aplicación
kubectl scale deployment flask-app --replicas=<número>
```


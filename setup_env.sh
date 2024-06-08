#!/bin/bash

# Instalar virtualenv usando pip3
pip3 install virtualenv

# Crear el entorno virtual llamado .venv
virtualenv .venv

# Activar el entorno virtual
source .venv/bin/activate

Instalar las dependencias desde requirements.txt
if [ -f requirements.txt ]; then
    while IFS= read -r package || [[ -n "$package" ]]; do
        pip3 install "$package" || echo "Error al instalar $package. Continuando con el siguiente paquete..."
    done < requirements.txt
else
    echo "El archivo requirements.txt no existe."
fi

# # Desactivar el entorno virtual
deactivate

echo "El entorno virtual ha sido configurado, y las dependencias y ipykernel han sido instaladas."


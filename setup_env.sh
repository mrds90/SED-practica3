#!/bin/bash

# Instalar virtualenv usando pip3
pip3 install virtualenv

# Crear el entorno virtual llamado .venv
if [ ! -d ".venv" ]; then
    python3 -m virtualenv .venv
fi

# Activar el entorno virtual
source .venv/bin/activate

pip3 install pandas
pip3 install matplotlib

# # Desactivar el entorno virtual
deactivate

echo "El entorno virtual ha sido configurado, y las dependencias y ipykernel han sido instaladas."


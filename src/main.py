import os
import requests
import zipfile
import tarfile
from flask import Flask, request, jsonify
import q1_memory as q1m
import q1_time as q1t
import q2_memory as q2m
import q2_time as q2t
import q3_memory as q3m
import q3_time as q3t

app = Flask(__name__)

def descargar_y_descomprimir(url: str, destino: str) -> str:
    """
    Descarga un archivo desde una URL y lo descomprime en el destino especificado.

    Args:
        url (str): URL del archivo a descargar.
        destino (str): Directorio donde se descomprimirá el archivo.

    Returns:
        str: Ruta del archivo descomprimido.
    """
    archivo_local = os.path.join(destino, url.split("/")[-1])

    # Descargar el archivo
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(archivo_local, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Archivo descargado: {archivo_local}")
    else:
        raise Exception(f"Error al descargar el archivo: {response.status_code}")

    # Verificar y descomprimir el archivo si es necesario
    if zipfile.is_zipfile(archivo_local):
        with zipfile.ZipFile(archivo_local, 'r') as zip_ref:
            zip_ref.extractall(destino)
        return destino
    elif tarfile.is_tarfile(archivo_local):
        with tarfile.open(archivo_local, 'r:*') as tar_ref:
            tar_ref.extractall(destino)
        return destino
    else:
        return archivo_local  # Si no es un archivo comprimido, devolver la ruta

@app.route('/q1/memory', methods=['POST'])
def q1_memory():
    file_path = request.json.get('file_path')
    result = q1m.q1_memory(file_path)
    return jsonify(result), 200

@app.route('/q1/time', methods=['POST'])
def q1_time():
    file_path = request.json.get('file_path')
    result = q1t.q1_time(file_path)
    return jsonify(result), 200

@app.route('/q2/memory', methods=['POST'])
def q2_memory():
    file_path = request.json.get('file_path')
    result = q2m.q2_memory(file_path)
    return jsonify(result), 200

@app.route('/q2/time', methods=['POST'])
def q2_time():
    file_path = request.json.get('file_path')
    result = q2t.q2_time(file_path)
    return jsonify(result), 200

@app.route('/q3/memory', methods=['POST'])
def q3_memory():
    file_path = request.json.get('file_path')
    result = q3m.q3_memory(file_path)
    return jsonify(result), 200

@app.route('/q3/time', methods=['POST'])
def q3_time():
    file_path = request.json.get('file_path')
    result = q3t.q3_time(file_path)
    return jsonify(result), 200

@app.route('/descargar', methods=['POST'])
def descargar():
    data = request.json
    url = data.get('url')
    destino = data.get('destino', '/tmp')
    try:
        ruta = descargar_y_descomprimir(url, destino)
        return jsonify({"ruta": ruta}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

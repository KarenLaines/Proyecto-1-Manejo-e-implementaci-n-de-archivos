import datetime
import os


def read_gif_info(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()

        info = {}
        info["File Path"] = file_path

        # Número de versión (asumiendo que estamos trabajando con GIF89a)
        version = data[0:6].decode("ascii")
        info["Número de versión"] = version

        # Tamaño de la imagen
        width = int.from_bytes(data[6:8], "little")
        height = int.from_bytes(data[8:10], "little")
        info["Tamaño de imagen"] = f"{width}x{height}"

        # Cantidad de colores
        color_count = 2 ** ((data[10] & 0b111) + 1)
        info["Cantidad de colores"] = color_count

        # Color de fondo
        background_color_index = data[11]
        info["Color de fondo (índice)"] = background_color_index

        # Tipo de compresión (GIF siempre utiliza LZW)
        info["Tipo de compresión de imagen"] = "LZW"

        # Formato numérico (usualmente se refiere al tamaño del archivo)
        info["Formato numérico"] = f"Tamaño en bytes: {len(data)}"

        # Cantidad de imágenes contenidas en el GIF
        image_count = data.count(b"\x2C")  # 0x2C indica el inicio de cada imagen
        info["Cantidad de imágenes"] = image_count

        # Fecha de creación y modificación
        info["Fecha de creación"] = datetime.datetime.fromtimestamp(
            os.path.getctime(file_path)
        ).strftime("%Y-%m-%d %H:%M:%S")
        info["Fecha de modificación"] = datetime.datetime.fromtimestamp(
            os.path.getmtime(file_path)
        ).strftime("%Y-%m-%d %H:%M:%S")

        # Comentarios
        comments = []
        # Comentarios (por defecto vacío si no existen)
        info["Comentarios agregados"] = "Sin comentarios"

        # Mostrar comentarios si existen
        if comments:
            info["Comentarios agregados"] = "\n".join(comments)
        else:
            info["Comentarios agregados"] = (
                "Sin comentarios"  # Cambiado para que indique que no hay comentarios
            )

        return info
    except Exception as e:
        print(f"Error al leer el archivo {file_path}: {e}")
        return {"Error": "No se pudo leer el archivo GIF"}

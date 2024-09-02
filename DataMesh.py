import os
import glob
import numpy as np
import pyvista as pv

def read_obj(file_path):
    vertices = []
    faces = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertices.append([float(coord) for coord in line.strip().split()[1:]])
            elif line.startswith('f '):
                faces.append([int(index.split('/')[0]) - 1 for index in line.strip().split()[1:]])
    return vertices, faces

def read_csv(file_path):
    import csv
    frames = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        columns = list(zip(*reader))
        for col in columns:
            frames.append([[float(value)] for value in col])
    return frames

def write_vtk(file_path, vertices, faces, colors):
    formatted_faces = []
    for face in faces:
        formatted_faces.append(len(face))
        formatted_faces.extend(face)
    
    mesh = pv.PolyData(vertices, formatted_faces)
    
    if colors:
        if len(colors) != len(vertices):
            raise ValueError(f"El número de colores ({len(colors)}) no coincide con el número de vértices ({len(vertices)})")
        
        colors = np.array(colors)
        mesh.point_data['colors'] = colors
    
    mesh.save(file_path, binary=True)
    print(f"Archivo VTK guardado: {file_path}")

def process_files(data_folder, output_base_folder, case_id, csv_filename, obj_filename, start_frame, end_frame):
    obj_file = os.path.join(data_folder, obj_filename)
    csv_file = os.path.join(data_folder, csv_filename)
    
    print(f"Procesando archivos para el caso: {case_id}")
    print(f"Archivo OBJ: {obj_file}")
    print(f"Archivo CSV: {csv_file}")
    print(f"Frame inicial: {start_frame}")
    print(f"Frame final: {end_frame}")
    
    if not os.path.exists(obj_file) or not os.path.exists(csv_file):
        print(f"No se encontraron los archivos necesarios para el caso {case_id} en la carpeta de datos.")
        print(f"Contenido de la carpeta {data_folder}:")
        print(os.listdir(data_folder))
        return False
    
    output_folder = os.path.join(output_base_folder, case_id)
    os.makedirs(output_folder, exist_ok=True)
    print(f"Carpeta de salida creada: {output_folder}")
    
    vertices, faces = read_obj(obj_file)
    frames = read_csv(csv_file)
    
    if len(frames) == 0:
        print(f"El archivo CSV está vacío o no contiene datos válidos: {csv_file}")
        return False
    
    if end_frame == -1 or end_frame >= len(frames):
        end_frame = len(frames) - 1
    
    start_frame = max(0, min(start_frame, end_frame))
    
    for i, colors in enumerate(frames[start_frame:end_frame+1], start=start_frame):
        output_file = os.path.join(output_folder, f'{case_id}_frame_{i:04d}.vtk')
        try:
            write_vtk(output_file, vertices, faces, colors)
            print(f"Archivo procesado: {output_file}")
        except ValueError as e:
            print(f"Error al procesar el frame {i}: {str(e)}")
            continue
    
    return True
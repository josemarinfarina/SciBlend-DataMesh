# SciBlend: DataMesh - CSV + OBJ to VTK Converter

SciBlend: DataMesh is a web application that processes CSV and OBJ files to generate VTK files. This tool is designed to assist in scientific visualization and data processing tasks.

## Features

- Upload CSV and OBJ files through a user-friendly web interface
- Process files to generate VTK output
- Specify start and end frames for processing
- Real-time feedback on file processing status

## Requirements

- Python 3.7+
- Flask
- NumPy
- PyVista

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/sciblend-datamesh.git
   cd sciblend-datamesh
   ```

2. Install the required dependencies:
   ```
   pip install flask numpy pyvista
   ```

## Usage

1. Run the Flask application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Use the web interface to upload your CSV and OBJ files, specify the start and end frames, and process the files.

## File Structure

- `app.py`: Main Flask application
- `DataMesh.py`: Core processing logic for CSV, OBJ, and VTK files
- `templates/upload.html`: HTML template for the web interface

## How It Works

1. The user uploads a CSV file (containing color data) and an OBJ file (containing 3D mesh data) through the web interface.
2. The application processes these files:
   - The OBJ file is read to extract vertices and faces of the 3D mesh.
   - The CSV file is read to extract color data for each vertex.
3. For each specified frame, a VTK file is generated, combining the 3D mesh structure with the corresponding color data.
4. The resulting VTK files are saved in an output folder, organized by case ID (derived from the OBJ filename).

## Contributing

Contributions to improve SciBlend: DataMesh are welcome. Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
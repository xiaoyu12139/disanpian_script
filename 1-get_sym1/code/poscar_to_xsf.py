import os

def read_poscar(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    title = lines[0].strip()
    scale = float(lines[1].strip())
    
    lattice_vectors = []
    for i in range(2, 5):
        lattice_vectors.append([float(x) for x in lines[i].strip().split()])
    
    atom_types = lines[5].strip().split()
    atom_counts = [int(x) for x in lines[6].strip().split()]
    
    coord_type = lines[7].strip()
    
    atom_positions = []
    start_idx = 8
    for count in atom_counts:
        for i in range(start_idx, start_idx + count):
            position = lines[i].strip().split()[:3]  # Only take the first three columns for positions
            atom_positions.append([float(x) for x in position])
        start_idx += count
    
    return title, scale, lattice_vectors, atom_types, atom_counts, atom_positions, coord_type

def write_xsf(filename, title, scale, lattice_vectors, atom_types, atom_counts, atom_positions, coord_type):
    with open(filename, 'w') as file:
        file.write(f"CRYSTAL\n")
        file.write(f"PRIMVEC\n")
        for vec in lattice_vectors:
            file.write(f"{vec[0] * scale:.10f} {vec[1] * scale:.10f} {vec[2] * scale:.10f}\n")
        
        file.write(f"PRIMCOORD\n")
        total_atoms = sum(atom_counts)
        file.write(f"{total_atoms} 1\n")
        
        atom_index = 0
        for atom_type, count in zip(atom_types, atom_counts):
            for _ in range(count):
                position = atom_positions[atom_index]
                atom_index += 1
                file.write(f"{atom_type} {position[0]:.10f} {position[1]:.10f} {position[2]:.10f}\n")

def poscar_to_xsf(poscar_path, xsf_path):
    title, scale, lattice_vectors, atom_types, atom_counts, atom_positions, coord_type = read_poscar(poscar_path)
    write_xsf(xsf_path, title, scale, lattice_vectors, atom_types, atom_counts, atom_positions, coord_type)

# def __name__ == "__main__":
#     poscar_path = 'POSCAR'
#     xsf_path = 'output.xsf'
#     poscar_to_xsf(poscar_path, xsf_path)
#     print(f"Conversion from {poscar_path} to {xsf_path} completed successfully.")

def poscar_to_xsf_fun(poscar_path,xsf_path):
    poscar_to_xsf(poscar_path, xsf_path)
    print(f"Conversion from {poscar_path} to {xsf_path} completed successfully.")


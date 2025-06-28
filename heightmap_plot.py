import numpy as np
import matplotlib.pyplot as plt

# Replace with your actual .ply file path
ply_file = "/Users/venkitesh/Downloads/sample file/sample_ply.ply"
print("hello world")
# Step 1: Read point cloud from ASCII PLY
def read_ply_xyz(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    start = 0
    for i, line in enumerate(lines):
        if line.strip() == "end_header":
            start = i + 1
            break
    points = np.array([list(map(float, line.strip().split()[:3])) for line in lines[start:]])
    return points

points = read_ply_xyz(ply_file)
x, y, z = points[:, 0], points[:, 1], points[:, 2]

# Step 2: Normalize and gridify
grid_size = 0.1
x -= x.min()
y -= y.min()
x_idx = (x / grid_size).astype(int)
y_idx = (y / grid_size).astype(int)
grid_width = x_idx.max() + 1
grid_height = y_idx.max() + 1
height_map = np.full((grid_height, grid_width), np.nan)

for i in range(len(z)):
    xi, yi = x_idx[i], y_idx[i]
    if np.isnan(height_map[yi, xi]):
        height_map[yi, xi] = z[i]
    else:
        height_map[yi, xi] = (height_map[yi, xi] + z[i]) / 2

# Step 3: Clip Z to boost contrast
z_clip_min = np.nanpercentile(height_map, 1)
z_clip_max = np.nanpercentile(height_map, 99)
height_map = np.clip(height_map, z_clip_min, z_clip_max)

# Step 4: Plot
plt.figure(figsize=(10, 8))
plt.imshow(height_map, cmap='viridis', origin='lower', vmin=z_clip_min, vmax=z_clip_max)
plt.title("Enhanced 2D Height Heatmap from .ply")
plt.colorbar(label="Height (Z)")
plt.tight_layout()
plt.show()

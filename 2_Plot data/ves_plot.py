# ----------------------------------------------------
# Plot hasil inversi VES dari IPI2win
# Author: Annora Vandanu Erlangga
# ----------------------------------------------------

import matplotlib.pyplot as plt
import os

# Ganti 'namafile.txt' dengan path ke file datamu
filename = 'D:/Kulon Progo 2025/Geolistrik/VES/Inversi/IPI2WIN/K4/K4.txt'
plot_title = os.path.splitext(os.path.basename(filename))[0]
save_dir = os.path.dirname(filename)
model_plot_path = os.path.join(save_dir, f"{plot_title}_Model_Inversi.png")
curve_plot_path = os.path.join(save_dir, f"{plot_title}_Kurva_Kalkulasi.png")

with open(filename, 'r') as file:
    lines = file.readlines()

start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if 'Model' in line:
        start_idx = i + 2  # Lewati header "D\tRo"
    if 'Field curve' in line:
        end_idx = i
        break

model_lines = lines[start_idx:end_idx]
depth = []
resistivity = []

for line in model_lines:
    parts = line.strip().split()
    if len(parts) == 2:
        d, r = parts
        try:
            depth.append(float(d))
            resistivity.append(float(r.replace(",", "")))  # hilangkan koma kalau ada
        except:
            pass  # lewati baris error

field_start = None
synthetic_start = None
for i, line in enumerate(lines):
    if 'Field curve' in line:
        field_start = i + 2  # Lewati header
    if 'Synthetic curve' in line:
        synthetic_start = i + 2
        break

ab2_obs = []
res_obs = []
for line in lines[field_start:synthetic_start - 2]:
    parts = line.strip().split()
    if len(parts) == 2:
        try:
            ab2_obs.append(float(parts[0]))
            res_obs.append(float(parts[1].replace(",", "")))
        except:
            pass

ab2_syn = []
res_syn = []
for line in lines[synthetic_start:]:
    parts = line.strip().split()
    if len(parts) == 2:
        try:
            ab2_syn.append(float(parts[0]))
            res_syn.append(float(parts[1].replace(",", "")))
        except:
            pass

# ========== Plot 1: Model Inversi ==========
fig, ax = plt.subplots(figsize=(4, 10))
ax.step(resistivity, depth, where='post', color='b', linewidth=2, label='Model Inversi')
ax.set_xlabel('Resistivitas (Ohm-m)')
ax.set_ylabel('Kedalaman (m)')
ax.set_title(f'Model Inversi VES {plot_title}')
ax.set_xscale('log')
ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=False))
ax.invert_yaxis()
ax.grid(True)
ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig(model_plot_path, transparent=True, dpi=300)
plt.show()

print(f"model inversi tersimpan di {model_plot_path}")

# ========== Plot 2: Kurva Lapangan vs Sintetik ==========
fig, ax = plt.subplots(figsize=(4, 10))
ax.plot(res_obs, ab2_obs, 'o-', label='Observasi (Lapangan)', color='black')
ax.plot(res_syn, ab2_syn, 'x--', label='Kalkulasi (Sintetik)', color='red')
ax.legend(loc='lower right')
ax.set_xlabel('Resistivitas Semu (Ohm-m)')
ax.set_ylabel('AB/2 (m)')
ax.set_title(f'Kurva Observasi & Kalkulasi {plot_title}')
ax.grid(True)
ax.invert_yaxis()
ax.set_xscale('log')
ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=False))
# ax.set_yscale('log')
plt.tight_layout()
plt.savefig(curve_plot_path, transparent=True, dpi=300)
plt.show()

print(f"kurva kalkulasi tersimpan di {curve_plot_path}")
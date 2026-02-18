#!/usr/bin/env python3
"""Panoramic sky pan from Polaris through Big Dipper to Paradise."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Reuse GU plane function from keyframes_fixed.py
def compute_gu_plane(ra_range):
    def to_cart(ra_deg, dec_deg):
        ra, dec = np.radians(ra_deg), np.radians(dec_deg)
        return np.array([np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)])
    p1 = to_cart(168, -1.3)
    p2 = to_cart(135, 2.0)
    normal = np.cross(p1, p2)
    normal = normal / np.linalg.norm(normal)
    dec_vals = []
    for ra in ra_range:
        ra_rad = np.radians(ra)
        dec_rad = np.arctan(-(normal[0]*np.cos(ra_rad) + normal[1]*np.sin(ra_rad)) / normal[2])
        dec_vals.append(np.degrees(dec_rad))
    return np.array(dec_vals)

# Star data - reuse from keyframes_fixed.py plus new additions
virgo_stars = [
    (201.30,-11.16,0.98),(190.42,-1.45,2.74),(184.98,-0.67,3.38),
    (183.95,3.40,2.83),(198.43,-6.00,3.38),(194.18,10.96,3.59),
    (177.67,14.57,3.89),(192.85,-5.83,3.37),
]
leo_stars = [
    (152.09,11.97,1.36),(177.26,14.57,2.14),(168.53,20.52,2.01),
    (154.17,23.77,2.56),(168.56,15.43,3.33),(146.46,23.77,3.44),
    (148.19,26.18,3.52),(151.83,16.76,3.48),(170.98,10.53,3.34),
]
crater_stars = [
    (170.15,-17.68,3.56),(167.91,-14.78,4.08),(164.94,-18.30,3.83),
    (169.84,-22.83,4.08),(176.19,-18.35,3.94),
]

# New star data
polaris = [(37.95, 89.26, 1.97)]
big_dipper = [
    (165.93, 61.75, 1.81),  # Dubhe
    (165.46, 56.38, 2.34),  # Merak
    (178.46, 53.69, 2.44),  # Phecda
    (183.86, 57.03, 3.32),  # Megrez
    (193.51, 55.96, 1.76),  # Alioth
    (200.98, 54.93, 2.23),  # Mizar
    (206.89, 49.31, 1.85),  # Alkaid
]

all_stars = polaris + big_dipper + virgo_stars + leo_stars + crater_stars

# Constellation names and positions
constellation_names = {
    'Ursa Major': (180, 55), 'Leo': (158, 18), 
    'Virgo': (192, 2), 'Crater': (170, -19),
}

# Star names to label (mag < 2.5)
star_names = {
    (37.95, 89.26): 'Polaris',
    (165.93, 61.75): 'Dubhe',
    (193.51, 55.96): 'Alioth',
    (200.98, 54.93): 'Mizar',
    (206.89, 49.31): 'Alkaid',
    (165.46, 56.38): 'Merak',
    (152.09, 11.97): 'Regulus',
    (177.26, 14.57): 'Denebola',
    (168.53, 20.52): 'Algieba',
    (201.30, -11.16): 'Spica'
}

# Generate background stars
rng = np.random.RandomState(42)
bg_n = 5000
bg_ra = rng.uniform(30, 220, bg_n)  # Cover pan range
bg_dec = rng.uniform(-10, 90, bg_n)  # Cover pan range
bg_s = rng.uniform(0.1, 2.0, bg_n)

# View parameters
view_width = 80
view_height = 50

# Animation parameters
frames_total = 70
frames_pause_start = 12
frames_pan = 40
frames_pause_end = 18

# Output path
output_path = '/home/warren/warren-ventures/active/lumen-wren/assets/cosmology-series/sky-pan-polaris-v1.gif'

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(16, 9), facecolor='#0a0a1a')
ax.set_facecolor('#0a0a1a')
ax.axis('off')

# Initialize empty scatter plots and text
scatter_bg = ax.scatter([], [], s=[], c='white', alpha=0.35, edgecolors='none', zorder=0)
scatter_stars_halo = ax.scatter([], [], s=[], c='white', alpha=0.08, edgecolors='none', zorder=3)
scatter_stars_core = ax.scatter([], [], s=[], c='white', alpha=0.8, edgecolors='none', zorder=4)
star_labels = []
constellation_texts = []
paradise_circles = []
paradise_text = None
gu_line, = ax.plot([], [], color='#ffd060', linewidth=1.5, linestyle='--', alpha=0.4, zorder=2)

# Ease-in-out function for smooth panning
def ease_in_out(t):
    return 0.5 * (1 - np.cos(t * np.pi))

# Update function for animation
def update(frame):
    # Calculate progress (0 to 1)
    if frame < frames_pause_start:
        progress = 0.0
    elif frame < frames_pause_start + frames_pan:
        pan_progress = (frame - frames_pause_start) / frames_pan
        progress = ease_in_out(pan_progress)
    else:
        progress = 1.0
    
    # Calculate current center
    center_ra = 37.95 + (168 - 37.95) * progress
    center_dec = 89.26 + (-1.3 - 89.26) * progress
    
    # Calculate view bounds
    ra_min = center_ra - view_width / 2
    ra_max = center_ra + view_width / 2
    dec_min = center_dec - view_height / 2
    dec_max = center_dec + view_height / 2
    
    # Update background stars
    mask_bg = (bg_ra > ra_min) & (bg_ra < ra_max) & (bg_dec > dec_min) & (bg_dec < dec_max)
    scatter_bg.set_offsets(np.column_stack((bg_ra[mask_bg], bg_dec[mask_bg])))
    scatter_bg.set_sizes(bg_s[mask_bg] * 10)
    
    # Update visible stars
    visible_stars = []
    sizes_halo = []
    sizes_core = []
    alphas_core = []
    
    for ra, dec, mag in all_stars:
        if ra_min < ra < ra_max and dec_min < dec < dec_max:
            visible_stars.append([ra, dec])
            sizes_halo.append(max(5, (4.5 - mag) * 15))
            sizes_core.append(max(2, (4.5 - mag) * 4))
            alphas_core.append(min(1.0, max(0.4, (4.0 - mag) / 2.5)))
    
    if visible_stars:
        visible_stars = np.array(visible_stars)
        scatter_stars_halo.set_offsets(visible_stars)
        scatter_stars_halo.set_sizes(sizes_halo)
        scatter_stars_core.set_offsets(visible_stars)
        scatter_stars_core.set_sizes(sizes_core)
        scatter_stars_core.set_alpha(alphas_core)
    
    # Update star labels
    for label in star_labels:
        label.remove()
    star_labels.clear()
    
    for (ra, dec), name in star_names.items():
        if ra_min < ra < ra_max and dec_min < dec < dec_max:
            label = ax.text(ra - 1, dec + 1.5, name, ha='right', va='bottom',
                           color='#8898b0', fontsize=7, alpha=0.7, zorder=5)
            star_labels.append(label)
    
    # Update constellation names
    for text in constellation_texts:
        text.remove()
    constellation_texts.clear()
    
    for name, (ra, dec) in constellation_names.items():
        if ra_min < ra < ra_max and dec_min < dec < dec_max:
            text = ax.text(ra, dec, name, ha='center', va='center',
                          color='#5a6a7a', fontsize=11, style='italic', alpha=0.5, zorder=2)
            constellation_texts.append(text)
    
    # Update GU plane
    gu_ra = np.linspace(ra_min, ra_max, 200)
    gu_dec = compute_gu_plane(gu_ra)
    mask_gu = (gu_dec > dec_min) & (gu_dec < dec_max)
    gu_line.set_data(gu_ra[mask_gu], gu_dec[mask_gu])
    
    # Update Paradise marker
    for circle in paradise_circles:
        circle.remove()
    paradise_circles.clear()
    
    if ra_min < 168 < ra_max and dec_min < -1.3 < dec_max:
        pa = min(1.0, max(0, (progress - 0.6) / 0.3))
        if pa > 0:
            for r, a in [(3, 0.04), (2, 0.08), (1, 0.15)]:
                circle = plt.Circle((168, -1.3), r, facecolor='#ffd060', alpha=a * pa, zorder=5)
                ax.add_patch(circle)
                paradise_circles.append(circle)
            
            if paradise_text:
                paradise_text.remove()
            if pa > 0.5:
                paradise_text = ax.text(168, -1.3 + 3, 'Paradise', ha='center', va='bottom',
                                      color='#ffd060', fontsize=13, fontweight='bold',
                                      style='italic', alpha=pa, zorder=6)
            else:
                paradise_text = None
    
    ax.set_xlim(ra_max, ra_min)
    ax.set_ylim(dec_min, dec_max)
    ax.set_aspect('equal')
    
    return [scatter_bg, scatter_stars_halo, scatter_stars_core, gu_line] + star_labels + constellation_texts + paradise_circles

# Create animation
ani = FuncAnimation(fig, update, frames=frames_total, interval=150, blit=False)

# Save animation
ani.save(output_path, writer='pillow', fps=10, dpi=100)
print(f"Animation saved to {output_path}")
plt.close()
#!/usr/bin/env python3
"""Panoramic sky pan animation from Polaris through Big Dipper to Leo and Paradise."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import os

# Ensure output directory exists
output_dir = '/home/warren/warren-ventures/active/lumen-wren/assets/cosmology-series'
os.makedirs(output_dir, exist_ok=True)

# Star data (RA deg, Dec deg, Vmag)
# Polaris and Big Dipper stars
polaris = [(37.95, 89.26, 1.97)]
big_dipper = [
    (165.93, 61.75, 1.81),  # Dubhe
    (165.46, 56.38, 2.34),  # Merak
    (178.46, 53.69, 2.44),  # Phecda
    (183.86, 57.03, 3.32),  # Megrez
    (193.51, 55.96, 1.76),  # Alioth
    (200.98, 54.93, 2.23),  # Mizar
    (206.89, 49.31, 1.85)   # Alkaid
]

# Reused from keyframes_fixed.py
leo_stars = [
    (152.09, 11.97, 1.36),  # Regulus
    (177.26, 14.57, 2.14),  # Denebola
    (168.53, 20.52, 2.01),  # Algieba
    (154.17, 23.77, 2.56),
    (168.56, 15.43, 3.33),
    (146.46, 23.77, 3.44),
    (148.19, 26.18, 3.52),
    (151.83, 16.76, 3.48),
    (170.98, 10.53, 3.34)
]

virgo_stars = [
    (201.30, -11.16, 0.98),  # Spica
    (190.42, -1.45, 2.74),
    (184.98, -0.67, 3.38),
    (183.95, 3.40, 2.83),
    (198.43, -6.00, 3.38),
    (194.18, 10.96, 3.59),
    (177.67, 14.57, 3.89),
    (192.85, -5.83, 3.37)
]

crater_stars = [
    (170.15, -17.68, 3.56),
    (167.91, -14.78, 4.08),
    (164.94, -18.30, 3.83),
    (169.84, -22.83, 4.08),
    (176.19, -18.35, 3.94)
]

# Combine all stars
all_stars = polaris + big_dipper + leo_stars + virgo_stars + crater_stars

# Constellation labels
constellation_names = {
    'Ursa Major': (190, 55),
    'Leo': (158, 18),
    'Virgo': (192, 2),
    'Crater': (170, -19)
}

# Star names (mag < 2.5)
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

# GU plane function (unchanged from keyframes_fixed.py)
def compute_gu_plane(ra_range):
    def to_cart(ra_deg, dec_deg):
        ra, dec = np.radians(ra_deg), np.radians(dec_deg)
        return np.array([np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)])
    p1 = to_cart(168, -1.3)  # Paradise
    p2 = to_cart(135, 2.0)   # Second point
    normal = np.cross(p1, p2)
    normal = normal / np.linalg.norm(normal)
    dec_vals = []
    for ra in ra_range:
        ra_rad = np.radians(ra)
        dec_rad = np.arctan(-(normal[0]*np.cos(ra_rad) + normal[1]*np.sin(ra_rad)) / normal[2])
        dec_vals.append(np.degrees(dec_rad))
    return np.array(dec_vals)

# Generate background stars
rng = np.random.RandomState(42)
bg_n = 5000
bg_ra = rng.uniform(30, 210, bg_n)  # Cover pan range
bg_dec = rng.uniform(-10, 90, bg_n)  # Cover pan range
bg_s = rng.uniform(0.1, 2.0, bg_n)   # Random sizes

# Animation parameters
view_width = 80
view_height = 50

# Create figure
fig, ax = plt.subplots(figsize=(16, 9), facecolor='#0a0a1a')
ax.set_facecolor('#0a0a1a')
ax.axis('off')

# Initial empty scatter plots
star_plot = ax.plot([], [], 'o', color='white', markersize=4, alpha=0.8)[0]
bg_plot = ax.plot([], [], 'o', color='white', markersize=1, alpha=0.3)[0]
halo_plots = [ax.plot([], [], 'o', color='white', markersize=10, alpha=0.1)[0] for _ in range(10)]

# Text elements
constellation_texts = {name: ax.text(0, 0, name, ha='center', va='center', 
                                    color='#5a6a7a', fontsize=11, style='italic', alpha=0.5) 
                      for name in constellation_names}
star_texts = {pos: ax.text(0, 0, name, ha='right', va='bottom', 
                           color='#8898b0', fontsize=7, alpha=0.7) 
             for pos, name in star_names.items()}

# GU plane line
gu_line, = ax.plot([], [], color='#ffd060', linewidth=1.5, linestyle='--', alpha=0.4)

# Paradise marker
paradise_circles = [plt.Circle((0, 0), r, facecolor='#ffd060', alpha=0.0) for r in [3, 2, 1]]
for circle in paradise_circles:
    ax.add_patch(circle)
paradise_marker = ax.plot([], [], 'o', color='#ffd060', markersize=8, alpha=0.0)[0]
paradise_text = ax.text(0, 0, 'Paradise', ha='center', va='bottom', 
                       color='#ffd060', fontsize=13, fontweight='bold', style='italic', alpha=0.0)

def init():
    ax.set_xlim(0, 360)
    ax.set_ylim(-90, 90)
    return [star_plot, bg_plot, gu_line, paradise_marker, paradise_text] + list(halo_plots) + list(constellation_texts.values()) + list(star_texts.values())

def update(frame):
    # Calculate current center position (ease in/out)
    if frame < 12:  # Pause at start
        center_ra = 37.95
        center_dec = 89.26
        progress = 0.0
    elif frame < 52:  # Pan (40 frames)
        t = (frame - 12) / 39
        t = t * t * (3 - 2 * t)  # Smoothstep easing
        center_ra = 37.95 + t * (158 - 37.95)
        center_dec = 89.26 + t * (-1.3 - 89.26)
        progress = t
    else:  # Pause at end (18 frames)
        center_ra = 158
        center_dec = -1.3
        progress = 1.0
    
    ra_min = center_ra - view_width / 2
    ra_max = center_ra + view_width / 2
    dec_min = center_dec - view_height / 2
    dec_max = center_dec + view_height / 2
    
    # Update view limits
    ax.set_xlim(ra_max, ra_min)
    ax.set_ylim(dec_min, dec_max)
    
    # Filter visible stars
    visible_stars = [(ra, dec, mag) for ra, dec, mag in all_stars 
                    if ra_min < ra < ra_max and dec_min < dec < dec_max]
    
    # Update star plots
    if visible_stars:
        star_ra, star_dec, star_mag = zip(*visible_stars)
        star_plot.set_data(star_ra, star_dec)
        star_sizes = [max(2, (4.5 - mag) * 4) for mag in star_mag]
        star_plot.set_markersize(star_sizes[0])
        
        # Update halos
        for i, (ra, dec, mag) in enumerate(visible_stars[:10]):
            halo_plots[i].set_data([ra], [dec])
            halo_size = max(5, (4.5 - mag) * 15)
            halo_plots[i].set_markersize(halo_size)
    
    # Update background stars
    bg_mask = (bg_ra > ra_min) & (bg_ra < ra_max) & (bg_dec > dec_min) & (bg_dec < dec_max)
    bg_plot.set_data(bg_ra[bg_mask], bg_dec[bg_mask])
    
    # Update constellation labels
    for name, (ra, dec) in constellation_names.items():
        text = constellation_texts[name]
        if ra_min < ra < ra_max and dec_min < dec < dec_max:
            text.set_position((ra, dec))
            text.set_alpha(0.5)
        else:
            text.set_alpha(0.0)
    
    # Update star labels
    for (ra, dec), text in star_texts.items():
        if ra_min < ra < ra_max and dec_min < dec < dec_max:
            text.set_position((ra - 1, dec + 1.5))
            text.set_alpha(0.7)
        else:
            text.set_alpha(0.0)
    
    # Update GU plane
    if dec_min < 0 < dec_max:  # Only draw near ecliptic
        gu_ra = np.linspace(ra_min, ra_max, 100)
        gu_dec = compute_gu_plane(gu_ra)
        gu_mask = (gu_dec > dec_min) & (gu_dec < dec_max)
        gu_line.set_data(gu_ra[gu_mask], gu_dec[gu_mask])
    else:
        gu_line.set_data([], [])
    
    # Update Paradise marker (fade in last 30%)
    paradise_alpha = min(1.0, max(0, (progress - 0.7) / 0.3))
    if paradise_alpha > 0:
        for i, circle in enumerate(paradise_circles):
            circle.center = (168, -1.3)
            circle.set_alpha([0.04, 0.08, 0.15][i] * paradise_alpha)
        paradise_marker.set_data([168], [-1.3])
        paradise_marker.set_alpha(paradise_alpha)
        paradise_text.set_position((168, -1.3 + 3))
        paradise_text.set_alpha(paradise_alpha)
    else:
        for circle in paradise_circles:
            circle.set_alpha(0.0)
        paradise_marker.set_alpha(0.0)
        paradise_text.set_alpha(0.0)
    
    return [star_plot, bg_plot, gu_line, paradise_marker, paradise_text] + list(halo_plots) + list(constellation_texts.values()) + list(star_texts.values())

# Create animation
ani = FuncAnimation(fig, update, frames=70, init_func=init, blit=True, interval=150)

# Save animation
output_path = os.path.join(output_dir, 'sky-pan-polaris-v1.gif')
ani.save(output_path, writer='pillow', fps=10, dpi=100)

print(f"Animation saved to {output_path}")
"""
3D Visualization Engine
Purpose: Build 3D visualization engine for sacred geometry, wave forms, toroidal fields, cymatics, harmonics
- 3D vector space visualization
- Sacred geometry rendering (Metatron's Cube, Tree of Life, etc.)
- Wave form visualization
- Toroidal field visualization
- Cymatics visualization
- Harmonic visualization
- Color/frequency mapping
- Chakra visualization
- Interactive dashboard

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import json

logger = logging.getLogger(__name__)

# Try to import visualization libraries
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False
    logger.warning("Plotly not installed, 3D visualization disabled")

try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    logger.warning("Matplotlib not installed, 3D visualization disabled")


class VisualizationEngine:
    """
    3D Visualization Engine - Creates visualizations for sacred geometry, waves, fields, etc.
    """
    
    def __init__(self):
        """Initialize visualization engine"""
        self.has_plotly = HAS_PLOTLY
        self.has_matplotlib = HAS_MATPLOTLIB
        logger.info(f"Initialized VisualizationEngine (Plotly: {HAS_PLOTLY}, Matplotlib: {HAS_MATPLOTLIB})")
    
    def generate_metatrons_cube(self, size: float = 1.0) -> Dict:
        """
        Generate Metatron's Cube geometry.
        
        Args:
            size: Size of the cube
            
        Returns:
            Dictionary with 3D coordinates
        """
        # Metatron's Cube consists of 13 circles arranged in a specific pattern
        # This is a simplified representation
        circles = []
        
        # Center circle
        circles.append({'x': 0, 'y': 0, 'z': 0, 'radius': size})
        
        # 6 circles around center (hexagon)
        for i in range(6):
            angle = i * np.pi / 3
            circles.append({
                'x': size * np.cos(angle),
                'y': size * np.sin(angle),
                'z': 0,
                'radius': size * 0.5
            })
        
        # 6 outer circles
        for i in range(6):
            angle = i * np.pi / 3
            circles.append({
                'x': size * 2 * np.cos(angle),
                'y': size * 2 * np.sin(angle),
                'z': 0,
                'radius': size * 0.5
            })
        
        return {
            'type': 'metatrons_cube',
            'circles': circles,
            'size': size
        }
    
    def generate_tree_of_life(self, size: float = 1.0) -> Dict:
        """
        Generate Tree of Life geometry.
        
        Args:
            size: Size of the tree
            
        Returns:
            Dictionary with 3D coordinates
        """
        # Tree of Life has 10 sephiroth (spheres) connected by 22 paths
        sephiroth = {
            'keter': {'x': 0, 'y': size * 3, 'z': 0},
            'chokmah': {'x': -size, 'y': size * 2, 'z': 0},
            'binah': {'x': size, 'y': size * 2, 'z': 0},
            'chesed': {'x': -size * 1.5, 'y': size, 'z': 0},
            'gevurah': {'x': -size * 0.5, 'y': size, 'z': 0},
            'tiferet': {'x': 0, 'y': size, 'z': 0},
            'netzach': {'x': size * 0.5, 'y': size, 'z': 0},
            'hod': {'x': size * 1.5, 'y': size, 'z': 0},
            'yesod': {'x': 0, 'y': 0, 'z': 0},
            'malkuth': {'x': 0, 'y': -size, 'z': 0}
        }
        
        # Paths connecting sephiroth
        paths = [
            ('keter', 'chokmah'),
            ('keter', 'binah'),
            ('chokmah', 'tiferet'),
            ('binah', 'tiferet'),
            ('chesed', 'gevurah'),
            ('gevurah', 'tiferet'),
            ('chesed', 'tiferet'),
            ('tiferet', 'netzach'),
            ('tiferet', 'hod'),
            ('netzach', 'yesod'),
            ('hod', 'yesod'),
            ('yesod', 'malkuth')
        ]
        
        return {
            'type': 'tree_of_life',
            'sephiroth': sephiroth,
            'paths': paths,
            'size': size
        }
    
    def generate_wave_form(self, frequency: float = 1.0, amplitude: float = 1.0, 
                           duration: float = 2.0, sample_rate: int = 1000) -> Dict:
        """
        Generate wave form visualization.
        
        Args:
            frequency: Wave frequency (Hz)
            amplitude: Wave amplitude
            duration: Duration in seconds
            sample_rate: Sample rate (samples per second)
            
        Returns:
            Dictionary with wave data
        """
        t = np.linspace(0, duration, int(sample_rate * duration))
        y = amplitude * np.sin(2 * np.pi * frequency * t)
        
        return {
            'type': 'wave_form',
            'time': t.tolist(),
            'amplitude': y.tolist(),
            'frequency': frequency,
            'amplitude_value': amplitude,
            'duration': duration
        }
    
    def generate_toroidal_field(self, radius: float = 1.0, tube_radius: float = 0.3, 
                                 resolution: int = 50) -> Dict:
        """
        Generate toroidal field geometry.
        
        Args:
            radius: Major radius of torus
            tube_radius: Minor radius of torus
            resolution: Resolution of the mesh
            
        Returns:
            Dictionary with 3D coordinates
        """
        u = np.linspace(0, 2 * np.pi, resolution)
        v = np.linspace(0, 2 * np.pi, resolution)
        u, v = np.meshgrid(u, v)
        
        x = (radius + tube_radius * np.cos(v)) * np.cos(u)
        y = (radius + tube_radius * np.cos(v)) * np.sin(u)
        z = tube_radius * np.sin(v)
        
        return {
            'type': 'toroidal_field',
            'x': x.tolist(),
            'y': y.tolist(),
            'z': z.tolist(),
            'radius': radius,
            'tube_radius': tube_radius
        }
    
    def generate_cymatics_pattern(self, frequency: float = 440.0, resolution: int = 100) -> Dict:
        """
        Generate cymatics pattern visualization.
        
        Args:
            frequency: Frequency in Hz
            resolution: Resolution of the pattern
            
        Returns:
            Dictionary with pattern data
        """
        x = np.linspace(-2, 2, resolution)
        y = np.linspace(-2, 2, resolution)
        X, Y = np.meshgrid(x, y)
        
        # Cymatics pattern based on frequency
        R = np.sqrt(X**2 + Y**2)
        pattern = np.sin(frequency * R) * np.exp(-R**2)
        
        return {
            'type': 'cymatics_pattern',
            'x': x.tolist(),
            'y': y.tolist(),
            'pattern': pattern.tolist(),
            'frequency': frequency
        }
    
    def generate_harmonic_series(self, fundamental: float = 440.0, harmonics: int = 10) -> Dict:
        """
        Generate harmonic series visualization.
        
        Args:
            fundamental: Fundamental frequency (Hz)
            harmonics: Number of harmonics
            
        Returns:
            Dictionary with harmonic data
        """
        frequencies = [fundamental * (i + 1) for i in range(harmonics)]
        amplitudes = [1.0 / (i + 1) for i in range(harmonics)]  # Decreasing amplitude
        
        return {
            'type': 'harmonic_series',
            'frequencies': frequencies,
            'amplitudes': amplitudes,
            'fundamental': fundamental,
            'harmonics_count': harmonics
        }
    
    def frequency_to_color(self, frequency: float) -> str:
        """
        Convert frequency to color (visible light spectrum).
        
        Args:
            frequency: Frequency in Hz
            
        Returns:
            Hex color code
        """
        # Visible light spectrum: 400-700 THz (approximately)
        # Map frequency to RGB
        if frequency < 400e12:
            # Below visible spectrum - blue/violet
            return '#0000FF'
        elif frequency > 700e12:
            # Above visible spectrum - red
            return '#FF0000'
        else:
            # Map to visible spectrum
            normalized = (frequency - 400e12) / (700e12 - 400e12)
            
            if normalized < 0.33:
                # Blue to green
                r = 0
                g = int(255 * normalized * 3)
                b = 255
            elif normalized < 0.66:
                # Green to yellow
                r = int(255 * (normalized - 0.33) * 3)
                g = 255
                b = int(255 * (1 - (normalized - 0.33) * 3))
            else:
                # Yellow to red
                r = 255
                g = int(255 * (1 - (normalized - 0.66) * 3))
                b = 0
            
            return f'#{r:02X}{g:02X}{b:02X}'
    
    def generate_chakra_visualization(self) -> Dict:
        """
        Generate chakra visualization.
        
        Returns:
            Dictionary with chakra data
        """
        chakras = [
            {'name': 'Root', 'color': '#FF0000', 'frequency': 256, 'position': {'x': 0, 'y': -3, 'z': 0}},
            {'name': 'Sacral', 'color': '#FF7F00', 'frequency': 288, 'position': {'x': 0, 'y': -2, 'z': 0}},
            {'name': 'Solar Plexus', 'color': '#FFFF00', 'frequency': 320, 'position': {'x': 0, 'y': -1, 'z': 0}},
            {'name': 'Heart', 'color': '#00FF00', 'frequency': 341.3, 'position': {'x': 0, 'y': 0, 'z': 0}},
            {'name': 'Throat', 'color': '#0000FF', 'frequency': 384, 'position': {'x': 0, 'y': 1, 'z': 0}},
            {'name': 'Third Eye', 'color': '#4B0082', 'frequency': 426.7, 'position': {'x': 0, 'y': 2, 'z': 0}},
            {'name': 'Crown', 'color': '#9400D3', 'frequency': 480, 'position': {'x': 0, 'y': 3, 'z': 0}}
        ]
        
        return {
            'type': 'chakra_visualization',
            'chakras': chakras
        }
    
    def create_3d_plot(self, geometry: Dict, title: str = "3D Visualization") -> Optional[Any]:
        """
        Create 3D plot from geometry data.
        
        Args:
            geometry: Geometry dictionary
            title: Plot title
            
        Returns:
            Plotly figure or None
        """
        if not self.has_plotly:
            logger.warning("Plotly not available, cannot create 3D plot")
            return None
        
        try:
            fig = go.Figure()
            
            geom_type = geometry.get('type')
            
            if geom_type == 'metatrons_cube':
                circles = geometry.get('circles', [])
                for circle in circles:
                    # Draw circle as scatter plot
                    theta = np.linspace(0, 2 * np.pi, 100)
                    x = circle['x'] + circle['radius'] * np.cos(theta)
                    y = circle['y'] + circle['radius'] * np.sin(theta)
                    z = [circle['z']] * len(theta)
                    
                    fig.add_trace(go.Scatter3d(
                        x=x.tolist(),
                        y=y.tolist(),
                        z=z,
                        mode='lines',
                        name=f"Circle at ({circle['x']}, {circle['y']})"
                    ))
            
            elif geom_type == 'tree_of_life':
                sephiroth = geometry.get('sephiroth', {})
                paths = geometry.get('paths', [])
                
                # Draw sephiroth as points
                for name, pos in sephiroth.items():
                    fig.add_trace(go.Scatter3d(
                        x=[pos['x']],
                        y=[pos['y']],
                        z=[pos['z']],
                        mode='markers',
                        marker=dict(size=10),
                        name=name
                    ))
                
                # Draw paths
                for start, end in paths:
                    if start in sephiroth and end in sephiroth:
                        fig.add_trace(go.Scatter3d(
                            x=[sephiroth[start]['x'], sephiroth[end]['x']],
                            y=[sephiroth[start]['y'], sephiroth[end]['y']],
                            z=[sephiroth[start]['z'], sephiroth[end]['z']],
                            mode='lines',
                            line=dict(width=2),
                            showlegend=False
                        ))
            
            elif geom_type == 'toroidal_field':
                x = np.array(geometry['x'])
                y = np.array(geometry['y'])
                z = np.array(geometry['z'])
                
                fig.add_trace(go.Surface(
                    x=x,
                    y=y,
                    z=z,
                    colorscale='Viridis'
                ))
            
            fig.update_layout(
                title=title,
                scene=dict(
                    xaxis_title='X',
                    yaxis_title='Y',
                    zaxis_title='Z',
                    aspectmode='cube'
                )
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating 3D plot: {e}")
            return None
    
    def create_wave_plot(self, wave_data: Dict, title: str = "Wave Form") -> Optional[Any]:
        """
        Create wave form plot.
        
        Args:
            wave_data: Wave data dictionary
            title: Plot title
            
        Returns:
            Plotly figure or None
        """
        if not self.has_plotly:
            logger.warning("Plotly not available, cannot create wave plot")
            return None
        
        try:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=wave_data['time'],
                y=wave_data['amplitude'],
                mode='lines',
                name=f"Frequency: {wave_data['frequency']} Hz"
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title='Time (s)',
                yaxis_title='Amplitude'
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating wave plot: {e}")
            return None
    
    def create_cymatics_plot(self, pattern_data: Dict, title: str = "Cymatics Pattern") -> Optional[Any]:
        """
        Create cymatics pattern plot.
        
        Args:
            pattern_data: Pattern data dictionary
            title: Plot title
            
        Returns:
            Plotly figure or None
        """
        if not self.has_plotly:
            logger.warning("Plotly not available, cannot create cymatics plot")
            return None
        
        try:
            fig = go.Figure()
            
            pattern = np.array(pattern_data['pattern'])
            
            fig.add_trace(go.Contour(
                x=pattern_data['x'],
                y=pattern_data['y'],
                z=pattern,
                colorscale='Viridis'
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title='X',
                yaxis_title='Y'
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating cymatics plot: {e}")
            return None
    
    def create_harmonic_plot(self, harmonic_data: Dict, title: str = "Harmonic Series") -> Optional[Any]:
        """
        Create harmonic series plot.
        
        Args:
            harmonic_data: Harmonic data dictionary
            title: Plot title
            
        Returns:
            Plotly figure or None
        """
        if not self.has_plotly:
            logger.warning("Plotly not available, cannot create harmonic plot")
            return None
        
        try:
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=[f"H{i+1}" for i in range(len(harmonic_data['frequencies']))],
                y=harmonic_data['amplitudes'],
                name="Amplitude"
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title='Harmonic',
                yaxis_title='Amplitude'
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating harmonic plot: {e}")
            return None
    
    def create_chakra_plot(self, chakra_data: Dict, title: str = "Chakra Visualization") -> Optional[Any]:
        """
        Create chakra visualization plot.
        
        Args:
            chakra_data: Chakra data dictionary
            title: Plot title
            
        Returns:
            Plotly figure or None
        """
        if not self.has_plotly:
            logger.warning("Plotly not available, cannot create chakra plot")
            return None
        
        try:
            fig = go.Figure()
            
            chakras = chakra_data.get('chakras', [])
            
            for chakra in chakras:
                fig.add_trace(go.Scatter3d(
                    x=[chakra['position']['x']],
                    y=[chakra['position']['y']],
                    z=[chakra['position']['z']],
                    mode='markers',
                    marker=dict(
                        size=15,
                        color=chakra['color']
                    ),
                    name=chakra['name'],
                    text=f"{chakra['name']}<br>Frequency: {chakra['frequency']} Hz",
                    hovertemplate='%{text}<extra></extra>'
                ))
            
            fig.update_layout(
                title=title,
                scene=dict(
                    xaxis_title='X',
                    yaxis_title='Y',
                    zaxis_title='Z',
                    aspectmode='cube'
                )
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating chakra plot: {e}")
            return None


# Singleton instance
_visualization_engine = None

def get_visualization_engine() -> VisualizationEngine:
    """Get or create visualization engine singleton."""
    global _visualization_engine
    if _visualization_engine is None:
        _visualization_engine = VisualizationEngine()
    return _visualization_engine


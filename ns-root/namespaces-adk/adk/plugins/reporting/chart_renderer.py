"""
Chart Renderer - Enterprise Grade
==================================

This module provides high-quality chart rendering for PDF reports with enterprise-grade features including:
- Multiple chart types (bar, line, pie, scatter, area)
- Customizable styling and branding
- High-resolution output
- Legend and labeling support
- Multi-series data support
"""

import io
import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.figure import Figure
    import numpy as np
except ImportError:
    raise ImportError(
        "matplotlib is required for chart rendering. "
        "Install with: pip install matplotlib numpy"
    )

logger = logging.getLogger(__name__)


class ChartType(Enum):
    """Supported chart types."""
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    SCATTER = "scatter"
    AREA = "area"
    HORIZONTAL_BAR = "horizontal_bar"
    STACKED_BAR = "stacked_bar"


class ChartColorScheme(Enum):
    """Pre-defined color schemes."""
    CORPORATE = "corporate"
    MODERN = "modern"
    PASTEL = "pastel"
    BRIGHT = "bright"
    CUSTOM = "custom"


@dataclass
class ChartStyle:
    """Chart styling configuration."""
    figure_size: Tuple[int, int] = (10, 6)
    dpi: int = 300
    font_size: int = 12
    
    # Colors
    primary_colors: List[str] = None
    secondary_color: str = "#3498DB"
    accent_color: str = "#E74C3C"
    text_color: str = "#333333"
    grid_color: str = "#CCCCCC"
    background_color: str = "#FFFFFF"
    
    # Chart settings
    show_legend: bool = True
    show_grid: bool = True
    show_values: bool = False
    value_format: str = "{:.2f}"
    
    # Axis settings
    x_label: Optional[str] = None
    y_label: Optional[str] = None
    title_font_size: int = 16
    label_font_size: int = 12


@dataclass
class ChartData:
    """Chart data container."""
    labels: List[str]
    values: List[float]
    series_name: Optional[str] = None
    multi_series: Optional[Dict[str, List[float]]] = None


class ChartRenderer:
    """
    Enterprise-grade chart renderer for PDF reports.
    
    Features:
    - Multiple chart types (bar, line, pie, scatter, area)
    - Customizable styling and branding
    - High-resolution output
    - Legend and labeling support
    - Multi-series data support
    
    Performance Targets:
    - Single chart: <1s
    - 10 charts: <5s
    - Memory usage: <20MB
    """
    
    # Color scheme presets
    COLOR_SCHEMES = {
        ChartColorScheme.CORPORATE: [
            "#2C3E50", "#3498DB", "#E74C3C", "#F39C12", 
            "#27AE60", "#9B59B6", "#1ABC9C", "#34495E"
        ],
        ChartColorScheme.MODERN: [
            "#667EEA", "#764BA2", "#F093FB", "#F5576C",
            "#4FACFE", "#00F260", "#FA709A", "#FEE140"
        ],
        ChartColorScheme.PASTEL: [
            "#FFB5BA", "#AEC6CF", "#77DD77", "#FDFD96",
            "#F49AC2", "#B39EB5", "#FFB347", "#CB99C9"
        ],
        ChartColorScheme.BRIGHT: [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
            "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F"
        ]
    }
    
    def __init__(self, style: Optional[ChartStyle] = None):
        """
        Initialize chart renderer.
        
        Args:
            style: Chart styling configuration
        """
        self.style = style or ChartStyle()
        
        # Set default colors
        if self.style.primary_colors is None:
            self.style.primary_colors = self.COLOR_SCHEMES[ChartColorScheme.CORPORATE]
        
        # Setup matplotlib style
        plt.style.use('default')
        
        logger.info(
            f"ChartRenderer initialized with {len(self.style.primary_colors)} colors"
        )
    
    def render_bar_chart(
        self,
        data: ChartData,
        output_path: str,
        horizontal: bool = False,
        stacked: bool = False
    ) -> str:
        """
        Render bar chart.
        
        Args:
            data: Chart data
            output_path: Path to save chart image
            horizontal: Whether to render horizontal bars
            stacked: Whether to stack bars (multi-series)
            
        Returns:
            Path to generated chart image
        """
        logger.info(f"Rendering bar chart: {output_path}")
        
        fig, ax = plt.subplots(
            figsize=self.style.figure_size,
            dpi=self.style.dpi
        )
        
        if data.multi_series:
            # Multi-series bar chart
            x_positions = np.arange(len(data.labels))
            width = 0.8 / len(data.multi_series)
            
            for i, (series_name, values) in enumerate(data.multi_series.items()):
                color = self.style.primary_colors[i % len(self.style.primary_colors)]
                offset = i * width
                ax.bar(
                    x_positions + offset,
                    values,
                    width,
                    label=series_name,
                    color=color,
                    edgecolor='white',
                    linewidth=0.7
                )
            
            ax.set_xticks(x_positions + width * (len(data.multi_series) - 1) / 2)
            ax.set_xticklabels(data.labels, rotation=45, ha='right')
        
        else:
            # Single series bar chart
            color = self.style.primary_colors[0]
            
            if horizontal:
                ax.barh(data.labels, data.values, color=color)
                ax.set_xlabel(data.y_label or "Value")
                ax.set_ylabel(data.x_label or "Category")
            else:
                ax.bar(data.labels, data.values, color=color)
                ax.set_xlabel(data.x_label or "Category")
                ax.set_ylabel(data.y_label or "Value")
        
        # Apply styling
        self._apply_chart_styling(ax, data)
        
        # Save chart
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.style.dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Bar chart saved: {output_path}")
        return output_path
    
    def render_line_chart(
        self,
        data: ChartData,
        output_path: str,
        fill_area: bool = False
    ) -> str:
        """
        Render line chart.
        
        Args:
            data: Chart data
            output_path: Path to save chart image
            fill_area: Whether to fill area under line
            
        Returns:
            Path to generated chart image
        """
        logger.info(f"Rendering line chart: {output_path}")
        
        fig, ax = plt.subplots(
            figsize=self.style.figure_size,
            dpi=self.style.dpi
        )
        
        if data.multi_series:
            # Multi-series line chart
            for i, (series_name, values) in enumerate(data.multi_series.items()):
                color = self.style.primary_colors[i % len(self.style.primary_colors)]
                ax.plot(data.labels, values, marker='o', label=series_name, color=color, linewidth=2)
                
                if fill_area:
                    ax.fill_between(data.labels, values, alpha=0.3, color=color)
        else:
            # Single series line chart
            color = self.style.primary_colors[0]
            ax.plot(data.labels, data.values, marker='o', color=color, linewidth=2)
            
            if fill_area:
                ax.fill_between(data.labels, data.values, alpha=0.3, color=color)
        
        # Apply styling
        self._apply_chart_styling(ax, data)
        
        # Save chart
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.style.dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Line chart saved: {output_path}")
        return output_path
    
    def render_pie_chart(
        self,
        data: ChartData,
        output_path: str,
        donut: bool = False
    ) -> str:
        """
        Render pie chart.
        
        Args:
            data: Chart data
            output_path: Path to save chart image
            donut: Whether to render as donut chart
            
        Returns:
            Path to generated chart image
        """
        logger.info(f"Rendering pie chart: {output_path}")
        
        fig, ax = plt.subplots(
            figsize=self.style.figure_size,
            dpi=self.style.dpi
        )
        
        # Render pie chart
        colors = self.style.primary_colors[:len(data.labels)]
        wedges, texts, autotexts = ax.pie(
            data.values,
            labels=data.labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
        )
        
        # Make it a donut chart if requested
        if donut:
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            fig.gca().add_artist(centre_circle)
        
        # Apply styling
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
        
        ax.axis('equal')
        ax.set_title(data.series_name or "Distribution", fontsize=self.style.title_font_size)
        
        # Save chart
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.style.dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Pie chart saved: {output_path}")
        return output_path
    
    def render_scatter_chart(
        self,
        data: ChartData,
        output_path: str,
        x_values: Optional[List[float]] = None
    ) -> str:
        """
        Render scatter chart.
        
        Args:
            data: Chart data
            output_path: Path to save chart image
            x_values: X-axis values (defaults to labels converted to numbers)
            
        Returns:
            Path to generated chart image
        """
        logger.info(f"Rendering scatter chart: {output_path}")
        
        fig, ax = plt.subplots(
            figsize=self.style.figure_size,
            dpi=self.style.dpi
        )
        
        # Determine x values
        if x_values is None:
            x_values = list(range(len(data.labels)))
        
        # Render scatter plot
        color = self.style.primary_colors[0]
        ax.scatter(x_values, data.values, color=color, s=100, alpha=0.6, edgecolors='white')
        
        # Add labels if provided
        if len(data.labels) <= 20:
            for i, label in enumerate(data.labels):
                ax.annotate(label, (x_values[i], data.values[i]), 
                           xytext=(5, 5), textcoords='offset points')
        
        # Apply styling
        ax.set_xlabel(data.x_label or "X")
        ax.set_ylabel(data.y_label or "Y")
        ax.set_title(data.series_name or "Scatter Plot", fontsize=self.style.title_font_size)
        
        if self.style.show_grid:
            ax.grid(True, linestyle='--', alpha=0.7, color=self.style.grid_color)
        
        # Save chart
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.style.dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Scatter chart saved: {output_path}")
        return output_path
    
    def render_area_chart(
        self,
        data: ChartData,
        output_path: str
    ) -> str:
        """
        Render area chart.
        
        Args:
            data: Chart data
            output_path: Path to save chart image
            
        Returns:
            Path to generated chart image
        """
        logger.info(f"Rendering area chart: {output_path}")
        
        fig, ax = plt.subplots(
            figsize=self.style.figure_size,
            dpi=self.style.dpi
        )
        
        if data.multi_series:
            # Multi-series area chart
            for i, (series_name, values) in enumerate(data.multi_series.items()):
                color = self.style.primary_colors[i % len(self.style.primary_colors)]
                ax.fill_between(data.labels, values, alpha=0.5, label=series_name, color=color)
                ax.plot(data.labels, values, linewidth=2, color=color)
        else:
            # Single series area chart
            color = self.style.primary_colors[0]
            ax.fill_between(data.labels, data.values, alpha=0.5, color=color)
            ax.plot(data.labels, data.values, linewidth=2, color=color)
        
        # Apply styling
        self._apply_chart_styling(ax, data)
        
        # Save chart
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.style.dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Area chart saved: {output_path}")
        return output_path
    
    def _apply_chart_styling(self, ax, data: ChartData) -> None:
        """Apply consistent styling to chart."""
        # Set labels
        if data.x_label:
            ax.set_xlabel(data.x_label, fontsize=self.style.label_font_size)
        if data.y_label:
            ax.set_ylabel(data.y_label, fontsize=self.style.label_font_size)
        
        # Set title
        ax.set_title(data.series_name or "Chart", fontsize=self.style.title_font_size)
        
        # Show grid
        if self.style.show_grid:
            ax.grid(True, linestyle='--', alpha=0.7, color=self.style.grid_color)
        
        # Show legend for multi-series
        if data.multi_series and self.style.show_legend:
            ax.legend(loc='best')
        
        # Rotate x-axis labels if needed
        if len(data.labels) > 8:
            plt.xticks(rotation=45, ha='right')
        
        # Set colors
        ax.xaxis.label.set_color(self.style.text_color)
        ax.yaxis.label.set_color(self.style.text_color)
        ax.title.set_color(self.style.text_color)
        ax.tick_params(axis='x', colors=self.style.text_color)
        ax.tick_params(axis='y', colors=self.style.text_color)
    
    def render_to_bytes(self, chart_type: ChartType, data: ChartData, **kwargs) -> bytes:
        """
        Render chart to bytes.
        
        Args:
            chart_type: Type of chart to render
            data: Chart data
            **kwargs: Additional chart-specific parameters
            
        Returns:
            Chart image as bytes
        """
        # Render to buffer
        buffer = io.BytesIO()
        
        if chart_type == ChartType.BAR:
            self.render_bar_chart(data, buffer, **kwargs)
        elif chart_type == ChartType.LINE:
            self.render_line_chart(data, buffer, **kwargs)
        elif chart_type == ChartType.PIE:
            self.render_pie_chart(data, buffer, **kwargs)
        elif chart_type == ChartType.SCATTER:
            self.render_scatter_chart(data, buffer, **kwargs)
        elif chart_type == ChartType.AREA:
            self.render_area_chart(data, buffer, **kwargs)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
        
        # Get bytes
        chart_bytes = buffer.getvalue()
        buffer.close()
        
        return chart_bytes


def create_chart_renderer(
    color_scheme: str = "corporate",
    figure_size: Tuple[int, int] = (10, 6),
    dpi: int = 300
) -> ChartRenderer:
    """
    Factory function to create a chart renderer.
    
    Args:
        color_scheme: Color scheme name
        figure_size: Figure size (width, height)
        dpi: Resolution in dots per inch
        
    Returns:
        Configured ChartRenderer instance
    """
    # Map string to enum
    color_scheme_enum = ChartColorScheme(color_scheme.lower())
    
    # Get color scheme
    colors = ChartRenderer.COLOR_SCHEMES.get(
        color_scheme_enum,
        ChartRenderer.COLOR_SCHEMES[ChartColorScheme.CORPORATE]
    )
    
    # Create style
    style = ChartStyle(
        figure_size=figure_size,
        dpi=dpi,
        primary_colors=colors
    )
    
    return ChartRenderer(style=style)
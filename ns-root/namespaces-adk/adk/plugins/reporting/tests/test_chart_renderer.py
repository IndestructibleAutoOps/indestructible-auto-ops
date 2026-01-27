"""
Unit Tests for Chart Renderer
==============================

Tests for the enterprise-grade chart rendering system.
"""

import tempfile
from pathlib import Path

import pytest

from chart_renderer import (
    ChartRenderer,
    ChartData,
    ChartStyle,
    ChartType,
    ChartColorScheme,
    create_chart_renderer
)


@pytest.fixture
def temp_chart_dir():
    """Create temporary directory for chart files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def chart_renderer():
    """Create chart renderer instance."""
    return create_chart_renderer(
        color_scheme="corporate"
    )


@pytest.fixture
def sample_chart_data():
    """Create sample chart data."""
    return ChartData(
        labels=["A", "B", "C", "D", "E"],
        values=[10, 20, 30, 40, 50],
        series_name="Sample Chart"
    )


class TestChartRenderer:
    """Test suite for ChartRenderer."""
    
    def test_initialization(self):
        """Test chart renderer initialization."""
        renderer = ChartRenderer()
        
        assert renderer.style is not None
        assert renderer.style.primary_colors is not None
        assert len(renderer.style.primary_colors) > 0
    
    def test_custom_style_initialization(self):
        """Test initialization with custom style."""
        style = ChartStyle(
            figure_size=(12, 8),
            dpi=300,
            font_size=14
        )
        
        renderer = ChartRenderer(style=style)
        
        assert renderer.style.figure_size == (12, 8)
        assert renderer.style.dpi == 300
        assert renderer.style.font_size == 14
    
    def test_render_bar_chart(self, chart_renderer, sample_chart_data, temp_chart_dir):
        """Test rendering bar chart."""
        output_path = temp_chart_dir / "bar_chart.png"
        
        result = chart_renderer.render_bar_chart(sample_chart_data, str(output_path))
        
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
    
    def test_render_horizontal_bar_chart(self, chart_renderer, sample_chart_data, temp_chart_dir):
        """Test rendering horizontal bar chart."""
        output_path = temp_chart_dir / "horizontal_bar_chart.png"
        
        result = chart_renderer.render_bar_chart(
            sample_chart_data,
            str(output_path),
            horizontal=True
        )
        
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
    
    def test_render_stacked_bar_chart(self, chart_renderer, temp_chart_dir):
        """Test rendering stacked bar chart."""
        data = ChartData(
            labels=["A", "B", "C"],
            values=[],
            multi_series={
                "Series 1": [10, 20, 30],
                "Series 2": [15, 25, 35],
                "Series 3": [20, 30, 40]
            }
        )
        
        output_path = temp_chart_dir / "stacked_bar_chart.png"
        
        result = chart_renderer.render_bar_chart(
            data,
            str(output_path),
            stacked=True
        )
        
        assert Path(result).exists()
    
    def test_render_line_chart(self, chart_renderer, sample_chart_data, temp_chart_dir):
        """Test rendering line chart."""
        output_path = temp_chart_dir / "line_chart.png"
        
        result = chart_renderer.render_line_chart(sample_chart_data, str(output_path))
        
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
    
    def test_render_line_chart_with_fill(self, chart_renderer, sample_chart_data, temp_chart_dir):
        """Test rendering line chart with area fill."""
        output_path = temp_chart_dir / "line_chart_fill.png"
        
        result = chart_renderer.render_line_chart(
            sample_chart_data,
            str(output_path),
            fill_area=True
        )
        
        assert Path(result).exists()
    
    def test_render_pie_chart(self, chart_renderer, sample_chart_data, temp_chart_dir):
        """Test rendering pie chart."""
        output_path = temp_chart_dir / "pie_chart.png"
        
        result = chart_renderer.render_pie_chart(sample_chart_data, str(output_path))
        
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
    
    def test_render_donut_chart(self, chart_renderer, sample_chart_data, temp_chart_dir):
        """Test rendering donut chart."""
        output_path = temp_chart_dir / "donut_chart.png"
        
        result = chart_renderer.render_pie_chart(
            sample_chart_data,
            str(output_path),
            donut=True
        )
        
        assert Path(result).exists()
    
    def test_render_scatter_chart(self, chart_renderer, sample_chart_data, temp_chart_dir):
        """Test rendering scatter chart."""
        output_path = temp_chart_dir / "scatter_chart.png"
        
        result = chart_renderer.render_scatter_chart(sample_chart_data, str(output_path))
        
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
    
    def test_render_scatter_chart_with_x_values(self, chart_renderer, sample_chart_data, temp_chart_dir):
        """Test rendering scatter chart with custom x values."""
        x_values = [1, 2, 3, 4, 5]
        output_path = temp_chart_dir / "scatter_chart_x.png"
        
        result = chart_renderer.render_scatter_chart(
            sample_chart_data,
            str(output_path),
            x_values=x_values
        )
        
        assert Path(result).exists()
    
    def test_render_area_chart(self, chart_renderer, sample_chart_data, temp_chart_dir):
        """Test rendering area chart."""
        output_path = temp_chart_dir / "area_chart.png"
        
        result = chart_renderer.render_area_chart(sample_chart_data, str(output_path))
        
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
    
    def test_render_multi_series_chart(self, chart_renderer, temp_chart_dir):
        """Test rendering multi-series line chart."""
        data = ChartData(
            labels=["A", "B", "C", "D", "E"],
            values=[],
            multi_series={
                "Series 1": [10, 20, 30, 40, 50],
                "Series 2": [15, 25, 35, 45, 55],
                "Series 3": [20, 30, 40, 50, 60]
            }
        )
        
        output_path = temp_chart_dir / "multi_series_line.png"
        
        result = chart_renderer.render_line_chart(data, str(output_path))
        
        assert Path(result).exists()
    
    def test_render_to_bytes(self, chart_renderer, sample_chart_data):
        """Test rendering chart to bytes."""
        chart_bytes = chart_renderer.render_to_bytes(
            ChartType.BAR,
            sample_chart_data
        )
        
        assert isinstance(chart_bytes, bytes)
        assert len(chart_bytes) > 0


class TestChartData:
    """Test suite for ChartData."""
    
    def test_chart_data_creation(self):
        """Test creating chart data."""
        data = ChartData(
            labels=["A", "B", "C"],
            values=[10, 20, 30],
            series_name="Test Chart"
        )
        
        assert data.labels == ["A", "B", "C"]
        assert data.values == [10, 20, 30]
        assert data.series_name == "Test Chart"
        assert data.multi_series is None
    
    def test_multi_series_chart_data(self):
        """Test multi-series chart data."""
        data = ChartData(
            labels=["A", "B", "C"],
            values=[],
            multi_series={
                "Series 1": [10, 20, 30],
                "Series 2": [15, 25, 35]
            }
        )
        
        assert data.multi_series is not None
        assert "Series 1" in data.multi_series
        assert "Series 2" in data.multi_series


class TestChartStyle:
    """Test suite for ChartStyle."""
    
    def test_default_style(self):
        """Test default style configuration."""
        style = ChartStyle()
        
        assert style.figure_size == (10, 6)
        assert style.dpi == 300
        assert style.font_size == 12
        assert style.show_legend is True
        assert style.show_grid is True
        assert style.primary_colors is None
    
    def test_custom_style(self):
        """Test custom style configuration."""
        style = ChartStyle(
            figure_size=(12, 8),
            dpi=150,
            font_size=14,
            show_legend=False,
            show_grid=False
        )
        
        assert style.figure_size == (12, 8)
        assert style.dpi == 150
        assert style.font_size == 14
        assert style.show_legend is False
        assert style.show_grid is False


class TestFactoryFunction:
    """Test suite for factory functions."""
    
    def test_create_chart_renderer(self):
        """Test creating chart renderer via factory function."""
        renderer = create_chart_renderer(
            color_scheme="corporate"
        )
        
        assert isinstance(renderer, ChartRenderer)
    
    def test_create_chart_renderer_different_schemes(self):
        """Test creating renderer with different color schemes."""
        schemes = ["corporate", "modern", "pastel", "bright"]
        
        for scheme in schemes:
            renderer = create_chart_renderer(color_scheme=scheme)
            assert isinstance(renderer, ChartRenderer)
            assert renderer.style.primary_colors is not None


class TestColorSchemes:
    """Test suite for color schemes."""
    
    def test_color_schemes_exist(self):
        """Test that all color schemes are defined."""
        schemes = [
            ChartColorScheme.CORPORATE,
            ChartColorScheme.MODERN,
            ChartColorScheme.PASTEL,
            ChartColorScheme.BRIGHT
        ]
        
        for scheme in schemes:
            assert scheme in ChartRenderer.COLOR_SCHEMES
    
    def test_color_scheme_colors(self):
        """Test color scheme color values."""
        corporate_colors = ChartRenderer.COLOR_SCHEMES[ChartColorScheme.CORPORATE]
        
        assert isinstance(corporate_colors, list)
        assert len(corporate_colors) > 0
        
        # Check color format (hex)
        for color in corporate_colors:
            assert color.startswith("#")
            assert len(color) == 7


class TestPerformance:
    """Performance tests for chart renderer."""
    
    def test_single_chart_performance(self, chart_renderer, sample_chart_data, temp_chart_dir):
        """Test performance for single chart."""
        output_path = temp_chart_dir / "perf_single.png"
        
        import time
        start_time = time.time()
        chart_renderer.render_bar_chart(sample_chart_data, str(output_path))
        elapsed_time = time.time() - start_time
        
        # Should be <1s for single chart
        assert elapsed_time < 1.0, f"Single chart took {elapsed_time:.2f}s (target: <1s)"
    
    def test_multiple_charts_performance(self, chart_renderer, sample_chart_data, temp_chart_dir):
        """Test performance for multiple charts."""
        chart_types = [
            (chart_renderer.render_bar_chart, sample_chart_data),
            (chart_renderer.render_line_chart, sample_chart_data),
            (chart_renderer.render_pie_chart, sample_chart_data),
            (chart_renderer.render_area_chart, sample_chart_data),
            (chart_renderer.render_scatter_chart, sample_chart_data)
        ]
        
        import time
        start_time = time.time()
        
        for i, (render_func, data) in enumerate(chart_types):
            output_path = temp_chart_dir / f"perf_multi_{i}.png"
            render_func(data, str(output_path))
        
        elapsed_time = time.time() - start_time
        
        # Should be <5s for 5 charts
        assert elapsed_time < 5.0, f"Multiple charts took {elapsed_time:.2f}s (target: <5s)"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
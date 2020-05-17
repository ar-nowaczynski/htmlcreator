import base64
import pathlib
from io import BytesIO
from typing import Optional, Union

import numpy as np
import pandas as pd
import PIL
import plotly
from PIL import Image


class HTMLDocument:
    """HTML Document class."""

    def __init__(self) -> None:
        self.style = ''
        self.title = self.__class__.__name__
        self.head = ''
        self.body = ''
        self._is_plotlyjs_included = False
        self._set_default_style()

    def __str__(self) -> str:
        return (
            '<!DOCTYPE html>\n'
            '<html lang="en">\n'
            '<head>\n'
            '<meta charset="UTF-8">\n'
            f'<title>{self.title}</title>\n'
            f'<style type="text/css">\n{self.style}</style>\n'
            f'{self.head}'
            '</head>\n'
            '<body>\n'
            f'{self.body}'
            '</body>\n'
            '</html>\n'
        )

    def add_header(
        self,
        header: str,
        level: str = 'h2',
        align: str = 'left',
    ) -> None:
        """Add header."""
        self.body += (
            f'<{level} style="text-align: {align}">'
            f'{header}'
            f'</{level}>\n'
        )

    def add_text(
        self,
        text: str,
        size: str = '16px',
        indent: str = '0',
        align: str = 'left',
    ) -> None:
        """Add text paragraph."""
        self.body += (
            f'<p style="font-size:{size}; text-indent: {indent}; text-align: {align}">'
            f'{text}'
            '</p>\n'
        )

    def add_line_break(self) -> None:
        """Add line break."""
        self.body += '<br>\n'

    def add_page_break(self) -> None:
        """Add page break."""
        self.body += '<p style="page-break-after: always;">&nbsp;</p>\n'

    def add_table(self, df: pd.DataFrame) -> None:
        """Embed pandas DataFrame."""
        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                f'df is of type {type(df)}, but it should be of type {pd.DataFrame}.'
            )
        self.body += (
            '<div class="pandas-dataframe">\n'
            f'{df.to_html()}\n'
            '</div>\n'
        )

    def add_image(
        self,
        image: Union[np.ndarray, PIL.Image.Image, pathlib.Path, str],
        title: Optional[str] = None,
        height: Optional[Union[int, str]] = None,
        width: Optional[Union[int, str]] = None,
        pixelated: bool = False,
    ) -> None:
        """Embed image."""
        image_encoded_str = self._encode_image(image)
        image_src = f'data:image/png;base64, {image_encoded_str}'
        self._add_image_tag(
            src=image_src,
            title=title,
            height=height,
            width=width,
            pixelated=pixelated,
        )

    def add_image_link(
        self,
        image_link: Union[pathlib.Path, str],
        title: Optional[str] = None,
        height: Optional[Union[int, str]] = None,
        width: Optional[Union[int, str]] = None,
        pixelated: bool = False,
    ) -> None:
        """Add image link (filepath or URL)."""
        if isinstance(image_link, pathlib.Path):
            image_src = str(image_link)
        elif isinstance(image_link, str):
            image_src = image_link
        else:
            raise TypeError(
                f'image_link is of type {type(image_link)}, '
                f'but it should be {pathlib.Path} or {str}.'
            )
        self._add_image_tag(
            src=image_src,
            title=title,
            height=height,
            width=width,
            pixelated=pixelated,
        )

    def add_plotly_figure(
        self,
        fig: plotly.graph_objs.Figure,
        include_plotlyjs: bool = True,
    ) -> None:
        """Add plotly figure."""
        if not isinstance(fig, plotly.graph_objs.Figure):
            raise TypeError(
                f'fig is of type {type(fig)}, '
                f'but it should be {plotly.graph_objs.Figure}.'
            )
        if self._is_plotlyjs_included:
            include_plotlyjs = False
        elif include_plotlyjs:
            self._is_plotlyjs_included = True
        else:
            include_plotlyjs = 'cdn'
        plotly_figure_html = plotly.io.to_html(
            fig=fig,
            full_html=False,
            include_plotlyjs=include_plotlyjs,
        )
        self.body += (
            '<div class="plotly-figure">\n'
            f'{plotly_figure_html}\n'
            '</div>\n'
        )

    def set_style(self, style: str) -> None:
        """Set CSS style."""
        self.style = style

    def set_title(self, title: str) -> None:
        """Set title."""
        self.title = title

    def write(self, filepath: str) -> None:
        """Save to filepath."""
        with open(filepath, 'w') as f:
            f.write(str(self))

    def _add_image_tag(
        self,
        src: str,
        title: Optional[str] = None,
        height: Optional[Union[int, str]] = None,
        width: Optional[Union[int, str]] = None,
        pixelated: bool = False,
    ) -> None:
        """Add image tag."""
        image_tag = f'<img src="{src}"'
        if title:
            image_tag += f' title="{title}"'
        if height:
            image_tag += f' height={height}'
        if width:
            image_tag += f' width={width}'
        image_tag += ' style="border:1px solid #021a40; margin: 3px 3px'
        if pixelated:
            image_tag += '; image-rendering: pixelated'
        image_tag += '">\n'
        self.body += image_tag

    def _encode_image(
        self,
        image: Union[np.ndarray, PIL.Image.Image, pathlib.Path, str],
    ) -> str:
        """Encode image to base64 string."""
        if isinstance(image, np.ndarray):
            if image.dtype != np.uint8:
                raise RuntimeError(
                    f'image.dtype is {image.dtype}, but it should be uint8.'
                )
            if not (image.ndim == 2 or image.ndim == 3):
                raise RuntimeError(
                    f'image.ndim is {image.ndim}, but it should be 2 or 3.'
                )
            buff = BytesIO()
            Image.fromarray(image).save(buff, format='PNG')
            encoded = base64.b64encode(buff.getvalue())
        elif isinstance(image, PIL.Image.Image):
            buff = BytesIO()
            image.save(buff, format='PNG')
            encoded = base64.b64encode(buff.getvalue())
        elif isinstance(image, pathlib.Path):
            encoded = base64.b64encode(open(str(image), 'rb').read())
        elif isinstance(image, str):
            encoded = base64.b64encode(open(image, 'rb').read())
        else:
            raise TypeError(
                f'image is of type {type(image)}, but it should be one of: '
                f'{np.ndarray}, {PIL.Image.Image}, {pathlib.Path} or {str}.'
            )
        image_encoded_str = encoded.decode('utf-8')
        return image_encoded_str

    def _set_default_style(self) -> None:
        """Set default style."""
        self_filename = pathlib.Path(__file__)
        self_filepath = self_filename.resolve()
        package_dirpath = self_filepath.parent
        style_filepath = package_dirpath / 'style.css'
        with open(str(style_filepath)) as f:
            style = f.read()
        self.set_style(style)

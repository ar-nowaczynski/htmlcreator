import os
import pathlib

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

from htmlcreator import HTMLDocument

np.random.seed(123)

_TEST_IMAGE_PATH = '_test_image.jpg'
_TEST_DOCUMENT_PATH = '_test_document.html'


def test_HTMLDocument():
    document = HTMLDocument()

    assert document.css

    document.set_title(title='title')

    document.add_header(header='header', level='h2', align='left')

    document.add_paragraph(text='text', size='15px', indent='0', align='left')

    document.add_line_break()

    document.add_table(df=_get_df())

    try:
        document.add_table(df=[_get_df()])
    except Exception as e:
        assert isinstance(e, TypeError)
        assert str(e) == "df is of type <class 'list'>, but it should be of type <class 'pandas.core.frame.DataFrame'>."

    document.add_page_break()

    document.add_image(image=_get_image_array(), title='image from array', height=320, width=480, pixelated=False)

    document.add_image(image=_get_PIL_Image(), title='image from PIL')

    _create_test_image()

    document.add_image(image=pathlib.Path(_TEST_IMAGE_PATH), title='image from Path')

    document.add_image_link(image_link=_TEST_IMAGE_PATH, title='image link from filepath', width='50%')

    document.add_image_link(image_link=pathlib.Path(_TEST_IMAGE_PATH), title='image link from Path')

    try:
        document.add_image(image=_get_image_array().astype(np.float32))
    except Exception as e:
        assert isinstance(e, RuntimeError)
        assert str(e) == 'image.dtype is float32, but it should be uint8.'

    try:
        document.add_image(image=np.random.randint(0, 256, size=(1, 200, 200, 3)).astype(np.uint8))
    except Exception as e:
        assert isinstance(e, RuntimeError)
        assert str(e) == 'image.ndim is 4, but it should be 2 or 3.'

    try:
        document.add_image(image=[_get_image_array()])
    except Exception as e:
        assert isinstance(e, TypeError)
        assert str(e) == "image is of type <class 'list'>, but it should be one of: <class 'numpy.ndarray'>, <class 'PIL.Image.Image'> or <class 'pathlib.Path'>."

    try:
        document.add_image_link(image_link=_get_image_array())
    except Exception as e:
        assert isinstance(e, TypeError)
        assert str(e) == "image_link is of type <class 'numpy.ndarray'>, but it should be <class 'pathlib.Path'> or <class 'str'>."

    document.add_plotly_figure(fig=_get_plotly_figure())

    try:
        document.add_plotly_figure(fig=_get_image_array())
    except Exception as e:
        assert isinstance(e, TypeError)
        assert str(e) == "fig is of type <class 'numpy.ndarray'>, but it should be <class 'plotly.graph_objs._figure.Figure'>."

    document.write(_TEST_DOCUMENT_PATH)

    assert os.path.exists(_TEST_DOCUMENT_PATH)

    _remove_test_document()

    _remove_test_image()


def _get_df():
    num_rows = 10
    num_cols = 20
    df = pd.DataFrame(
        data=np.random.randn(num_rows, num_cols),
        index=pd.date_range('19700101', periods=num_rows),
        columns=[f'c{i}' for i in range(num_cols)],
    )
    df['col_str'] = 'value_str'
    df.index.name = 'date'
    return df


def _get_image_array():
    return np.random.randint(0, 256, size=(200, 200, 3)).astype(np.uint8)


def _get_PIL_Image():
    return Image.fromarray(_get_image_array())


def _get_plotly_figure():
    x = np.arange(10)
    fig = go.Figure(data=go.Scatter(x=x, y=x**2))
    return fig


def _create_test_image():
    _get_PIL_Image().save(_TEST_IMAGE_PATH)


def _remove_test_image():
    if os.path.exists(_TEST_IMAGE_PATH):
        os.remove(_TEST_IMAGE_PATH)


def _remove_test_document():
    if os.path.exists(_TEST_DOCUMENT_PATH):
        os.remove(_TEST_DOCUMENT_PATH)


if __name__ == '__main__':
    test_HTMLDocument()

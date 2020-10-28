import numpy as np
import pytest


@pytest.mark.filterwarnings("ignore:data shape:UserWarning")
def test_big_2D_image(make_test_viewer):
    """Test big 2D image with axis exceeding max texture size."""
    viewer = make_test_viewer()

    shape = (20_000, 10)
    data = np.random.random(shape)
    layer = viewer.add_image(data, multiscale=False)
    visual = viewer.window.qt_viewer.layer_to_visual[layer]
    assert visual.node is not None
    if visual.MAX_TEXTURE_SIZE_2D is not None:
        s = np.ceil(np.divide(shape, visual.MAX_TEXTURE_SIZE_2D)).astype(int)
        assert np.all(layer._transforms['tile2data'].scale == s)


@pytest.mark.filterwarnings("ignore:data shape:UserWarning")
def test_big_3D_image(make_test_viewer):
    """Test big 3D image with axis exceeding max texture size."""
    viewer = make_test_viewer(ndisplay=3)

    shape = (5, 10, 3_000)
    data = np.random.random(shape)
    layer = viewer.add_image(data, multiscale=False)
    visual = viewer.window.qt_viewer.layer_to_visual[layer]
    assert visual.node is not None
    if visual.MAX_TEXTURE_SIZE_3D is not None:
        s = np.ceil(np.divide(shape, visual.MAX_TEXTURE_SIZE_3D)).astype(int)
        assert np.all(layer._transforms['tile2data'].scale == s)


@pytest.mark.parametrize(
    "shape", [(2, 4), (256, 4048), (4, 20_000), (20_000, 4)],
)
@pytest.mark.filterwarnings("ignore:data shape:UserWarning")
def test_downsample_value(make_test_viewer, shape):
    """Test getting correct value for downsampled data."""
    viewer = make_test_viewer()

    data = np.zeros(shape)
    data[shape[0] // 2 :, shape[1] // 2 :] = 1
    layer = viewer.add_image(data, multiscale=False)

    test_points = [
        (int(shape[0] * 0.25), int(shape[1] * 0.25)),
        (int(shape[0] * 0.75), int(shape[1] * 0.25)),
        (int(shape[0] * 0.25), int(shape[1] * 0.75)),
        (int(shape[0] * 0.75), int(shape[1] * 0.75)),
    ]
    expected_values = [0.0, 0.0, 0.0, 1.0]

    for test_point, expected_value in zip(test_points, expected_values):
        viewer.cursor.position = test_point
        assert layer.get_value() == expected_value

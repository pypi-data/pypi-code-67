from pathlib import Path

import dash_html_components as html
from dash.dependencies import Input, Output, State

import dash_uploader.settings as settings


def create_dash_callback(callback, settings):
    def wrapper(iscompleted, filenames, upload_id):
        if not iscompleted:
            return

        out = []
        if not filenames is None:
            if upload_id:
                root_folder = Path(settings.UPLOAD_FOLDER_ROOT) / upload_id
            else:
                root_folder = Path(settings.UPLOAD_FOLDER_ROOT)

            for filename in filenames:
                file = root_folder / filename
                out.append(str(file))

        return callback(out)

    return wrapper


def callback(
    output,
    id='dash-uploader',
):
    """
    Add a callback to dash application.
    This callback fires when upload is completed.
    Note: Must be called after du.configure_upload!

    Parameters
    ----------
    output: dash Ouput
        The output dash component
    id: str 
        The id of the du.Upload component.

    Example
    -------
    @du.callback(
       output=Output('callback-output', 'children'),
       id='dash-uploader',
    )
    def get_a_list(filenames):
        return html.Ul([html.Li(filenames)])


    """
    def add_callback(function):
        """
        Parameters
        ---------
        function: callable
            Function that receivers one argument,
            filenames and returns one argument,
            a dash component. The filenames is either
            None or list of str containing the uploaded 
            file(s).
        output: dash.dependencies.Output
            The dash output. For example:
            Output('callback-output', 'children')

        """
        dash_callback = create_dash_callback(
            function,
            settings,
        )

        if not hasattr(settings, 'app'):
            raise Exception(
                'The du.configure_upload must be called before the @du.callback can be used! Please, configure the dash-uploader.'
            )

        dash_callback = settings.app.callback(
            output,
            [Input(id, 'isCompleted')],
            [State(id, 'fileNames'),
             State(id, 'upload_id')],
        )(dash_callback)
        return function

    return add_callback

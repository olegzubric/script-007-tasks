import json

from aiohttp import web
import server.FileService as FileService
from utils import StrUtils


class WebHandler:
    """aiohttp handler with coroutines."""

    def __init__(self, path: str) -> None:
        FileService.change_dir(path)

    async def handle(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Basic coroutine for connection testing.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with status.
        """

        return web.json_response(data={
            'status': 'success'
        })

    async def change_dir(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for changing working directory with files.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                "path": "string. Directory path. Required",
            }.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        result = ''
        stream = request.content
        while not stream.at_eof():
            line = await stream.read()
            result += line.decode()

        try:
            data = json.loads(result)
            path = data.get('path')
            FileService.change_dir(path, autocreate=True)
            return web.json_response(data={
                'status': 'success',
                'message': f'You successfully changed working directory path. New path is {path}',
            })

        except (RuntimeError, ValueError) as err:
            raise web.HTTPBadRequest(text=f'got error {str(err)}')

    @staticmethod
    def _stringify_filedata(filedata):
        filedata['create_date'] = StrUtils.json_serialize_helper(filedata['create_date'])
        if 'edit_date' in filedata:
            filedata['edit_date'] = StrUtils.json_serialize_helper(filedata['edit_date'])
        if 'content' in filedata:
            filedata['content'] = StrUtils.bytes2str(filedata['content'])
        return filedata


    async def get_files(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for getting info about all files in working directory.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with success status and data or error status and error message.
        """

        data = FileService.get_files()
        for item in data:
            WebHandler._stringify_filedata(item)

        return web.json_response(data={
            'status': 'success',
            'data': data,
        })


    async def get_file_data(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for getting full info about file in working directory.

        Args:
            request (Request): aiohttp request, contains filename and is_signed parameters.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        match_info = request.match_info
        if 'filename' not in match_info:
            raise web.HTTPBadRequest(text='Parameter "filename" is not set')
        filename = match_info['filename']

        try:
            filedata = FileService.get_file_data(filename)
        except (RuntimeError, ValueError) as err:
            raise web.HTTPBadRequest(text=f'got error {str(err)}')

        filedata = WebHandler._stringify_filedata(filedata)
        return web.json_response(data={
            'status': 'success',
            'data': filedata,
        })


    async def create_file(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for creating file.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                'filename': 'string. filename',
                'content': 'string. Content string. Optional',
            }.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        result = ''
        stream = request.content
        while not stream.at_eof():
            line = await stream.read()
            result += line.decode()

        data = json.loads(result)
        filename = data.get('filename')
        content = data.get('content', None)

        try:
            filedata = FileService.create_file(filename, content)
        except (RuntimeError, ValueError) as err:
            raise web.HTTPBadRequest(text=f'got error {str(err)}')

        filedata = WebHandler._stringify_filedata(filedata)
        return web.json_response(data={
            'status': 'success',
            'data': filedata,
        })


    async def delete_file(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for deleting file.

        Args:
            request (Request): aiohttp request, contains filename.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """

        if 'filename' not in request.match_info:
            raise web.HTTPBadRequest(text='Parameter "filename" is not set')
        filename = request.match_info['filename']

        try:
            FileService.delete_file(filename)
            return web.json_response(data={
                'status': 'success',
                'message': f'File {filename} is successfully deleted',
            })
        except (RuntimeError, ValueError) as err:
            raise web.HTTPBadRequest(text=f'got error {str(err)}')

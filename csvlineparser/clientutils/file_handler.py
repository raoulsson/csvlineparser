from __future__ import annotations

import glob
import logging
import os
import pathlib
import shutil
from io import StringIO, BytesIO
from pathlib import Path

logger = logging.getLogger(__name__)


class FileHandler:

    def __init__(self) -> None:
        super().__init__()

    def delete_folder_contents(self, dst_path: str) -> None:
        for filename in os.listdir(dst_path):
            if filename == '.marker':
                continue
            file_path = os.path.join(dst_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logger.info('Failed to delete %s. Reason: %s' % (file_path, e))
        logger.info(f'Cleaned workbench folder: {dst_path}')

    def store_text_file(self, file_handle, dst_path: str) -> None:
        if dst_path == '/dev/null':
            """ ignore, we do this sometimes """
            return
        with open(dst_path, 'w') as f:
            f.write(file_handle)

    def store_binary_file(self, file_handle, dst_path: str) -> None:
        self.store_text_file(file_handle, dst_path)

    def copy_file(self, src_path: str, dst_path: str) -> None:
        shutil.copyfile(src_path, dst_path)
        logger.info(f'Local file copy. From: {src_path}, to: {dst_path}')

    def load_text_file_to_list(self, src_path: str) -> list[str]:
        with open(src_path, 'r', encoding='UTF-8') as f:
            lines = [line.rstrip() for line in f]
            return lines

    def load_text_file_to_buffer(self, src_path: str) -> StringIO:
        lines = self.load_text_file_to_list(src_path)
        my_buffer = StringIO()
        for line in lines:
            my_buffer.write(line + os.linesep)
        return my_buffer

    def load_binary_file_to_buffer(self, src_path: str) -> BytesIO:
        with open(src_path, "rb") as fh:
            my_buffer = BytesIO(fh.read())
        return my_buffer

    def store_buffer_to_file(self, my_buffer: StringIO | BytesIO, dst_path: str) -> None:
        mode = 'w'
        if type(my_buffer) == type(BytesIO()):
            mode = 'wb'
        logger.debug(f'Writing buffer to file: {dst_path}')
        my_buffer.seek(0)
        with open(dst_path, mode) as f:
            f.write(my_buffer.read())

    def file_exists(self, src_path: str) -> bool:
        return self.__exists(src_path)

    def directory_exists(self, src_path: str) -> bool:
        return self.__exists(src_path)

    def __exists(self, src_path: str) -> bool:
        file_handle = Path(src_path)
        return file_handle.exists()

    def list_files(self, src_path: str, file_type: str | None = None) -> list[str]:
        """ filetype must be the pure ending, like csv """
        if file_type is None:
            file_type = '*'
        file_list = []
        for file in glob.glob(src_path + '/*.' + file_type):
            file_list.append(file)
        return file_list

    def delete_file(self, src_path: str) -> None:
        file_handle = pathlib.Path(src_path)
        file_handle.unlink()

    def create_dir(self, src_path: str) -> None:
        os.mkdir(src_path)

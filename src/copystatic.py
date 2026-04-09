import shutil
import os
import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

def target_withing_working_directory(working_directory, target) -> str | None:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, target))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not os.path.isdir(target_dir):
        return None
    if not valid_target_dir:
        return f'Error: "{target}" is outside the permitted working directory'
    return None

def copy_directory_src_to_dest(working_directory: str, source: str, destination: str):
    if err_val:= target_withing_working_directory(working_directory, source):
        raise Exception(err_val)
    if err_val:= target_withing_working_directory(working_directory, destination):
        raise Exception(err_val)
    logger.debug(f'Making directory: "{destination}"')
    os.makedirs(destination, exist_ok=True)
    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        if os.path.isdir(src_path):
            logger.debug(f"Navigating to directory: {source} -> {item}")
            copy_directory_src_to_dest(working_directory, src_path, dest_path)
            continue
        logger.debug(f'Copying: "{src_path}" -> "{dest_path}"')
        shutil.copy(src_path, dest_path)
    return
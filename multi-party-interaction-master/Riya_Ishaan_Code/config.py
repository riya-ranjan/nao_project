import os.path


ROBOT_IP = "169.254.28.144"
ROBOT_PORT = 9559

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5678


def get_project_root():
    current_filepath = os.path.abspath(__file__)

    return os.path.dirname(current_filepath)


def to_path_str(curr_path, *path_parts):
    return os.path.abspath(os.path.join(curr_path, *path_parts))


# project root
projectRootPath = get_project_root()

debugScriptPath = to_path_str(projectRootPath, "debug_scripts")


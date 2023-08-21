import os

os.environ.setdefault("SETTINGS_MODULE", "config")

from teleapi.core.state import project_settings

if __name__ == '__main__':
    print(project_settings.DEBUG, project_settings.API_TOKEN)

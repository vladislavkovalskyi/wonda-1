from envparse import env
import os
from typing import NoReturn, Optional, Union


class Token(str):
    @classmethod
    def from_env(
        cls,
        file_name: Optional[str] = ".env",
        var_name: Optional[str] = "WONDA_TOKEN"
    ) -> Union["Token", NoReturn]:
        env_file_path = os.path.join(os.path.abspath(os.curdir), file_name)
        env.read_envfile(env_file_path)

        if not (token := env.str(var_name)):
            raise KeyError(f"Environment variable {var_name!r} not found!")
        return token

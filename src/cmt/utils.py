import subprocess
import tempfile


def edit_with_vim(message: str) -> str:
    with tempfile.NamedTemporaryFile(
        mode="w+",
        delete=False
    ) as tmp_file:
        tmp_file.write(message)
        tmp_file.flush()
        subprocess.run(["vim", tmp_file.name], check=True)
        tmp_file.seek(0)
        return tmp_file.read().strip()

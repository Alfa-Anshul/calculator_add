from __future__ import annotations

import base64
import io
import re
import shlex
import stat
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse

import paramiko

from ..config import get_settings

BASE_DIR = Path(__file__).resolve().parents[2]
COMMON_FASTAPI_CANDIDATES: list[tuple[str, str]] = [
    ("backend/main.py", "backend.main:app"),
    ("backend/backend.py", "backend.backend:app"),
    ("backend/app.py", "backend.app:app"),
    ("main.py", "main:app"),
    ("app/main.py", "app.main:app"),
    ("app.py", "app:app"),
]
COMMON_REQUIREMENTS_FILES = [
    "backend/requirements.txt",
    "requirements.txt",
]
SKIP_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}


def deploy_repo_in_docker(
    *,
    github_repo_url: str,
    branch: str = "main",
    app_name: str | None = None,
    fastapi_module: str | None = None,
    public_host: str | None = None,
    deploy_ssh_host: str | None = None,
    deploy_ssh_user: str | None = None,
    deploy_ssh_port: int | None = None,
    deploy_ssh_key_path: str | None = None,
    deploy_ssh_private_key: str | None = None,
    deploy_docker_command: str | None = None,
    github_token: str = "",
) -> dict[str, Any]:
    settings = get_settings()

    repo_url = _normalize_github_repo_url(github_repo_url)
    owner, repo = _parse_github_repo(repo_url)
    ssh_host = (deploy_ssh_host or settings.deploy_ssh_host).strip()
    if not ssh_host:
        raise ValueError("DEPLOY_SSH_HOST is not configured.")

    ssh_user = (deploy_ssh_user or settings.deploy_ssh_user).strip() or "ubuntu"
    ssh_port = int(deploy_ssh_port or settings.deploy_ssh_port)
    deploy_root = str(PurePosixPath(settings.deploy_base_dir.strip() or "/opt/mcp-deployments"))
    docker_command = _normalize_shell_command(deploy_docker_command or settings.deploy_docker_command)
    scheme = settings.deploy_public_scheme.strip() or "http"
    resolved_public_host = (public_host or settings.deploy_public_host or ssh_host).strip()
    if not resolved_public_host:
        raise ValueError("DEPLOY_PUBLIC_HOST is not configured.")

    slug = _slugify(app_name or repo)
    container_name = _trim_name(f"mcp-deploy-{slug}")
    image_name = container_name
    remote_project_dir = str(PurePosixPath(deploy_root) / slug)

    ssh = _connect_ssh(
        host=ssh_host,
        port=ssh_port,
        username=ssh_user,
        key_path=deploy_ssh_key_path or settings.deploy_ssh_key_path,
        private_key=deploy_ssh_private_key or settings.deploy_ssh_private_key,
    )
    try:
        _sync_repo_on_remote(
            ssh=ssh,
            repo_url=repo_url,
            branch=branch.strip() or "main",
            remote_project_dir=remote_project_dir,
            github_token=github_token,
        )

        sftp = ssh.open_sftp()
        try:
            resolved_fastapi_module = (
                fastapi_module.strip()
                if isinstance(fastapi_module, str) and fastapi_module.strip()
                else _detect_fastapi_module(sftp, remote_project_dir)
            )
            requirements_file = _detect_requirements_file(sftp, remote_project_dir)
            dockerfile_path = str(PurePosixPath(remote_project_dir) / ".mcp-deploy" / "Dockerfile")
            _write_remote_text(
                sftp,
                dockerfile_path,
                _render_dockerfile(
                    fastapi_module=resolved_fastapi_module,
                    requirements_file=requirements_file,
                ),
            )
        finally:
            sftp.close()

        existing_port = _get_existing_container_port(ssh, docker_command, container_name)
        host_port = existing_port or _find_open_remote_port(
            ssh,
            start=int(settings.deploy_port_start),
            end=int(settings.deploy_port_end),
        )

        _build_and_run_container(
            ssh=ssh,
            docker_command=docker_command,
            remote_project_dir=remote_project_dir,
            dockerfile_path=str(PurePosixPath(remote_project_dir) / ".mcp-deploy" / "Dockerfile"),
            image_name=image_name,
            container_name=container_name,
            host_port=host_port,
        )
        _wait_for_fastapi(
            ssh=ssh,
            docker_command=docker_command,
            container_name=container_name,
            host_port=host_port,
        )

        public_url = f"{scheme}://{resolved_public_host}:{host_port}"
        return {
            "deployed": True,
            "github_repo_url": repo_url,
            "repo_owner": owner,
            "repo_name": repo,
            "branch": branch.strip() or "main",
            "app_name": slug,
            "remote_project_dir": remote_project_dir,
            "container_name": container_name,
            "image_name": image_name,
            "fastapi_module": resolved_fastapi_module,
            "requirements_file": requirements_file,
            "public_url": public_url,
            "docs_url": f"{public_url}/docs",
            "port": host_port,
        }
    finally:
        ssh.close()


def _sanitize_github_token(raw_token: Any) -> str:
    token = str(raw_token or "").strip()
    if len(token) >= 2 and ((token[0] == '"' and token[-1] == '"') or (token[0] == "'" and token[-1] == "'")):
        token = token[1:-1].strip()
    return token


def _normalize_github_repo_url(repo_url: str) -> str:
    normalized = repo_url.strip()
    if not normalized:
        raise ValueError("github_repo_url is required.")
    if normalized.startswith("https://github.com/"):
        return normalized.removesuffix(".git")

    shorthand = normalized.strip("/")
    parts = [part for part in shorthand.split("/") if part]
    if len(parts) == 2:
        return f"https://github.com/{parts[0]}/{parts[1].removesuffix('.git')}"

    raise ValueError(
        "github_repo_url must be a valid GitHub repo URL like https://github.com/<owner>/<repo> or <owner>/<repo>."
    )


def _parse_github_repo(repo_url: str) -> tuple[str, str]:
    parsed = urlparse(repo_url)
    if parsed.scheme != "https" or parsed.netloc.lower() != "github.com":
        raise ValueError(
            "github_repo_url must be a valid GitHub repo URL like https://github.com/<owner>/<repo> or <owner>/<repo>."
        )

    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(parts) != 2:
        raise ValueError("github_repo_url must include owner and repository name.")
    return parts[0], parts[1].removesuffix(".git")


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "fastapi-app"


def _trim_name(value: str, max_length: int = 63) -> str:
    trimmed = value[:max_length].rstrip("-")
    return trimmed or value[:max_length]


def _normalize_shell_command(command: str) -> str:
    parts = shlex.split(command.strip() or "docker")
    return " ".join(shlex.quote(part) for part in parts)


def _connect_ssh(
    *,
    host: str,
    port: int,
    username: str,
    key_path: str,
    private_key: str,
) -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    resolved_key_path = _resolve_ssh_key_path(key_path)
    if resolved_key_path:
        client.connect(
            hostname=host,
            port=port,
            username=username,
            key_filename=resolved_key_path,
            look_for_keys=False,
            allow_agent=False,
            timeout=20,
        )
        return client

    pkey = _load_private_key(private_key)
    if pkey is None:
        raise ValueError(
            "SSH key is not configured. Set DEPLOY_SSH_KEY_PATH, mount mcp_automation.pem into the app, or set DEPLOY_SSH_PRIVATE_KEY."
        )

    client.connect(
        hostname=host,
        port=port,
        username=username,
        pkey=pkey,
        look_for_keys=False,
        allow_agent=False,
        timeout=20,
    )
    return client


def _resolve_ssh_key_path(configured_path: str) -> str:
    candidates: list[Path] = []
    if configured_path.strip():
        candidate = Path(configured_path.strip())
        candidates.append(candidate if candidate.is_absolute() else (BASE_DIR / candidate))
    candidates.append(BASE_DIR / "mcp_automation.pem")

    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return ""


def _load_private_key(private_key: str) -> paramiko.PKey | None:
    key_text = private_key.strip().replace("\\n", "\n")
    if not key_text:
        return None

    key_classes = (
        paramiko.RSAKey,
        paramiko.Ed25519Key,
        paramiko.ECDSAKey,
        paramiko.DSSKey,
    )
    for key_class in key_classes:
        try:
            return key_class.from_private_key(io.StringIO(key_text))
        except paramiko.SSHException:
            continue
    raise ValueError("DEPLOY_SSH_PRIVATE_KEY could not be parsed as a supported private key.")


def _run_remote(ssh: paramiko.SSHClient, script: str, *, check: bool = True) -> tuple[int, str, str]:
    command = f"bash -lc {shlex.quote(script)}"
    _, stdout, stderr = ssh.exec_command(command, timeout=900)
    exit_code = stdout.channel.recv_exit_status()
    out_text = stdout.read().decode("utf-8", errors="replace").strip()
    err_text = stderr.read().decode("utf-8", errors="replace").strip()
    if check and exit_code != 0:
        detail = err_text or out_text or f"remote command failed with exit code {exit_code}"
        raise RuntimeError(detail)
    return exit_code, out_text, err_text


def _sync_repo_on_remote(
    *,
    ssh: paramiko.SSHClient,
    repo_url: str,
    branch: str,
    remote_project_dir: str,
    github_token: str,
) -> None:
    remote_dir = PurePosixPath(remote_project_dir)
    base_dir = remote_dir.parent.as_posix()
    auth_exports, auth_unset = _git_auth_snippets(_sanitize_github_token(github_token))
    script = f"""
set -euo pipefail
REPO_URL={shlex.quote(repo_url)}
BRANCH={shlex.quote(branch)}
BASE_DIR={shlex.quote(base_dir)}
REPO_DIR={shlex.quote(remote_project_dir)}
mkdir -p "$BASE_DIR"
if [ -d "$REPO_DIR/.git" ]; then
  git -C "$REPO_DIR" remote set-url origin "$REPO_URL"
  {auth_exports}
  git -C "$REPO_DIR" fetch --depth 1 origin "$BRANCH"
  git -C "$REPO_DIR" checkout -B "$BRANCH" "origin/$BRANCH"
  git -C "$REPO_DIR" reset --hard "origin/$BRANCH"
  {auth_unset}
else
  rm -rf "$REPO_DIR"
  {auth_exports}
  git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$REPO_DIR"
  {auth_unset}
fi
git -C "$REPO_DIR" remote set-url origin "$REPO_URL"
"""
    _run_remote(ssh, script)


def _git_auth_snippets(token: str) -> tuple[str, str]:
    if not token:
        return ":", ":"

    basic_auth = base64.b64encode(f"x-access-token:{token}".encode("utf-8")).decode("ascii")
    auth_header = f"AUTHORIZATION: basic {basic_auth}"
    exports = "\n".join(
        [
            "export GIT_CONFIG_COUNT=1",
            "export GIT_CONFIG_KEY_0=http.https://github.com/.extraheader",
            f"export GIT_CONFIG_VALUE_0={shlex.quote(auth_header)}",
        ]
    )
    unsets = "unset GIT_CONFIG_COUNT GIT_CONFIG_KEY_0 GIT_CONFIG_VALUE_0"
    return exports, unsets


def _remote_exists(sftp: paramiko.SFTPClient, path: str) -> bool:
    try:
        sftp.stat(path)
        return True
    except OSError:
        return False


def _detect_fastapi_module(sftp: paramiko.SFTPClient, remote_project_dir: str) -> str:
    for rel_path, module in COMMON_FASTAPI_CANDIDATES:
        file_path = str(PurePosixPath(remote_project_dir) / rel_path)
        if not _remote_exists(sftp, file_path):
            continue
        text = _read_remote_text(sftp, file_path)
        if _looks_like_fastapi_app(text):
            return module

    for file_path in _iter_remote_python_files(sftp, remote_project_dir):
        text = _read_remote_text(sftp, file_path)
        if not _looks_like_fastapi_app(text):
            continue
        relative = PurePosixPath(file_path).relative_to(PurePosixPath(remote_project_dir))
        return f"{'.'.join(relative.with_suffix('').parts)}:app"

    raise ValueError(
        "Could not detect a FastAPI app in the repository. Add a file such as backend/main.py or pass fastapi_module explicitly."
    )


def _looks_like_fastapi_app(text: str) -> bool:
    return bool(re.search(r"\bapp\s*(?::[^=]+)?=\s*FastAPI\s*\(", text))


def _iter_remote_python_files(sftp: paramiko.SFTPClient, remote_root: str) -> list[str]:
    root = PurePosixPath(remote_root)
    pending = [root]
    results: list[str] = []
    while pending:
        current = pending.pop()
        for entry in sftp.listdir_attr(current.as_posix()):
            name = entry.filename
            child = current / name
            if stat.S_ISDIR(entry.st_mode):
                if name in SKIP_DIRS:
                    continue
                pending.append(child)
                continue
            if name.endswith(".py"):
                results.append(child.as_posix())
    return results


def _detect_requirements_file(sftp: paramiko.SFTPClient, remote_project_dir: str) -> str | None:
    for rel_path in COMMON_REQUIREMENTS_FILES:
        file_path = str(PurePosixPath(remote_project_dir) / rel_path)
        if _remote_exists(sftp, file_path):
            return rel_path
    return None


def _read_remote_text(sftp: paramiko.SFTPClient, path: str) -> str:
    with sftp.open(path, "rb") as handle:
        return handle.read().decode("utf-8", errors="replace")


def _render_dockerfile(*, fastapi_module: str, requirements_file: str | None) -> str:
    install_line = (
        f"RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r {requirements_file}"
        if requirements_file
        else "RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir fastapi uvicorn[standard]"
    )
    return "\n".join(
        [
            "FROM python:3.12-slim",
            "",
            "WORKDIR /app",
            "",
            "ENV PYTHONDONTWRITEBYTECODE=1",
            "ENV PYTHONUNBUFFERED=1",
            "",
            "COPY . /app",
            install_line,
            "",
            "EXPOSE 8000",
            f'CMD ["uvicorn", "{fastapi_module}", "--host", "0.0.0.0", "--port", "8000"]',
            "",
        ]
    )


def _ensure_remote_dir(sftp: paramiko.SFTPClient, remote_dir: str) -> None:
    current = PurePosixPath(remote_dir)
    parts = current.parts
    prefix = PurePosixPath(parts[0]) if parts and parts[0] == "/" else PurePosixPath(".")
    for part in parts[1:] if prefix.as_posix() == "/" else parts:
        prefix = prefix / part
        try:
            sftp.stat(prefix.as_posix())
        except OSError:
            sftp.mkdir(prefix.as_posix())


def _write_remote_text(sftp: paramiko.SFTPClient, path: str, content: str) -> None:
    _ensure_remote_dir(sftp, str(PurePosixPath(path).parent))
    with sftp.open(path, "wb") as handle:
        handle.write(content.encode("utf-8"))


def _get_existing_container_port(ssh: paramiko.SSHClient, docker_command: str, container_name: str) -> int | None:
    script = f"""
set -e
{docker_command} inspect -f '{{{{(index (index .NetworkSettings.Ports "8000/tcp") 0).HostPort}}}}' {shlex.quote(container_name)}
"""
    exit_code, stdout, _ = _run_remote(ssh, script, check=False)
    if exit_code != 0 or not stdout.strip():
        return None
    try:
        return int(stdout.strip())
    except ValueError:
        return None


def _find_open_remote_port(ssh: paramiko.SSHClient, *, start: int, end: int) -> int:
    script = f"""
python3 - <<'PY'
import socket

for port in range({start}, {end} + 1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(("0.0.0.0", port))
        except OSError:
            continue
        print(port)
        raise SystemExit(0)
raise SystemExit(1)
PY
"""
    _, stdout, _ = _run_remote(ssh, script)
    try:
        return int(stdout.strip())
    except ValueError as exc:
        raise RuntimeError("Could not allocate a free remote port for deployment.") from exc


def _build_and_run_container(
    *,
    ssh: paramiko.SSHClient,
    docker_command: str,
    remote_project_dir: str,
    dockerfile_path: str,
    image_name: str,
    container_name: str,
    host_port: int,
) -> None:
    script = f"""
set -euo pipefail
{docker_command} build -t {shlex.quote(image_name)} -f {shlex.quote(dockerfile_path)} {shlex.quote(remote_project_dir)}
{docker_command} rm -f {shlex.quote(container_name)} >/dev/null 2>&1 || true
{docker_command} run -d --name {shlex.quote(container_name)} --restart unless-stopped -p {host_port}:8000 {shlex.quote(image_name)}
"""
    _run_remote(ssh, script)


def _wait_for_fastapi(
    *,
    ssh: paramiko.SSHClient,
    docker_command: str,
    container_name: str,
    host_port: int,
) -> None:
    script = f"""
python3 - <<'PY'
import time
import urllib.request

url = "http://127.0.0.1:{host_port}/docs"
for _ in range(30):
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            if response.status < 500:
                raise SystemExit(0)
    except Exception:
        time.sleep(2)
raise SystemExit(1)
PY
"""
    exit_code, _, error_text = _run_remote(ssh, script, check=False)
    if exit_code == 0:
        return

    _, _, logs = _run_remote(
        ssh,
        f"{docker_command} logs --tail 80 {shlex.quote(container_name)}",
        check=False,
    )
    detail = logs or error_text or "FastAPI container did not become healthy in time."
    raise RuntimeError(detail)

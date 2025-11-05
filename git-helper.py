#!/usr/bin/env python3
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence


DEFAULT_BASE = Path.home() / "Documentos" / "Git"


@dataclass
class MenuOption:
    key: str
    label: str


def prompt_menu(title: str, options: Sequence[MenuOption]) -> Optional[MenuOption]:
    print(f"\n{title}")
    for option in options:
        print(f"[{option.key}] {option.label}")
    print("[q] Sair/voltar")

    while True:
        choice = input("> ").strip().lower()
        if choice in {"q", "quit"}:
            return None
        for option in options:
            if choice == option.key.lower():
                return option
        print("Opção inválida, tente novamente.")


def run_git(repo_path: Path, args: Sequence[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(repo_path),
        check=check,
        text=True,
        capture_output=True,
    )


def list_git_repositories(base_dir: Path) -> List[Path]:
    repos: List[Path] = []
    if not base_dir.exists():
        return repos

    for entry in base_dir.iterdir():
        if not entry.is_dir():
            continue
        git_dir = entry / ".git"
        if git_dir.exists():
            repos.append(entry)
            continue
        # procurar um nível abaixo
        try:
            for subentry in entry.iterdir():
                if subentry.is_dir() and (subentry / ".git").exists():
                    repos.append(subentry)
        except PermissionError:
            continue
    return sorted(set(repos))


def choose_repository(base_dir: Path) -> Optional[Path]:
    repos = list_git_repositories(base_dir)
    if not repos:
        print("Nenhum repositório encontrado. Use a opção de clonar primeiro.")
        return None

    options = [
        MenuOption(str(idx + 1), f"{repo.relative_to(base_dir)}")
        for idx, repo in enumerate(repos)
    ]
    choice = prompt_menu("Selecione o repositório:", options)
    if not choice:
        return None
    idx = int(choice.key) - 1
    return repos[idx]


def clone_repository(base_dir: Path) -> None:
    url = input("Informe a URL SSH/HTTPS do repositório: ").strip()
    if not url:
        print("URL inválida.")
        return

    target = input("Diretório de destino (vazio para padrão): ").strip()
    dest_arg: List[str] = []
    if target:
        dest = Path(target)
        if not dest.is_absolute():
            dest = base_dir / dest
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest_arg = [str(dest)]

    print("Clonando repositório...")
    try:
        subprocess.run(["git", "clone", url, *dest_arg], check=True)
        print("Clone concluído.")
    except subprocess.CalledProcessError as exc:
        print("Erro ao clonar repositório.")
        print(exc)


def show_git_status(repo: Path) -> None:
    result = run_git(repo, ["status"], check=False)
    print(result.stdout or result.stderr)


def check_remote_access(repo: Path) -> None:
    try:
        result = run_git(repo, ["remote", "get-url", "origin"])
    except subprocess.CalledProcessError:
        print("Repositório não possui remote 'origin' configurado.")
        return

    remote_url = result.stdout.strip()
    print(f"Verificando acesso a {remote_url} ...")
    try:
        ls_remote = run_git(repo, ["ls-remote", "origin"], check=False)
        if ls_remote.returncode == 0:
            print("Acesso verificado com sucesso.")
        else:
            print("Falha ao acessar o remoto.")
            if ls_remote.stderr:
                print(ls_remote.stderr)
    except subprocess.CalledProcessError as exc:
        print(f"Erro ao verificar remoto: {exc}")


def create_commit(repo: Path) -> None:
    status = run_git(repo, ["status", "--short"], check=False)
    if not status.stdout.strip():
        print("Não há alterações para commit.")
        return
    print("Alterações pendentes:\n" + status.stdout)
    confirm = input("Deseja prosseguir com git add -A e commit? (s/N): ").strip().lower()
    if confirm != "s":
        print("Commit cancelado.")
        return
    message = input("Mensagem do commit: ").strip()
    if not message:
        print("Mensagem vazia. Commit cancelado.")
        return
    try:
        run_git(repo, ["add", "-A"])
        run_git(repo, ["commit", "-m", message])
        print("Commit criado com sucesso.")
    except subprocess.CalledProcessError as exc:
        print("Erro ao criar commit.")
        print(exc.stderr)


def create_tag(repo: Path) -> None:
    latest = run_git(repo, ["tag", "--sort=-creatordate"], check=False).stdout.splitlines()
    if latest:
        print("Tags recentes:")
        for tag in latest[:5]:
            print(f" - {tag}")
    else:
        print("Nenhuma tag encontrada.")
    tag_name = input("Nome da nova tag (ex: v1.0.20): ").strip()
    if not tag_name:
        print("Nome de tag vazio. Operação cancelada.")
        return
    tag_msg = input("Mensagem da tag: ").strip()
    if not tag_msg:
        print("Mensagem de tag vazia. Operação cancelada.")
        return
    try:
        run_git(repo, ["tag", "-a", tag_name, "-m", tag_msg])
        print(f"Tag {tag_name} criada.")
    except subprocess.CalledProcessError as exc:
        print("Erro ao criar tag.")
        print(exc.stderr)


def push_changes(repo: Path) -> None:
    try:
        branch = run_git(repo, ["rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
    except subprocess.CalledProcessError:
        print("Não foi possível identificar a branch atual.")
        return

    print(f"Branch atual: {branch}")
    options = [
        MenuOption("1", "Enviar commits (git push origin <branch>)"),
        MenuOption("2", "Enviar tags pendentes (git push origin --tags)"),
        MenuOption("3", "Enviar commits e tags"),
    ]
    choice = prompt_menu("Selecione o tipo de push:", options)
    if not choice:
        return

    try:
        if choice.key == "1":
            run_git(repo, ["push", "origin", branch], check=True)
            print("Commits enviados com sucesso.")
        elif choice.key == "2":
            run_git(repo, ["push", "origin", "--tags"], check=True)
            print("Tags enviadas com sucesso.")
        elif choice.key == "3":
            run_git(repo, ["push", "origin", branch], check=True)
            run_git(repo, ["push", "origin", "--tags"], check=True)
            print("Commits e tags enviados com sucesso.")
    except subprocess.CalledProcessError as exc:
        print("Erro ao executar push.")
        print(exc.stderr)


def repo_menu(repo: Path) -> None:
    print(f"\nRepositório selecionado: {repo}")
    while True:
        option = prompt_menu(
            "Escolha uma ação:",
            [
                MenuOption("1", "Mostrar git status"),
                MenuOption("2", "Verificar acesso ao remoto"),
                MenuOption("3", "Criar commit"),
                MenuOption("4", "Criar tag"),
                MenuOption("5", "Enviar (push)"),
            ],
        )
        if option is None:
            break
        if option.key == "1":
            show_git_status(repo)
        elif option.key == "2":
            check_remote_access(repo)
        elif option.key == "3":
            create_commit(repo)
        elif option.key == "4":
            create_tag(repo)
        elif option.key == "5":
            push_changes(repo)


def determine_base_dir() -> Path:
    if len(sys.argv) > 1:
        base = Path(sys.argv[1]).expanduser()
    else:
        base = DEFAULT_BASE
    base.mkdir(parents=True, exist_ok=True)
    return base


def main() -> None:
    base_dir = determine_base_dir()
    print(f"Diretório base: {base_dir}")

    while True:
        option = prompt_menu(
            "Menu principal:",
            [
                MenuOption("1", "Clonar novo repositório"),
                MenuOption("2", "Trabalhar com repositório local"),
            ],
        )
        if option is None:
            print("Até breve!")
            return

        if option.key == "1":
            clone_repository(base_dir)
        elif option.key == "2":
            repo = choose_repository(base_dir)
            if repo:
                repo_menu(repo)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")

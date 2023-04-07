#!/usr/bin/python3
import argparse
import shutil
from pathlib import Path
from datetime import datetime


def create_backup(src: str, dst: str) -> None:
    """
    Creates a .zip backup of the src dir and places it at dst dir
    """
    source_dir = Path(src)
    backup_dir = Path(dst)

    backup_dir.mkdir(exist_ok=True)

    date_string = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = backup_dir.joinpath(f"{source_dir.name}{date_string}")

    backup_name = shutil.make_archive(backup_path, "zip", source_dir)
    print(f"Backup created: {backup_name}")


def delete_old_backups(dst: str, days: int) -> None:
    """
    Removes backups older than the specified number of days
    """
    if days < 0:
        return
    backup_dir = Path(dst)

    for backup in backup_dir.iterdir():
        if backup.is_file():
            timestamp = backup.stat().st_mtime
            age_days = (datetime.now() - datetime.fromtimestamp(timestamp)).days
            if age_days > days:
                backup.unlink()
                print(f"Removed backup: {backup}")


def get_args():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.description = "description"
    parser.add_argument("--src", "-s", help="Source directory", required=True)
    parser.add_argument("--dst", "-d", help="Destination directory", required=True)
    parser.add_argument(
        "--del_days_old",
        help="Delete backups older than x days. Set to -1 to prevent deleting",
        default=30,
        type=int,
    )
    args = parser.parse_args()
    return args


def main():
    """
    Main program
    """
    args = get_args()
    create_backup(args.src, args.dst)
    delete_old_backups(args.dst, args.del_days_old)


if __name__ == "__main__":
    main()

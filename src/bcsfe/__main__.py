from __future__ import annotations
import traceback

from bcsfe import cli, copy_to_data_dir

from bcsfe import core, __app_name__, __version__

import bcsfe
import argparse

from importlib import resources


def migrate(force: bool):
    v_path = core.Path.get_data_folder().add("version.txt")
    if not v_path.exists():
        try:
            v_path.parent().generate_dirs()
            v_path.write(core.Data(__version__))
        except FileNotFoundError:
            print(
                "데이터 폴더를 만들지 못했습니다. 사용자 권한이나 백신 프로그램 문제일 수 있습니다"
            )
            print("--data-dir 옵션으로 에디터가 쓸 수 있는 폴더를 지정해 주세요")
            pass
        vers = None
    else:
        vers = v_path.read().to_str().strip()
    # 한국어 번역판: ko 언어 파일이 데이터 폴더에 없으면 강제로 복사
    ko_missing = not core.Path.get_data_folder().add("locales").add("ko").exists()
    if vers != __version__ or force or ko_missing:
        p = resources.files(__app_name__).joinpath("files")
        copy_to_data_dir(p, p)
        v_path.write(core.Data(__version__))


def main():
    parser = argparse.ArgumentParser(bcsfe.__app_name__)

    parser.add_argument(
        "--version", "-v", action="store_true", help="버전을 표시하고 종료"
    )
    parser.add_argument(
        "--input-path", "-i", type=str, help="수정할 세이브 파일 경로"
    )
    parser.add_argument(
        "--game-data-dir", "-g", type=str, help="게임 데이터를 저장할 폴더"
    )
    parser.add_argument(
        "--data-dir", "-d", type=str, help="에디터 데이터를 저장할 폴더"
    )
    parser.add_argument(
        "--transfer-backup-path",
        type=str,
        help="기종 변경 후 백업 SAVE_DATA를 저장할 경로",
    )
    parser.add_argument(
        "--config-path",
        "-c",
        type=str,
        default=None,
        help=f"설정 파일 경로. 지정하지 않으면 {core.Config.get_config_path()}",
    )
    parser.add_argument(
        "--log-path",
        "-l",
        type=str,
        default=None,
        help=f"로그 파일 경로. 지정하지 않으면 {core.Logger.get_log_path()}",
    )
    parser.add_argument(
        "--force-migrate",
        action="store_true",
        help=f"bcsfe/src/files의 모든 데이터를 {core.Path.get_data_folder()}에 다시 복사",
    )

    args = parser.parse_args()
    if args.version:
        print(bcsfe.__version__)
        exit()

    if args.config_path is not None:
        core.set_config_path(core.Path(args.config_path))

    if args.log_path is not None:
        core.set_log_path(core.Path(args.log_path))

    if args.transfer_backup_path is not None:
        core.set_transfer_backup_path(core.Path(args.transfer_backup_path))

    if args.game_data_dir is not None:
        core.set_game_data_path(core.Path(args.game_data_dir))

    if args.data_dir is not None:
        core.set_data_dir_path(core.Path(args.data_dir))

    migrate(args.force_migrate)

    core.core_data.init_data()

    try:
        cli.main.Main().main(args.input_path)
    except KeyboardInterrupt:
        cli.main.Main.leave()
    except Exception as e:
        tb = traceback.format_exc()
        cli.color.color_print_key(
            "error", error=e, version=bcsfe.__version__, traceback=tb
        )
        try:
            cli.main.Main.exit_editor()
        except Exception:
            pass
        except KeyboardInterrupt:
            pass


main()

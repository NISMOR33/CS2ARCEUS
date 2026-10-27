import binascii
import ctypes
import json
from pathlib import Path
import zipfile

FILES_TO_INCLUDE = [
    "main.py",
    "db.py",
    "econ_defs.py",
    "ui_template.py",
    "inventory_socache.json",
    "test_verification.py",
    "compare_inspect_links.py",
    "TEST_RESULTS.txt",
    "RECHERCHE_ET_TESTS_INJECTION_CS2.md",
    "native/CMakeLists.txt",
    "native/offsets.hpp",
    "native/injector.cpp",
    "native/dllmain.cpp",
    "native/mesa_injector.exe",
    "native/mesa_bridge.dll",
]


def get_desktop_path() -> Path:
    buf = ctypes.create_unicode_buffer(260)
    CSIDL_DESKTOPDIRECTORY = 0x0010
    res = ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_DESKTOPDIRECTORY, 0, 0, buf)
    if res == 0 and buf.value:
        return Path(buf.value)
    for candidate in [
        Path.home() / "Desktop",
        Path.home() / "Bureau",
        Path.home() / "OneDrive" / "Desktop",
        Path.home() / "OneDrive" / "Bureau",
    ]:
        if candidate.exists():
            return candidate
    return Path.home() / "Desktop"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    desktop_dir = get_desktop_path()
    desktop_dir.mkdir(parents=True, exist_ok=True)
    zip_path = desktop_dir / "MESA-AUDIT.zip"

    missing = []
    for rel in FILES_TO_INCLUDE:
        if not (base_dir / rel).exists():
            missing.append(rel)

    if missing:
        print(f"[!] Fichiers absents : {', '.join(missing)}")

    total_uncompressed = 0
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel in FILES_TO_INCLUDE:
            src = base_dir / rel
            if src.exists():
                zf.write(src, arcname=rel)
                sz = src.stat().st_size
                total_uncompressed += sz
                print(f"[+] Inclus : {rel:<35} ({sz:>8} octets)")

    zip_sz = zip_path.stat().st_size
    print("-" * 60)
    print(f"[OK] MESA-AUDIT.zip généré sur : {zip_path}")
    print(f"[OK] Fichiers archivés : {len(FILES_TO_INCLUDE) - len(missing)}/{len(FILES_TO_INCLUDE)}")
    print(f"[OK] Taille totale décompressée : {total_uncompressed} octets")
    print(f"[OK] Taille archive ZIP         : {zip_sz} octets")


if __name__ == "__main__":
    main()

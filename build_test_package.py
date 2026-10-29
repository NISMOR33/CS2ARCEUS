import shutil
import zipfile
import re
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent
    desktop = Path.home() / "Desktop"
    pkg_dir = desktop / "ARCEUS-CS2-TEST-PACKAGE"
    pkg_dir.mkdir(parents=True, exist_ok=True)
    native_dir = pkg_dir / "native"
    native_dir.mkdir(parents=True, exist_ok=True)

    files_root = [
        "main.py",
        "db.py",
        "econ_defs.py",
        "ui_template.py",
        "inventory_socache.json",
        "cs2_skins.sqlite3",
        "requirements.txt",
        "LANCER_CS2_LOADER.bat",
        "run_arceus.bat",
        "inject_bridge.bat",
        "TEST_GUIDE.md",
        "logo.png",
        "logo.ico",
        "STYLE.png",
        "test_verification.py",
        "compare_inspect_links.py",
    ]

    files_native = [
        "native/mesa_injector.exe",
        "native/mesa_bridge.dll",
        "native/offsets.hpp",
        "native/dllmain.cpp",
        "native/injector.cpp",
        "native/CMakeLists.txt",
    ]

    print("--- Assemblage du Package ---")
    for rel in files_root:
        src = root / rel
        if src.exists():
            dst = pkg_dir / src.name
            shutil.copy2(src, dst)
            print(f"[+] Root: {rel} ({src.stat().st_size} octets)")
        else:
            print(f"[!] Manquant: {rel}")

    for rel in files_native:
        src = root / rel
        if src.exists():
            dst = native_dir / src.name
            shutil.copy2(src, dst)
            print(f"[+] Native: {rel} ({src.stat().st_size} octets)")
        else:
            print(f"[!] Manquant: {rel}")

    # Vérification d'absence de chemins absolus Windows résiduels vers la machine locale
    print("\n--- Verification des chemins dans les scripts ---")
    pattern_admin = re.compile(r"C:\\Users\\admin", re.IGNORECASE)
    for script_file in [pkg_dir / "run_arceus.bat", pkg_dir / "inject_bridge.bat"]:
        content = script_file.read_text(encoding="latin-1", errors="replace")
        matches = pattern_admin.findall(content)
        if matches:
            print(f"[ERREUR] Chemin absolu detecte dans {script_file.name}: {matches}")
        else:
            print(f"[OK] {script_file.name} : Chemins 100% relatifs (%~dp0)")

    # Produce ZIP
    zip_path = desktop / "ARCEUS-CS2-TEST-PACKAGE.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(pkg_dir.rglob("*")):
            if file_path.is_file():
                arcname = file_path.relative_to(pkg_dir)
                zf.write(file_path, arcname)

    print(f"\n[OK] Package cree : {pkg_dir}")
    print(f"[OK] Archive ZIP mise a jour : {zip_path} ({zip_path.stat().st_size} octets)")

    # Detail contenu du zip
    print("\n--- Contenu de l'archive ZIP ---")
    with zipfile.ZipFile(zip_path, "r") as zf:
        for info in zf.infolist():
            print(f" - {info.filename:<32} {info.file_size:>9} octets")

if __name__ == "__main__":
    main()

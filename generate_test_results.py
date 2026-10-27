import subprocess
from pathlib import Path

def main():
    out_file = Path("TEST_RESULTS.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("==============================================================================\n")
        f.write("RAPPORT DES TESTS TECHNIQUES LOCAUX - ARCEUS / MESA.CS2\n")
        f.write("==============================================================================\n\n")
        f.write("=== 1. SUITE DE VÉRIFICATION TECHNIQUE (test_verification.py) ===\n")
        res1 = subprocess.run(["python", "test_verification.py"], capture_output=True, text=True, errors="replace")
        f.write((res1.stdout or "") + "\n" + (res1.stderr or ""))
        f.write("\n=== 2. COMPARAISON INDÉPENDANTE INSPECT CSFLOAT (compare_inspect_links.py) ===\n")
        res2 = subprocess.run(["python", "compare_inspect_links.py"], capture_output=True, text=True, errors="replace")
        f.write((res2.stdout or "") + "\n" + (res2.stderr or ""))
    print(f"[+] {out_file} généré avec succès ({out_file.stat().st_size} octets)")

if __name__ == "__main__":
    main()

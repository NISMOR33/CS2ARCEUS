import ctypes
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
import os
from pathlib import Path
import shutil
import subprocess
import threading
import time
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlparse
import webbrowser

from db import SkinDatabase
from econ_defs import AppliedSticker, RARITY_MAP, WEAPON_DEF_INDEX, build_cs2_inspect_url
from ui_template import MESA_HTML

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("cs2_skin_loader")

MENU_WIDTH = 960
MENU_HEIGHT = 610
WINDOW_TITLE = "ARCEUS // CS2 PREMIUM CHEAT"
STICKER_ALLOWED_CATEGORIES = {"Fusils", "Pistolets", "PM", "Lourde"}


def _read_bridge_status_file(status_file: Path) -> Optional[Dict[str, Any]]:
    if not status_file.exists():
        return None
    try:
        return json.loads(status_file.read_text(encoding="utf-8"))
    except Exception:
        return None


def try_sync_native_bridge(base_dir: Path, verify_item_id: Optional[int] = None) -> Dict[str, Any]:
    candidates = [
        base_dir / "native" / "mesa_injector.exe",
        base_dir / "native" / "build" / "Release" / "mesa_injector.exe",
    ]
    dll_candidates = [
        base_dir / "native" / "mesa_bridge.dll",
        base_dir / "native" / "build" / "Release" / "mesa_bridge.dll",
    ]
    injector_bin = next((p for p in candidates if p.exists()), None)
    dll_bin = next((p for p in dll_candidates if p.exists()), None)
    status_file = base_dir / "mesa_bridge_status.json"

    steps = {
        "dll_loaded": False,
        "json_read": False,
        "item_added": False,
        "item_equipped": False,
    }

    if not injector_bin or not dll_bin:
        return {
            "synced": False,
            "reason": "DLL C++ non compilée (native/mesa_bridge.dll absent)",
            "steps": steps,
            "bridge_status": None,
        }

    try:
        res = subprocess.run(
            [str(injector_bin), str(dll_bin)],
            capture_output=True,
            text=True,
            timeout=6,
        )

        if res.returncode == 2:
            return {
                "synced": False,
                "reason": "cs2.exe n'est pas lancé",
                "steps": steps,
                "bridge_status": None,
            }

        if res.returncode != 0:
            err_msg = (res.stderr or res.stdout or "Échec injection").strip()
            return {
                "synced": False,
                "reason": err_msg,
                "steps": steps,
                "bridge_status": _read_bridge_status_file(status_file),
            }

        # L'injecteur a confirmé que mesa_bridge.dll est chargée dans cs2.exe.
        steps["dll_loaded"] = True
        bridge_status = _read_bridge_status_file(status_file)

        # Si un item_id précis est demandé, on attend jusqu'à 650 ms que le worker C++
        # (cycle 60 * 8 ms = 480 ms) lise inventory_socache.json et publie l'état de cet item.
        if verify_item_id is not None:
            item_key = str(verify_item_id)
            for _ in range(13):
                bridge_status = _read_bridge_status_file(status_file)
                if bridge_status and isinstance(bridge_status.get("items"), dict):
                    item_state = bridge_status["items"].get(item_key)
                    if isinstance(item_state, dict) and item_state.get("json_read"):
                        steps["json_read"] = bool(item_state.get("json_read", False))
                        steps["item_added"] = bool(item_state.get("item_added", False))
                        steps["item_equipped"] = bool(item_state.get("item_equipped", False))
                        break
                time.sleep(0.05)

        fully_verified = (
            all(steps.values())
            if verify_item_id is not None
            else bool(steps["dll_loaded"] and bridge_status and bridge_status.get("active"))
        )

        if verify_item_id is not None:
            reason = (
                f"DLL={int(steps['dll_loaded'])} | "
                f"JSON={int(steps['json_read'])} | "
                f"AddEconItem={int(steps['item_added'])} | "
                f"Equip={int(steps['item_equipped'])}"
            )
        else:
            reason = "DLL chargée dans cs2.exe" if steps["dll_loaded"] else "Non connecté"

        return {
            "synced": fully_verified,
            "reason": reason,
            "steps": steps,
            "bridge_status": bridge_status,
        }
    except Exception as exc:
        logger.debug("Bridge natif non injecté: %s", exc)
        return {
            "synced": False,
            "reason": str(exc),
            "steps": steps,
            "bridge_status": None,
        }


def parse_applied_stickers(raw_list: List[Dict[str, Any]]) -> List[AppliedSticker]:
    out: List[AppliedSticker] = []
    for item in raw_list[:5]:
        st_id = int(item.get("sticker_id") or item.get("def_index") or 0)
        if st_id <= 0:
            continue
        out.append(
            AppliedSticker(
                slot=int(item.get("slot", len(out))),
                sticker_id=st_id,
                name=str(item.get("name", "")),
                image_url=str(item.get("image_url", "")),
                wear=float(item.get("wear", 0.0)),
                scale=float(item.get("scale", 1.0)),
                rotation=float(item.get("rotation", 0.0)),
                offset_x=float(item.get("offset_x", 0.0)),
                offset_y=float(item.get("offset_y", 0.0)),
            )
        )
    return out


class MesaRequestHandler(BaseHTTPRequestHandler):
    db: SkinDatabase
    base_dir: Path

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _send_json(self, payload: Dict[str, Any], status: int = 200) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _read_body_json(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            raw = MESA_HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return

        if parsed.path in ("/assets/logo.png", "/assets/style.png"):
            img_name = "logo.png" if parsed.path == "/assets/logo.png" else "STYLE.png"
            img_path = self.base_dir / img_name
            if not img_path.exists():
                img_path = self.base_dir / "logo.png"
            if img_path.exists():
                raw = img_path.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
                return

        if parsed.path == "/api/nav":
            self._send_json(self.db.get_navigation_metadata())
            return

        if parsed.path == "/api/status":
            self._send_json(try_sync_native_bridge(self.base_dir))
            return

        if parsed.path == "/api/categories":
            meta = self.db.get_navigation_metadata()
            self._send_json({"categories": [c["name"] for c in meta["categories"]]})
            return

        if parsed.path == "/api/catalog":
            qs = parse_qs(parsed.query)
            q = qs.get("q", [""])[0]
            cat = qs.get("category", ["Toutes"])[0]
            weapon = qs.get("weapon", ["Toutes"])[0]
            rarity = int(qs.get("rarity", ["0"])[0] or 0)
            only_st = qs.get("st", ["0"])[0] == "1"
            sort_by = qs.get("sort", ["rarity_desc"])[0]

            items = self.db.search_catalog(
                query=q,
                category=cat,
                weapon_name=weapon,
                rarity_rank=rarity,
                only_stattrak=only_st,
                sort_by=sort_by,
            )
            self._send_json({"total": len(items), "items": items})
            return

        if parsed.path == "/api/stickers":
            qs = parse_qs(parsed.query)
            q = qs.get("q", [""])[0]
            items = self.db.search_stickers(query=q, limit=120)
            self._send_json({"items": items})
            return

        if parsed.path == "/api/inventory":
            inv = [asdict(x) for x in self.db.list_inventory()]
            self._send_json({"items": inv})
            return

        self._send_json({"error": "Not found"}, status=404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        body = self._read_body_json()

        if parsed.path == "/api/import":
            skin_id = str(body.get("skin_id", ""))
            entry = self.db.get_skin_by_id(skin_id)
            if not entry:
                self._send_json({"error": "Skin introuvable"}, status=404)
                return

            allowed_stickers = (
                list(body.get("stickers", []))[:5]
                if entry.category_name in STICKER_ALLOWED_CATEGORIES
                else []
            )

            econ_item = self.db.import_econ_item(
                entry=entry,
                paint_wear=float(body.get("paint_wear", 0.001)),
                paint_seed=int(body.get("paint_seed", 661)),
                stattrak_count=int(body.get("stattrak_count", -1)),
                custom_name=str(body.get("custom_name", "")),
                equip_t=bool(body.get("equip_t", True)),
                equip_ct=bool(body.get("equip_ct", True)),
                stickers_raw=allowed_stickers,
            )
            bridge_info = try_sync_native_bridge(self.base_dir, verify_item_id=econ_item.item_id)
            self._send_json(
                {
                    "ok": True,
                    "item_id": econ_item.item_id,
                    "steps": bridge_info["steps"],
                    "bridge_synced": bool(bridge_info["synced"]),
                    "bridge_reason": str(bridge_info["reason"]),
                    "bridge_status": bridge_info["bridge_status"],
                    "socache_object": econ_item.to_socache_dict(),
                }
            )
            return

        if parsed.path == "/api/inspect":
            skin_id = str(body.get("skin_id", ""))
            entry = self.db.get_skin_by_id(skin_id)
            if not entry:
                self._send_json({"error": "Skin introuvable"}, status=404)
                return

            def_index = WEAPON_DEF_INDEX.get(entry.weapon_id, 7)
            is_knife = "knife" in entry.weapon_id or "bayonet" in entry.weapon_id or "gloves" in entry.weapon_id
            st_count = int(body.get("stattrak_count", -1))
            quality = 3 if is_knife else (9 if st_count >= 0 else 4)
            rarity = RARITY_MAP.get(entry.rarity_id, 4)
            raw_stickers = (
                list(body.get("stickers", []))[:5]
                if entry.category_name in STICKER_ALLOWED_CATEGORIES
                else []
            )
            applied_stickers = parse_applied_stickers(raw_stickers)

            url = build_cs2_inspect_url(
                def_index=def_index,
                paint_index=entry.paint_index,
                paint_seed=int(body.get("paint_seed", 661)),
                paint_wear=float(body.get("paint_wear", 0.001)),
                rarity=rarity,
                quality=quality,
                stattrak_count=st_count,
                custom_name=str(body.get("custom_name", "")),
                stickers=applied_stickers,
            )
            webbrowser.open(url)
            self._send_json({"ok": True, "inspect_url": url})
            return

        if parsed.path == "/api/delete":
            item_id = int(body.get("item_id", 0))
            self.db.delete_inventory_item(item_id)
            self._send_json({"ok": True})
            return

        if parsed.path == "/api/sync":
            count = self.db.sync_catalog_from_api()
            self._send_json({"ok": True, "count": count})
            return

        self._send_json({"error": "Not found"}, status=404)


def _lock_win32_window_geometry() -> None:
    if os.name != "nt":
        return
    user32 = ctypes.windll.user32
    GWL_STYLE = -16
    WS_THICKFRAME = 0x00040000
    WS_MAXIMIZEBOX = 0x00010000
    SWP_NOMOVE = 0x0002
    SWP_NOZORDER = 0x0004
    SWP_FRAMECHANGED = 0x0020

    for _ in range(40):
        hwnd = user32.FindWindowW(None, WINDOW_TITLE)
        if hwnd:
            style = user32.GetWindowLongW(hwnd, GWL_STYLE)
            new_style = style & ~WS_THICKFRAME & ~WS_MAXIMIZEBOX
            user32.SetWindowLongW(hwnd, GWL_STYLE, new_style)
            user32.SetWindowPos(
                hwnd,
                0,
                0,
                0,
                MENU_WIDTH,
                MENU_HEIGHT,
                SWP_NOMOVE | SWP_NOZORDER | SWP_FRAMECHANGED,
            )
            logger.info("Fenêtre verrouillée à %dx%d (non-redimensionnable)", MENU_WIDTH, MENU_HEIGHT)
            return
        time.sleep(0.15)


def launch_desktop_window(url: str, base_dir: Path) -> None:
    edge_candidates = [
        shutil.which("msedge"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    profile_dir = base_dir / ".mesa_ui_profile"
    for candidate in edge_candidates:
        if candidate and Path(candidate).exists():
            subprocess.Popen(
                [
                    candidate,
                    f"--app={url}",
                    f"--user-data-dir={profile_dir}",
                    f"--window-size={MENU_WIDTH},{MENU_HEIGHT}",
                    "--disable-extensions",
                ]
            )
            threading.Thread(target=_lock_win32_window_geometry, daemon=True).start()
            return
    webbrowser.open(url)


def main() -> None:
    base_dir = Path(os.environ.get("CS2_LOADER_DIR", Path(__file__).resolve().parent))
    db_path = base_dir / "cs2_skins.sqlite3"
    socache_path = base_dir / "inventory_socache.json"
    database = SkinDatabase(db_path=db_path, socache_path=socache_path)

    if database.needs_full_sync():
        database.sync_catalog_from_api()

    MesaRequestHandler.db = database
    MesaRequestHandler.base_dir = base_dir
    try_sync_native_bridge(base_dir)

    port = int(os.environ.get("MESA_PORT", "17300"))
    server = ThreadingHTTPServer(("127.0.0.1", port), MesaRequestHandler)
    app_url = f"http://127.0.0.1:{port}"
    logger.info("Interface ARCEUS // CS2 PREMIUM CHEAT active sur %s", app_url)
    launch_desktop_window(app_url, base_dir)
    server.serve_forever()


if __name__ == "__main__":
    main()

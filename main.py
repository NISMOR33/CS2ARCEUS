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

from license_manager import GLOBAL_LICENSE_MGR, get_machine_hwid
from db import SkinDatabase
from econ_defs import AppliedSticker, RARITY_MAP, WEAPON_DEF_INDEX, build_cs2_inspect_url
from ui_template import MESA_HTML

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("cs2_skin_loader")

# ═══════════════════════════════════════════════════════════════
# ARCEUS LICENSE EXPIRATION WATCHDOG & EMERGENCY GAME TERMINATOR
# ═══════════════════════════════════════════════════════════════
ACTIVE_SESSION = {
    "key": None,
    "token": None,
    "pseudo": None,
    "expires_at": None,
    "is_lifetime": False,
    "armed": False
}

def trigger_emergency_kill(reason: str = "EXPIRED") -> None:
    logger.critical("[SECURITY] EXPIRATION DE LICENCE OU VIOLATION DE SESSION : %s", reason)
    try:
        # 1. Fermeture immédiate et forcée du processus Counter-Strike 2
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/IM", "cs2.exe"], capture_output=True, timeout=3, creationflags=0x08000000)
            subprocess.run(["taskkill", "/F", "/IM", "ARCEUS.exe"], capture_output=True, timeout=3, creationflags=0x08000000)
    except Exception as exc:
        logger.error("[SECURITY] Erreur kill processus: %s", exc)
    finally:
        logger.critical("[SECURITY] ARCEUS LOADER CLOSING NOW.")
        time.sleep(0.5)
        os._exit(0)

def _watchdog_loop():
    last_hb_check = 0.0
    while True:
        time.sleep(2)
        if not ACTIVE_SESSION["armed"]:
            continue
        exp = ACTIVE_SESSION["expires_at"]
        if exp and not ACTIVE_SESSION["is_lifetime"] and time.time() >= exp:
            trigger_emergency_kill("TEMPS DE LICENCE ÉCOULÉ (0s RESTANTE)")
            break
        # Contrôle distant en temps réel du ban / heartbeat toutes les 12 secondes
        now = time.time()
        if now - last_hb_check >= 12:
            last_hb_check = now
            k = ACTIVE_SESSION.get("key")
            tok = ACTIVE_SESSION.get("token")
            if k and tok:
                res = GLOBAL_LICENSE_MGR.heartbeat(k, tok)
                if not res.get("ok"):
                    status = res.get("status") or res.get("reason") or "REVOKED"
                    err = res.get("error") or "Licence bannie ou session fermée à distance"
                    trigger_emergency_kill(f"ORDRE SERVEUR [{status}] : {err}")
                    break

threading.Thread(target=_watchdog_loop, daemon=True, name="ArceusLicenseWatchdog").start()


if os.name == "nt":
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("CS2.SkinAndInventoryLoader.App.1.0")
    except Exception:
        pass

MENU_WIDTH = 960
MENU_HEIGHT = 610
WINDOW_TITLE = "CS2 // SKIN & INVENTORY LOADER"
STICKER_ALLOWED_CATEGORIES = {
    "Fusils", "Pistolets", "PM", "Lourde", "Armes",
    "Rifles", "Pistols", "SMGs", "Heavy", "Weapons",
    "rifles", "pistols", "smgs", "heavy"
}


def _read_bridge_status_file(status_file: Path) -> Optional[Dict[str, Any]]:
    if not status_file.exists():
        return None
    try:
        return json.loads(status_file.read_text(encoding="utf-8"))
    except Exception:
        return None


def try_sync_native_bridge(base_dir: Path, verify_item_id: Optional[int] = None) -> Dict[str, Any]:
    # Support both MESA native bridge and ARCEUS native engine
    candidates = [
        base_dir / "Lootline" / "x64" / "Release" / "ARCEUS.exe",
        base_dir / "native" / "mesa_injector.exe",
        base_dir / "native" / "build" / "Release" / "mesa_injector.exe",
    ]
    dll_candidates = [
        base_dir / "Lootline" / "x64" / "Release" / "Lootline.dll",
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
            creationflags=0x08000000 if os.name == "nt" else 0
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

        if parsed.path.startswith("/assets/"):
            asset_name = parsed.path.split("/assets/")[-1].split("?")[0]
            if asset_name.lower() == "style.png":
                asset_path = self.base_dir / "STYLE.png"
            else:
                asset_path = self.base_dir / asset_name
            if not asset_path.exists():
                asset_path = self.base_dir / "logo.png"
            if asset_path.exists() and asset_path.is_file():
                raw = asset_path.read_bytes()
                mime = "image/png"
                if asset_path.suffix.lower() in (".jpg", ".jpeg"):
                    mime = "image/jpeg"
                elif asset_path.suffix.lower() == ".svg":
                    mime = "image/svg+xml"
                elif asset_path.suffix.lower() == ".ico":
                    mime = "image/x-icon"
                elif asset_path.suffix.lower() == ".gif":
                    mime = "image/gif"
                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.send_header("Access-Control-Allow-Origin", "*")
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

        if parsed.path == "/api/auth/login":
            try:
                pseudo = str(body.get("pseudo", "")).strip() or "dj"
                key = str(body.get("key", "")).strip().upper()
                hwid = str(body.get("hwid", "")).strip() or get_machine_hwid()

                auth_res = GLOBAL_LICENSE_MGR.validate_login(key=key, pseudo=pseudo, hwid=hwid)
                if auth_res.get("ok"):
                    ACTIVE_SESSION["key"] = auth_res.get("key")
                    ACTIVE_SESSION["token"] = auth_res.get("session_token") or auth_res.get("token")
                    ACTIVE_SESSION["pseudo"] = auth_res.get("pseudo") or auth_res.get("bound_pseudo") or pseudo
                    ACTIVE_SESSION["expires_at"] = auth_res.get("expires_at")
                    ACTIVE_SESSION["is_lifetime"] = auth_res.get("is_lifetime", False)
                    ACTIVE_SESSION["armed"] = True
                    logger.info("[AUTH] Connexion réussie pour %s [Clé: %s, Plan: %s, Lifetime: %s]",
                                pseudo, key, auth_res.get("plan"), auth_res.get("is_lifetime"))
                    self._send_json(auth_res, status=200)
                else:
                    logger.warning("[AUTH] Rejet connexion pour %s [Clé: %s]: %s", pseudo, key, auth_res.get("error"))
                    self._send_json(auth_res, status=200)
            except Exception as e:
                logger.error("[AUTH] Erreur interne login: %s", e)
                self._send_json({"ok": False, "error": f"Erreur interne: {e}"}, status=200)
            return

        if parsed.path == "/api/auth/heartbeat":
            key = str(body.get("key", "")).strip().upper() or ACTIVE_SESSION.get("key", "")
            token = str(body.get("session_token", "")).strip() or ACTIVE_SESSION.get("token", "")
            hwid = str(body.get("hwid", "")).strip() or get_machine_hwid()

            if not key or not token:
                self._send_json({"ok": False, "error": "Paramètres manquants"}, status=400)
                return

            hb_res = GLOBAL_LICENSE_MGR.heartbeat(key=key, session_token=token, hwid=hwid)
            if not hb_res.get("ok"):
                reason = hb_res.get("reason", "unknown")
                if reason in ("expired", "session_replaced", "revoked"):
                    def _delayed_kill():
                        time.sleep(1.5)
                        trigger_emergency_kill(f"Heartbeat rejeté: {reason}")
                    threading.Thread(target=_delayed_kill, daemon=True).start()
            self._send_json(hb_res)
            return

        if parsed.path == "/api/auth/status":
            key = str(body.get("key", "")).strip().upper() or ACTIVE_SESSION.get("key", "")
            info = GLOBAL_LICENSE_MGR.get_license_info(key) if key else None
            if info:
                self._send_json({"ok": True, "info": info})
            else:
                self._send_json({"ok": False, "error": "Licence non trouvée"}, status=404)
            return

        if parsed.path == "/api/auth/expire-kill":
            logger.critical("[API] Fermeture forcée déclenchée par le frontend suite à expiration du timer.")
            def _async_kill():
                time.sleep(0.4)
                trigger_emergency_kill("TIMER FRONTEND À 0")
            threading.Thread(target=_async_kill, daemon=True).start()
            self._send_json({"ok": True, "action": "terminating"})
            return

        if parsed.path == "/api/license/create":
            plan = str(body.get("plan", "7jours"))
            email = str(body.get("email", ""))
            stripe_session = str(body.get("stripe_session_id", ""))
            lic = GLOBAL_LICENSE_MGR.create_license(plan=plan, email=email, stripe_session_id=stripe_session)
            self._send_json({"ok": True, "license": lic})
            return

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

        if parsed.path in ("/api/overlay/toggle", "/api/window/minimize"):
            is_visible = toggle_overlay_window()
            self._send_json({"ok": True, "visible": is_visible})
            return

        if parsed.path in ("/api/overlay/close", "/api/window/close"):
            self._send_json({"ok": True})
            def _instant_exit():
                try:
                    time.sleep(0.05)
                    if NATIVE_WINDOW:
                        NATIVE_WINDOW.destroy()
                except Exception:
                    pass
                finally:
                    os._exit(0)
            threading.Thread(target=_instant_exit, daemon=True).start()
            return

        if parsed.path == "/api/sync":
            count = self.db.sync_catalog_from_api()
            self._send_json({"ok": True, "count": count})
            return

        self._send_json({"error": "Not found"}, status=404)


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]


ARCEUS_WINDOW_HWND = 0
ARCEUS_BROWSER_PID = 0


def set_window_app_icon(hwnd: int, ico_path: Path) -> bool:
    if os.name != "nt" or not hwnd or not ico_path.exists():
        return False
    try:
        user32 = ctypes.windll.user32
        WM_SETICON = 0x0080
        ICON_SMALL = 0
        ICON_BIG = 1
        IMAGE_ICON = 1
        LR_LOADFROMFILE = 0x00000010

        hicon_big = user32.LoadImageW(0, str(ico_path), IMAGE_ICON, 32, 32, LR_LOADFROMFILE)
        hicon_small = user32.LoadImageW(0, str(ico_path), IMAGE_ICON, 16, 16, LR_LOADFROMFILE)

        if hicon_big:
            user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon_big)
            try:
                ctypes.windll.user32.SetClassLongPtrW(hwnd, -14, hicon_big)
            except Exception:
                pass
        if hicon_small:
            user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon_small)
            try:
                ctypes.windll.user32.SetClassLongPtrW(hwnd, -34, hicon_small)
            except Exception:
                pass
        logger.info("[ICON] Icone appliquee sur HWND=%d (ico=%s)", hwnd, ico_path.name)
        return True
    except Exception as exc:
        logger.warning("[ICON] Erreur application icone: %s", exc)
        return False


def _apply_icon_when_ready(ico_path: Path) -> None:
    for _ in range(60):
        time.sleep(0.1)
        h = _find_arceus_window()
        if h:
            set_window_app_icon(h, ico_path)
            break


def _find_arceus_window():
    global ARCEUS_WINDOW_HWND
    if os.name != "nt":
        return 0
    user32 = ctypes.windll.user32

    if ARCEUS_WINDOW_HWND and user32.IsWindow(ARCEUS_WINDOW_HWND):
        return ARCEUS_WINDOW_HWND

    # 1. Direct O(1) title lookups
    candidates = [
        WINDOW_TITLE,
        "CS2 // SKIN & INVENTORY LOADER",
        "CS2 // SKIN & INVENTORY LOADER - Google Chrome",
        "CS2 // SKIN & INVENTORY LOADER - Microsoft Edge",
        "ARCEUS // CS2 PREMIUM CHEAT",
        "ARCEUS",
    ]
    for title in candidates:
        h = user32.FindWindowW(None, title)
        if h and user32.IsWindow(h):
            ARCEUS_WINDOW_HWND = h
            logger.info("[OVERLAY] Fenetre detectee par titre: %s (HWND=%d)", title, h)
            return h

    # 2. Iteration via FindWindowExW (sans callback ctypes)
    h = user32.FindWindowExW(0, 0, None, None)
    while h:
        length = user32.GetWindowTextLengthW(h)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(h, buff, length + 1)
            val = buff.value.upper()
            if "SKIN & INVENTORY LOADER" in val or "ARCEUS" in val or "CS2 PREMIUM CHEAT" in val:
                ARCEUS_WINDOW_HWND = h
                logger.info("[OVERLAY] Fenetre detectee par scan: '%s' (HWND=%d)", buff.value, h)
                return h
        h = user32.FindWindowExW(0, h, None, None)

    return 0


import webview

NATIVE_WINDOW = None
IS_OVERLAY_VISIBLE = True


def toggle_overlay_window() -> bool:
    global NATIVE_WINDOW, IS_OVERLAY_VISIBLE
    if NATIVE_WINDOW is None:
        return False
    try:
        if IS_OVERLAY_VISIBLE:
            NATIVE_WINDOW.hide()
            IS_OVERLAY_VISIBLE = False
            if os.name == "nt":
                cs2_hwnd = ctypes.windll.user32.FindWindowW(None, "Counter-Strike 2")
                if cs2_hwnd:
                    ctypes.windll.user32.SetForegroundWindow(cs2_hwnd)
            logger.info("[OVERLAY] Fenetre native masquee -> Focus CS2")
            return False
        else:
            NATIVE_WINDOW.show()
            IS_OVERLAY_VISIBLE = True
            if os.name == "nt":
                hwnd = ctypes.windll.user32.FindWindowW(None, WINDOW_TITLE) or ctypes.windll.user32.FindWindowW(None, "ARCEUS // CS2 PREMIUM CHEAT")
                if hwnd:
                    HWND_TOPMOST = -1
                    SWP_NOMOVE = 0x0002
                    SWP_NOSIZE = 0x0001
                    SWP_SHOWWINDOW = 0x0040
                    ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
                    ctypes.windll.user32.SetForegroundWindow(hwnd)
            logger.info("[OVERLAY] Fenetre native affichee au premier plan")
            return True
    except Exception as exc:
        logger.warning("[OVERLAY] Erreur bascule: %s", exc)
        return False


def _listen_for_insert_hotkey() -> None:
    if os.name != "nt":
        return
    user32 = ctypes.windll.user32
    VK_INSERT = 0x2D
    VK_HOME = 0x24
    VK_F6 = 0x75

    was_down = False
    logger.info("[OVERLAY] Ecoute globale activee sur touches : INSERT / HOME / F6")

    while True:
        try:
            down_insert = bool(user32.GetAsyncKeyState(VK_INSERT) & 0x8000)
            down_home = bool(user32.GetAsyncKeyState(VK_HOME) & 0x8000)
            down_f6 = bool(user32.GetAsyncKeyState(VK_F6) & 0x8000)
            is_down = down_insert or down_home or down_f6

            if is_down and not was_down:
                key_name = "INSERT" if down_insert else ("HOME" if down_home else "F6")
                logger.info("[OVERLAY] Touche %s pressee -> Bascule de l'interface", key_name)
                toggle_overlay_window()
                time.sleep(0.3)

            was_down = is_down
            time.sleep(0.025)
        except Exception:
            time.sleep(0.1)


def main() -> None:
    global NATIVE_WINDOW, IS_OVERLAY_VISIBLE
    if getattr(sys, "frozen", False):
        base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        exe_dir = Path(sys.executable).resolve().parent
        db_path = base_dir / "cs2_skins.sqlite3"
        socache_path = exe_dir / "inventory_socache.json"
        if not socache_path.exists() and (base_dir / "inventory_socache.json").exists():
            try:
                shutil.copy2(base_dir / "inventory_socache.json", socache_path)
            except Exception:
                socache_path = base_dir / "inventory_socache.json"
    else:
        base_dir = Path(os.environ.get("CS2_LOADER_DIR", Path(__file__).resolve().parent))
        db_path = base_dir / "cs2_skins.sqlite3"
        socache_path = base_dir / "inventory_socache.json"
    database = SkinDatabase(db_path=db_path, socache_path=socache_path)

    MesaRequestHandler.db = database
    MesaRequestHandler.base_dir = base_dir

    def _bg_bootstrap():
        try:
            if database.needs_full_sync():
                database.sync_catalog_from_api()
        except Exception as e:
            logger.warning("[BOOT] Erreur sync catalogue bg: %s", e)
        try:
            try_sync_native_bridge(base_dir)
        except Exception as e:
            logger.warning("[BOOT] Erreur sync native bridge bg: %s", e)

    threading.Thread(target=_bg_bootstrap, daemon=True).start()

    port = int(os.environ.get("MESA_PORT", "17300"))
    server = ThreadingHTTPServer(("127.0.0.1", port), MesaRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    app_url = f"http://127.0.0.1:{port}"
    logger.info("Application native active sur %s", app_url)

    IS_OVERLAY_VISIBLE = True
    NATIVE_WINDOW = webview.create_window(
        title=WINDOW_TITLE,
        url=app_url,
        width=MENU_WIDTH,
        height=MENU_HEIGHT,
        resizable=False,
        frameless=True,
        easy_drag=False,
        background_color="#050505",
        text_select=False,
    )

    ico_candidate = base_dir / "logo.ico"
    threading.Thread(target=_apply_icon_when_ready, args=(ico_candidate,), daemon=True).start()
    threading.Thread(target=_listen_for_insert_hotkey, daemon=True).start()
    webview.start(debug=False)


if __name__ == "__main__":
    main()

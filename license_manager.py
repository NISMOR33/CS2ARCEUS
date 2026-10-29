# -*- coding: utf-8 -*-
"""
ARCEUS // CS2 KERNEL SKIN LOADER - ADVANCED LICENSING & HWID SECURITY ENGINE
=============================================================================
- Single-use concurrent session lock (1 machine at a time)
- Hardware ID (HWID) binding
- Timed expiration with automatic game / cheat termination
- Cryptographic key generation
- SQLite persistence
"""

import hashlib
import os
import secrets
import sqlite3
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def get_cloud_server_url() -> Optional[str]:
    env_url = os.environ.get("ARCEUS_SERVER_URL", "").strip()
    if env_url:
        return env_url.rstrip("/")
    candidates = []
    if getattr(sys, "frozen", False):
        candidates.append(Path(sys.executable).resolve().parent / "server.txt")
    candidates.append(Path(__file__).resolve().parent / "server.txt")
    for c in candidates:
        if c.exists():
            try:
                txt = c.read_text(encoding="utf-8").strip()
                if txt.startswith("http://") or txt.startswith("https://"):
                    return txt.rstrip("/")
            except Exception:
                pass
    return None

def resolve_db_path() -> Path:
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        db_file = exe_dir / "licenses.db"
        if not db_file.exists():
            bundled = Path(getattr(sys, "_MEIPASS", "")) / "licenses.db"
            if bundled.exists():
                try:
                    import shutil
                    shutil.copy2(bundled, db_file)
                except Exception:
                    pass
        return db_file
    return Path(__file__).resolve().parent / "licenses.db"

DB_PATH = resolve_db_path()


# ═══════════════════════════════════════════════════════════════
# ARCEUS // SUPABASE CLOUD REST ENGINE (24/7 ONLINE SYNC)
# ═══════════════════════════════════════════════════════════════
SUPABASE_URL = "https://hnhlymnmzmnafhrdtmfl.supabase.co"
SUPABASE_KEY = "sb_publishable_yFdTjfxRT5nuGL1SQnjVsw_lMsqVxdz"

def supabase_rest(endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None, timeout: float = 3.5) -> Optional[Any]:
    try:
        import urllib.request
        import json
        url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        body = json.dumps(data).encode("utf-8") if data is not None else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content) if content else {}
    except Exception as exc:
        return None

ARCEUS_MASTER_KEY_SECRET = "ARCEUS_CORE_2026_VANTA_SECURE"

PLAN_CODE_MAP = {
    "7J": "7jours",
    "7D": "7jours",
    "1M": "1mois",
    "1A": "1an",
    "1Y": "1an",
    "VIE": "vie",
    "LT": "vie",
}

def compute_key_checksum(plan_code: str, salt: str) -> str:
    """Calcule le hash cryptographique court HMAC/SHA256 pour sceller une clé."""
    raw = f"ARCEUS:{ARCEUS_MASTER_KEY_SECRET}:{plan_code.upper()}:{salt.upper()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:4].upper()

def generate_signed_license_key(plan_type: str) -> str:
    """Génère une clé cryptographique auto-validante format ARCEUS-<PLAN>-<SALT>-<SIG>."""
    clean = plan_type.lower().strip()
    rev_map = {
        "7jours": "7J", "semaine": "7J", "weekly": "7J",
        "1mois": "1M", "mois": "1M", "monthly": "1M",
        "1an": "1A", "an": "1A", "yearly": "1A",
        "vie": "VIE", "lifetime": "VIE"
    }
    p_code = rev_map.get(clean, "1M")
    alphabet = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
    salt = "".join(secrets.choice(alphabet) for _ in range(4))
    sig = compute_key_checksum(p_code, salt)
    return f"ARCEUS-{p_code}-{salt}-{sig}"

def verify_signed_key(key_str: str) -> Optional[Dict[str, Any]]:
    """Vérifie mathématiquement la signature d'une clé sans base de données préalable."""
    parts = key_str.strip().upper().split("-")
    if len(parts) != 4 or parts[0] != "ARCEUS":
        return None
    p_code, salt, sig = parts[1], parts[2], parts[3]
    if p_code not in PLAN_CODE_MAP:
        return None
    expected_sig = compute_key_checksum(p_code, salt)
    if sig != expected_sig:
        return None
    plan = PLAN_CODE_MAP[p_code]
    return {
        "valid": True,
        "plan": plan,
        "plan_code": p_code,
        "duration_seconds": DURATIONS.get(plan, 30 * 86400)
    }

# Plan durations in seconds
DURATIONS = {
    "semaine": 7 * 86400,        # 7 jours = 604 800s
    "7jours": 7 * 86400,
    "weekly": 7 * 86400,
    "mois": 30 * 86400,          # 30 jours = 2 592 000s
    "1mois": 30 * 86400,
    "monthly": 30 * 86400,
    "an": 365 * 86400,           # 365 jours = 31 536 000s
    "1an": 365 * 86400,
    "yearly": 365 * 86400,
    "vie": -1,                   # À vie / Permanent
    "lifetime": -1
}

PLAN_DISPLAY_NAMES = {
    "semaine": "LICENCE 7 JOURS",
    "7jours": "LICENCE 7 JOURS",
    "weekly": "LICENCE 7 JOURS",
    "mois": "LICENCE 1 MOIS",
    "1mois": "LICENCE 1 MOIS",
    "monthly": "LICENCE 1 MOIS",
    "an": "LICENCE 1 AN",
    "1an": "LICENCE 1 AN",
    "yearly": "LICENCE 1 AN",
    "vie": "LICENCE À VIE (PERMANENT)",
    "lifetime": "LICENCE À VIE (PERMANENT)"
}


def get_machine_hwid() -> str:
    """Generate a stable, unique cryptographic hardware fingerprint for this machine."""
    components = []
    
    # 1. Windows MachineGuid from registry
    if os.name == "nt":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography", 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            guid, _ = winreg.QueryValueEx(key, "MachineGuid")
            winreg.CloseKey(key)
            if guid:
                components.append(str(guid).strip())
        except Exception:
            pass

        # 2. Motherboard / BIOS UUID via WMIC or PowerShell
        try:
            res = subprocess.run(
                ["wmic", "csproduct", "get", "uuid"],
                capture_output=True,
                text=True,
                timeout=2,
                creationflags=0x08000000 if os.name == "nt" else 0
            )
            out = res.stdout.replace("UUID", "").strip()
            if out:
                components.append(out)
        except Exception:
            pass

    # 3. Fallback: username + processor + mac address
    try:
        import uuid
        mac = str(uuid.getnode())
        components.append(mac)
    except Exception:
        pass

    components.append(os.environ.get("COMPUTERNAME", "UNKNOWN_HOST"))
    raw_sig = "|".join(components)
    return hashlib.sha256(raw_sig.encode("utf-8")).hexdigest()[:32].upper()


class LicenseManager:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._lock = threading.Lock()
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=15)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._lock, self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS licenses (
                    key TEXT PRIMARY KEY,
                    plan TEXT NOT NULL,
                    duration_seconds INTEGER NOT NULL,
                    created_at REAL NOT NULL,
                    expires_at REAL,
                    bound_pseudo TEXT,
                    active_hwid TEXT,
                    active_session_token TEXT,
                    last_heartbeat REAL,
                    is_revoked INTEGER DEFAULT 0,
                    order_email TEXT,
                    stripe_session_id TEXT
                )
            """)
            conn.commit()

    @staticmethod
    def generate_key_string() -> str:
        """Génère une clé cryptographique sécurisée format ARCEUS-XXXX-XXXX-XXXX."""
        alphabet = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"  # Évite 0/O, 1/I
        part1 = "".join(secrets.choice(alphabet) for _ in range(4))
        part2 = "".join(secrets.choice(alphabet) for _ in range(4))
        part3 = "".join(secrets.choice(alphabet) for _ in range(4))
        return f"ARCEUS-{part1}-{part2}-{part3}"

    def create_license(
        self,
        plan: str,
        email: str = "",
        stripe_session_id: str = "",
        custom_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Crée et enregistre une nouvelle licence suite à un achat."""
        plan_clean = plan.lower().strip()
        dur_sec = DURATIONS.get(plan_clean, 30 * 86400)
        now = time.time()
        expires_at = (now + dur_sec) if dur_sec > 0 else None
        key = (custom_key or self.generate_key_string()).strip().upper()

        with self._lock, self._get_conn() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO licenses (
                    key, plan, duration_seconds, created_at, expires_at,
                    bound_pseudo, active_hwid, active_session_token, last_heartbeat,
                    is_revoked, order_email, stripe_session_id
                ) VALUES (?, ?, ?, ?, ?, NULL, NULL, NULL, NULL, 0, ?, ?)
            """, (key, plan_clean, dur_sec, now, expires_at, email, stripe_session_id))
            conn.commit()

        return {
            "key": key,
            "plan": plan_clean,
            "plan_name": PLAN_DISPLAY_NAMES.get(plan_clean, plan_clean.upper()),
            "created_at": now,
            "expires_at": expires_at,
            "is_lifetime": (dur_sec == -1)
        }

    def validate_login(
        self,
        key: str,
        pseudo: str,
        hwid: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Valide une tentative de connexion au launcher :
        - Clé existante ?
        - Clé révoquée ?
        - Clé expirée ?
        - Clé déjà utilisée en même temps sur un autre PC (Single concurrent user lock) ?
        """
        key_clean = key.strip().upper()
        current_hwid = (hwid or get_machine_hwid()).strip()
        now = time.time()

        # ─── VÉRIFICATION SUPABASE CLOUD (24/7 EN LIGNE) ───
        sb_rows = supabase_rest(f"licenses?key=eq.{key_clean}&select=*")
        if isinstance(sb_rows, list) and len(sb_rows) > 0:
            row = sb_rows[0]
            if row.get("is_revoked"):
                return {"ok": False, "error": "CETTE LICENCE A ÉTÉ BANIE / RÉVOQUÉE", "code": "KEY_REVOKED"}
            exp = row.get("expires_at")
            is_life = (row.get("duration_seconds") == -1)
            if not is_life and exp and now >= exp:
                return {"ok": False, "error": "LICENCE EXPIRÉE // RENOUVELLEMENT REQUIS", "code": "KEY_EXPIRED"}
            # Verrouillage concurrent
            last_hb = row.get("last_heartbeat") or 0
            act_hwid = row.get("active_hwid") or ""
            if act_hwid and act_hwid != current_hwid and (now - last_hb < 45):
                return {
                    "ok": False,
                    "error": "CETTE CLÉ EST DÉJÀ EN COURS D'UTILISATION SUR UN AUTRE ORDINATEUR",
                    "code": "CONCURRENT_SESSION_LOCKED"
                }
            session_tok = f"SESS_{secrets.token_hex(16).upper()}"
            supabase_rest(f"licenses?key=eq.{key_clean}", method="PATCH", data={
                "bound_pseudo": row.get("bound_pseudo") or pseudo or "player",
                "active_hwid": current_hwid,
                "active_session_token": session_tok,
                "last_heartbeat": now
            })
            rem = max(0, int(exp - now)) if (exp and not is_life) else -1
            return {
                "ok": True,
                "key": key_clean,
                "token": session_tok,
                "session_token": session_tok,
                "pseudo": row.get("bound_pseudo") or pseudo or "player",
                "bound_pseudo": row.get("bound_pseudo") or pseudo or "player",
                "plan": row.get("plan", "1mois"),
                "plan_name": PLAN_DISPLAY_NAMES.get(row.get("plan"), "LICENCE ACTIVE"),
                "is_lifetime": is_life,
                "expires_at": exp,
                "remaining_seconds": rem,
                "hwid": current_hwid
            }
        elif isinstance(sb_rows, list) and len(sb_rows) == 0:
            crypto_lic = verify_signed_key(key_clean)
            if crypto_lic and crypto_lic.get("valid"):
                p_type = crypto_lic["plan"]
                dur = crypto_lic["duration_seconds"]
                exp = (now + dur) if dur > 0 else None
                session_tok = f"SESS_{secrets.token_hex(16).upper()}"
                supabase_rest("licenses", method="POST", data={
                    "key": key_clean,
                    "plan": p_type,
                    "duration_seconds": dur,
                    "created_at": now,
                    "expires_at": exp,
                    "bound_pseudo": pseudo or "player",
                    "active_hwid": current_hwid,
                    "active_session_token": session_tok,
                    "last_heartbeat": now,
                    "is_revoked": False
                })
                rem = max(0, int(exp - now)) if (exp and dur > 0) else -1
                return {
                    "ok": True,
                    "key": key_clean,
                    "token": session_tok,
                    "session_token": session_tok,
                    "pseudo": pseudo or "player",
                    "bound_pseudo": pseudo or "player",
                    "plan": p_type,
                    "plan_name": PLAN_DISPLAY_NAMES.get(p_type, "LICENCE ACTIVE"),
                    "is_lifetime": (dur == -1),
                    "expires_at": exp,
                    "remaining_seconds": rem,
                    "hwid": current_hwid
                }

        with self._lock, self._get_conn() as conn:
            row = conn.execute("SELECT * FROM licenses WHERE key = ?", (key_clean,)).fetchone()
            if not row:
                # Vérification cryptographique de la signature de clé maître
                crypto_lic = verify_signed_key(key_clean)
                if crypto_lic and crypto_lic.get("valid"):
                    p_type = crypto_lic["plan"]
                    dur = crypto_lic["duration_seconds"]
                    exp = (now + dur) if dur > 0 else None
                    conn.execute("""
                        INSERT INTO licenses (
                            key, plan, duration_seconds, created_at, expires_at,
                            bound_pseudo, active_hwid, active_session_token, last_heartbeat,
                            is_revoked, order_email, stripe_session_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?, 0, ?, ?)
                    """, (
                        key_clean, p_type, dur, now, exp,
                        pseudo or "client", current_hwid, now,
                        "instant_stripe_buyer", "CRYPTO_SIGNED_KEY"
                    ))
                    conn.commit()
                    row = conn.execute("SELECT * FROM licenses WHERE key = ?", (key_clean,)).fetchone()
                else:
                    return {
                        "ok": False,
                        "error": "CLÉ INTROUVABLE // PAIEMENT REQUIS",
                        "code": "KEY_NOT_FOUND"
                    }

            if row["is_revoked"]:
                return {
                    "ok": False,
                    "error": "LICENCE SUSPENDUE PAR L'ADMINISTRATION",
                    "code": "KEY_REVOKED"
                }

            # 1. Vérification de l'expiration
            expires_at = row["expires_at"]
            is_lifetime = (row["duration_seconds"] == -1)

            if not is_lifetime and expires_at is not None:
                if now >= expires_at:
                    return {
                        "ok": False,
                        "error": "LICENCE EXPIRÉE // RENOUVELEZ VOTRE ACCÈS SUR LE SITE",
                        "code": "KEY_EXPIRED",
                        "expired_at": expires_at
                    }

            # 2. Verrouillage Concurrent (Une seule session en même temps)
            # Si un autre PC envoie un battement de coeur depuis moins de 50 secondes
            last_hb = row["last_heartbeat"] or 0
            active_hwid = row["active_hwid"] or ""
            active_token = row["active_session_token"] or ""

            if active_hwid and active_hwid != current_hwid and (now - last_hb < 50):
                return {
                    "ok": False,
                    "error": "CETTE CLÉ EST DÉJÀ ACTIVE SUR UN AUTRE ORDINATEUR",
                    "code": "SESSION_CONCURRENT_LOCKED",
                    "details": "Une seule machine peut utiliser cette licence simultanément."
                }

            # 3. Tout est valide : attribution de la session et verrouillage sur cet HWID
            session_token = f"ARCEUS_SESS_{secrets.token_hex(16).upper()}"
            bound_pseudo = row["bound_pseudo"] or pseudo or "dj"

            conn.execute("""
                UPDATE licenses SET
                    bound_pseudo = ?,
                    active_hwid = ?,
                    active_session_token = ?,
                    last_heartbeat = ?
                WHERE key = ?
            """, (bound_pseudo, current_hwid, session_token, now, key_clean))
            conn.commit()

            remaining_sec = max(0, int(expires_at - now)) if (expires_at and not is_lifetime) else -1

            return {
                "ok": True,
                "key": key_clean,
                "session_token": session_token,
                "pseudo": bound_pseudo,
                "plan": row["plan"],
                "plan_name": PLAN_DISPLAY_NAMES.get(row["plan"], row["plan"].upper()),
                "created_at": row["created_at"],
                "expires_at": expires_at,
                "remaining_seconds": remaining_sec,
                "is_lifetime": is_lifetime,
                "hwid": current_hwid
            }

    def heartbeat(
        self,
        key: str,
        session_token: str,
        hwid: Optional[str] = None
    ) -> Dict[str, Any]:
        """Met à jour le battement de coeur et vérifie si la licence est encore valide."""
        key_clean = key.strip().upper()
        current_hwid = (hwid or get_machine_hwid()).strip()
        now = time.time()

        # ─── SUPABASE CLOUD HEARTBEAT EN DIRECT ───
        sb_rows = supabase_rest(f"licenses?key=eq.{key_clean}&select=is_revoked,expires_at,duration_seconds,active_session_token")
        if isinstance(sb_rows, list) and len(sb_rows) > 0:
            row = sb_rows[0]
            if row.get("is_revoked"):
                return {"ok": False, "status": "REVOKED", "error": "LICENCE BANIE PAR L'ADMINISTRATION"}
            exp = row.get("expires_at")
            is_life = (row.get("duration_seconds") == -1)
            if not is_life and exp and now >= exp:
                return {"ok": False, "status": "EXPIRED", "error": "TEMPS ÉCOULÉ"}
            supabase_rest(f"licenses?key=eq.{key_clean}", method="PATCH", data={"last_heartbeat": now})
            rem = max(0, int(exp - now)) if (exp and not is_life) else -1
            return {"ok": True, "status": "ACTIVE", "remaining_seconds": rem}

        with self._lock, self._get_conn() as conn:
            row = conn.execute("SELECT * FROM licenses WHERE key = ?", (key_clean,)).fetchone()
            if not row:
                return {"ok": False, "reason": "key_deleted"}

            if row["is_revoked"]:
                return {"ok": False, "reason": "revoked"}

            # Vérifie si une autre session a pris la main
            if row["active_session_token"] != session_token:
                return {
                    "ok": False,
                    "reason": "session_replaced",
                    "error": "Session reprise par un autre utilisateur."
                }

            # Vérifie l'expiration
            expires_at = row["expires_at"]
            is_lifetime = (row["duration_seconds"] == -1)
            if not is_lifetime and expires_at is not None and now >= expires_at:
                return {
                    "ok": False,
                    "reason": "expired",
                    "error": "Licence expirée."
                }

            # Renouvelle le heartbeat
            conn.execute("UPDATE licenses SET last_heartbeat = ? WHERE key = ?", (now, key_clean))
            conn.commit()

            remaining_sec = max(0, int(expires_at - now)) if (expires_at and not is_lifetime) else -1
            return {
                "ok": True,
                "remaining_seconds": remaining_sec,
                "is_lifetime": is_lifetime
            }

    def logout(self, key: str, session_token: str) -> bool:
        """Libère la session active."""
        key_clean = key.strip().upper()
        with self._lock, self._get_conn() as conn:
            conn.execute("""
                UPDATE licenses SET
                    active_session_token = NULL,
                    last_heartbeat = NULL
                WHERE key = ? AND active_session_token = ?
            """, (key_clean, session_token))
            conn.commit()
            return True

    def get_license_info(self, key: str) -> Optional[Dict[str, Any]]:
        key_clean = key.strip().upper()
        with self._lock, self._get_conn() as conn:
            row = conn.execute("SELECT * FROM licenses WHERE key = ?", (key_clean,)).fetchone()
            if not row:
                return None
            now = time.time()
            exp = row["expires_at"]
            rem = max(0, int(exp - now)) if (exp and row["duration_seconds"] != -1) else -1
            return {
                "key": row["key"],
                "plan": row["plan"],
                "plan_name": PLAN_DISPLAY_NAMES.get(row["plan"], row["plan"].upper()),
                "created_at": row["created_at"],
                "expires_at": exp,
                "remaining_seconds": rem,
                "is_lifetime": (row["duration_seconds"] == -1),
                "bound_pseudo": row["bound_pseudo"],
                "is_active": bool(row["active_session_token"] and (now - (row["last_heartbeat"] or 0) < 50))
            }

    def list_all_licenses(self) -> List[Dict[str, Any]]:
        with self._lock, self._get_conn() as conn:
            rows = conn.execute("SELECT * FROM licenses ORDER BY created_at DESC").fetchall()
            now = time.time()
            res = []
            for r in rows:
                exp = r["expires_at"]
                rem = max(0, int(exp - now)) if (exp and r["duration_seconds"] != -1) else -1
                res.append({
                    "key": r["key"],
                    "plan": r["plan"],
                    "created_at": r["created_at"],
                    "expires_at": exp,
                    "remaining_seconds": rem,
                    "bound_pseudo": r["bound_pseudo"],
                    "is_lifetime": (r["duration_seconds"] == -1),
                    "is_active": bool(r["active_session_token"] and (now - (r["last_heartbeat"] or 0) < 50))
                })
            return res


# Instance globale
GLOBAL_LICENSE_MGR = LicenseManager()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ARCEUS License Management CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_create = sub.add_parser("create", help="Créer une nouvelle licence")
    p_create.add_argument("--plan", choices=["7j", "semaine", "1m", "mois", "1a", "an", "vie", "lifetime"], default="7j")
    p_create.add_argument("--email", default="")
    p_create.add_argument("--key", default=None, help="Clé personnalisée optionnelle")

    p_list = sub.add_parser("list", help="Lister toutes les licences")
    p_revoke = sub.add_parser("revoke", help="Révoquer / bannir une licence")
    p_revoke.add_argument("key")

    args = parser.parse_args()
    mgr = GLOBAL_LICENSE_MGR

    if args.cmd == "create":
        plan_map = {"7j": "7jours", "semaine": "7jours", "1m": "1mois", "mois": "1mois", "1a": "1an", "an": "1an", "vie": "vie", "lifetime": "vie"}
        target_plan = plan_map.get(args.plan, args.plan)
        lic = mgr.create_license(plan=target_plan, email=args.email, custom_key=args.key)
        print("\n" + "=" * 50)
        print(f" [ARCEUS] NOUVELLE LICENCE CRÉÉE :")
        print(f"  - CLÉ         : {lic['key']}")
        print(f"  - FORMULE     : {lic['plan_name']}")
        print(f"  - EXPIRATION  : {'À VIE' if lic['is_lifetime'] else time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lic['expires_at']))}")
        print("=" * 50 + "\n")

    elif args.cmd == "list":
        licenses = mgr.list_all_licenses()
        print("\n" + "=" * 70)
        print(f" TOTAL : {len(licenses)} LICENCES ENREGISTRÉES")
        print("=" * 70)
        for l in licenses:
            status = "ACTIF (EN LIGNE)" if l["is_active"] else "HORS LIGNE"
            exp_str = "À VIE" if l["is_lifetime"] else time.strftime("%Y-%m-%d %H:%M", time.localtime(l["expires_at"]))
            rem_str = "ILLIMITÉ" if l["is_lifetime"] else f"{l['remaining_seconds'] // 86400}j {(l['remaining_seconds'] % 86400) // 3600}h"
            print(f" {l['key']} | {l['plan'].upper():<8} | Exp: {exp_str:<16} | Reste: {rem_str:<12} | {status}")
        print("=" * 70 + "\n")

    elif args.cmd == "revoke":
        with mgr._get_conn() as conn:
            conn.execute("UPDATE licenses SET is_revoked = 1, active_session_token = NULL WHERE key = ?", (args.key.strip().upper(),))
            conn.commit()
        print(f"[ARCEUS] Licence {args.key} révoquée avec succès.")

    else:
        # Default run: display status summary
        print(f"[ARCEUS LICENSE ENGINE] Base: {DB_PATH.name} ({len(mgr.list_all_licenses())} licences)")
        print("Utilisez : python license_manager.py create --plan [7j|mois|an|vie]")
        print("           python license_manager.py list")

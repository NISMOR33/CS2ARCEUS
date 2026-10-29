# -*- coding: utf-8 -*-
"""
ARCEUS // CENTRAL CLOUD LICENSING & REALTIME ANTI-TAMPER SERVER
==============================================================
- Multi-PC Hardware Lock (HWID)
- Real-time Remote Ban & Kill-Switch
- Live Heartbeat Watchdog
- Dynamic Key Generation (7 Jours, 1 Mois, 1 An, À Vie)
- Stripe Webhook Auto-Fulfillment
- Admin Back-Office API
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
import os
from pathlib import Path
import secrets
import sqlite3
import sys
import threading
import time
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlparse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [SERVER] %(message)s"
)
logger = logging.getLogger("arceus_server")

DB_PATH = Path(os.environ.get("ARCEUS_DB_PATH", Path(__file__).resolve().parent / "licenses_cloud.db"))
ADMIN_PASSWORD = os.environ.get("ARCEUS_ADMIN_KEY", "dj2026")
PORT = int(os.environ.get("PORT", "8080"))

DURATIONS = {
    "7jours": 7 * 86400,
    "semaine": 7 * 86400,
    "weekly": 7 * 86400,
    "1mois": 30 * 86400,
    "mois": 30 * 86400,
    "monthly": 30 * 86400,
    "1an": 365 * 86400,
    "an": 365 * 86400,
    "yearly": 365 * 86400,
    "vie": -1,
    "lifetime": -1
}

PLAN_NAMES = {
    "7jours": "LICENCE 7 JOURS",
    "semaine": "LICENCE 7 JOURS",
    "1mois": "LICENCE 1 MOIS",
    "mois": "LICENCE 1 MOIS",
    "1an": "LICENCE 1 AN",
    "an": "LICENCE 1 AN",
    "vie": "LICENCE À VIE (PERMANENT)",
    "lifetime": "LICENCE À VIE (PERMANENT)"
}

class CloudLicenseManager:
    def __init__(self, db_path: Path):
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

            # Insérer clés maîtresses par défaut si vide
            count = conn.execute("SELECT COUNT(*) FROM licenses").fetchone()[0]
            if count == 0:
                now = time.time()
                conn.execute("""
                    INSERT INTO licenses (key, plan, duration_seconds, created_at, expires_at, bound_pseudo, active_hwid, is_revoked)
                    VALUES 
                    ('ARCEUS-MASTER-LIFETIME', 'vie', -1, ?, NULL, 'dj', NULL, 0),
                    ('ARCEUS-VIP-PRO-2026', '1an', ?, ?, ?, 'ZywOo_CS2', NULL, 0),
                    ('ARCEUS-DEMO-7JOURS', '7jours', ?, ?, ?, 'm0NESY_fan', NULL, 0)
                """, (now, 365*86400, now, now + 365*86400, 7*86400, now, now + 7*86400))
                conn.commit()
                logger.info("[DB] Initialisation des licences maîtres effectuée.")

    def create_key(self, plan: str, email: str = "", custom_key: Optional[str] = None) -> Dict[str, Any]:
        p = plan.lower().strip()
        dur = DURATIONS.get(p, 30 * 86400)
        now = time.time()
        exp = (now + dur) if dur > 0 else None
        
        alphabet = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
        r = lambda: "".join(secrets.choice(alphabet) for _ in range(4))
        key = (custom_key or f"ARCEUS-{r()}-{r()}-{r()}").strip().upper()

        with self._lock, self._get_conn() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO licenses (
                    key, plan, duration_seconds, created_at, expires_at,
                    bound_pseudo, active_hwid, active_session_token, last_heartbeat,
                    is_revoked, order_email, stripe_session_id
                ) VALUES (?, ?, ?, ?, ?, NULL, NULL, NULL, NULL, 0, ?, NULL)
            """, (key, p, dur, now, exp, email))
            conn.commit()

        logger.info("[LICENSE CREATE] Clé créée : %s (%s) pour %s", key, p, email or "client")
        return {
            "key": key,
            "plan": p,
            "plan_name": PLAN_NAMES.get(p, p.upper()),
            "created_at": now,
            "expires_at": exp,
            "is_lifetime": (dur == -1)
        }

    def revoke_key(self, key: str, revoke: bool = True) -> bool:
        k = key.strip().upper()
        with self._lock, self._get_conn() as conn:
            res = conn.execute("UPDATE licenses SET is_revoked = ? WHERE key = ?", (1 if revoke else 0, k))
            conn.commit()
            updated = (res.rowcount > 0)
        if updated:
            logger.warning("[LICENSE REVOKE] Clé %s : is_revoked = %s", k, revoke)
        return updated

    def login(self, key: str, pseudo: str, hwid: str) -> Dict[str, Any]:
        k = key.strip().upper()
        h = hwid.strip()
        now = time.time()

        with self._lock, self._get_conn() as conn:
            row = conn.execute("SELECT * FROM licenses WHERE key = ?", (k,)).fetchone()
            if not row:
                return {"ok": False, "error": "CLÉ INTROUVABLE // PAIEMENT REQUIS", "code": "KEY_NOT_FOUND"}

            if row["is_revoked"]:
                return {"ok": False, "error": "CETTE LICENCE A ÉTÉ BANIE / RÉVOQUÉE", "code": "KEY_REVOKED"}

            expires_at = row["expires_at"]
            is_lifetime = (row["duration_seconds"] == -1)

            if not is_lifetime and expires_at and now >= expires_at:
                return {"ok": False, "error": "LICENCE EXPIRÉE // RENOUVELLEMENT REQUIS", "code": "KEY_EXPIRED"}

            # Verrouillage concurrent : si un autre HWID a émis un heartbeat il y a moins de 45s
            last_hb = row["last_heartbeat"] or 0
            active_hwid = row["active_hwid"] or ""
            if active_hwid and active_hwid != h and (now - last_hb < 45):
                return {
                    "ok": False,
                    "error": "CETTE CLÉ EST DÉJÀ EN COURS D'UTILISATION SUR UN AUTRE ORDINATEUR",
                    "code": "CONCURRENT_SESSION_LOCKED"
                }

            token = f"SESS_{secrets.token_hex(16).upper()}"
            bound_pseudo = row["bound_pseudo"] or pseudo or "player"

            conn.execute("""
                UPDATE licenses SET
                    bound_pseudo = ?,
                    active_hwid = ?,
                    active_session_token = ?,
                    last_heartbeat = ?
                WHERE key = ?
            """, (bound_pseudo, h, token, now, k))
            conn.commit()

            rem = max(0, int(expires_at - now)) if (expires_at and not is_lifetime) else -1
            logger.info("[LOGIN SUCCESS] %s connecté avec %s sur HWID %s", bound_pseudo, k, h[:8] + "...")
            return {
                "ok": True,
                "key": k,
                "token": token,
                "plan": row["plan"],
                "plan_name": PLAN_NAMES.get(row["plan"], row["plan"].upper()),
                "is_lifetime": is_lifetime,
                "expires_at": expires_at,
                "remaining_seconds": rem,
                "bound_pseudo": bound_pseudo
            }

    def heartbeat(self, key: str, token: str, hwid: str) -> Dict[str, Any]:
        k = key.strip().upper()
        h = hwid.strip()
        now = time.time()

        with self._lock, self._get_conn() as conn:
            row = conn.execute("SELECT * FROM licenses WHERE key = ?", (k,)).fetchone()
            if not row:
                return {"ok": False, "status": "NOT_FOUND", "error": "Clé inexistante"}

            if row["is_revoked"]:
                logger.warning("[HEARTBEAT TERMINATION] Clé %s est marquée RÉVOQUÉE -> Ordre de kill envoyé !", k)
                return {"ok": False, "status": "REVOKED", "error": "LICENCE BANIE PAR L'ADMINISTRATION"}

            expires_at = row["expires_at"]
            is_lifetime = (row["duration_seconds"] == -1)

            if not is_lifetime and expires_at and now >= expires_at:
                logger.warning("[HEARTBEAT TERMINATION] Clé %s a expiré -> Ordre de kill envoyé !", k)
                return {"ok": False, "status": "EXPIRED", "error": "TEMPS ÉCOULÉ"}

            # Vérification token de session
            if row["active_session_token"] and row["active_session_token"] != token:
                return {"ok": False, "status": "KICKED", "error": "Session écrasée par une autre machine"}

            conn.execute("UPDATE licenses SET last_heartbeat = ? WHERE key = ?", (now, k))
            conn.commit()

            rem = max(0, int(expires_at - now)) if (expires_at and not is_lifetime) else -1
            return {"ok": True, "status": "ACTIVE", "remaining_seconds": rem}

    def list_all(self) -> list:
        now = time.time()
        with self._lock, self._get_conn() as conn:
            rows = conn.execute("SELECT * FROM licenses ORDER BY created_at DESC").fetchall()
            out = []
            for r in rows:
                is_lifetime = (r["duration_seconds"] == -1)
                exp = r["expires_at"]
                last_hb = r["last_heartbeat"] or 0
                is_online = bool(r["active_hwid"] and (now - last_hb < 45))
                rem = max(0, int(exp - now)) if (exp and not is_lifetime) else (-1 if is_lifetime else 0)
                out.append({
                    "key": r["key"],
                    "plan": r["plan"],
                    "plan_name": PLAN_NAMES.get(r["plan"], r["plan"].upper()),
                    "created_at": r["created_at"],
                    "expires_at": exp,
                    "is_lifetime": is_lifetime,
                    "bound_pseudo": r["bound_pseudo"] or "-",
                    "active_hwid": (r["active_hwid"][:8] + "...") if r["active_hwid"] else "-",
                    "is_active": is_online,
                    "is_revoked": bool(r["is_revoked"]),
                    "remaining_seconds": rem,
                    "order_email": r["order_email"] or ""
                })
            return out


MANAGER = CloudLicenseManager(DB_PATH)


class ArceusServerHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        return

    def _send_json(self, payload: Dict[str, Any], status: int = 200) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _read_json(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            return {}

    def do_OPTIONS(self) -> None:
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def _is_admin_auth(self) -> bool:
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth.split("Bearer ")[-1].strip()
            return (token == ADMIN_PASSWORD)
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        return (qs.get("admin_key", [""])[0] == ADMIN_PASSWORD)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)

        if parsed.path == "/api/health":
            self._send_json({"status": "UP", "time": time.time(), "service": "ARCEUS_CENTRAL_AUTH"})
            return

        if parsed.path in ("/api/admin/licenses", "/api/license/list"):
            if not self._is_admin_auth():
                self._send_json({"ok": False, "error": "NON AUTORISÉ // MOT DE PASSE REQUIS"}, 401)
                return
            licenses = MANAGER.list_all()
            self._send_json({"ok": True, "licenses": licenses})
            return

        # Servir index.html ou admin.html si présent dans le dossier SITE WEB
        site_web_dir = Path(__file__).resolve().parent / "SITE WEB"
        file_to_serve = None
        if parsed.path in ("/", "/index.html"):
            file_to_serve = site_web_dir / "index.html"
        elif parsed.path in ("/admin", "/admin.html"):
            file_to_serve = site_web_dir / "admin.html"
        elif parsed.path.startswith("/"):
            candidate = site_web_dir / parsed.path.lstrip("/")
            if candidate.exists() and candidate.is_file():
                file_to_serve = candidate

        if file_to_serve and file_to_serve.exists():
            data = file_to_serve.read_bytes()
            mime = "text/html; charset=utf-8"
            if file_to_serve.suffix == ".ico":
                mime = "image/x-icon"
            elif file_to_serve.suffix == ".png":
                mime = "image/png"
            elif file_to_serve.suffix == ".jpg":
                mime = "image/jpeg"
            elif file_to_serve.suffix == ".css":
                mime = "text/css"
            elif file_to_serve.suffix == ".js":
                mime = "application/javascript"

            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        self._send_json({"error": "Endpoint not found"}, 404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        data = self._read_json()

        # 1. Authentification Launcher
        if parsed.path in ("/api/auth/login", "/api/license/login"):
            key = str(data.get("key", ""))
            pseudo = str(data.get("pseudo", ""))
            hwid = str(data.get("hwid", ""))
            res = MANAGER.login(key, pseudo, hwid)
            status_code = 200 if res.get("ok") else 403
            self._send_json(res, status_code)
            return

        # 2. Heartbeat en jeu
        if parsed.path in ("/api/auth/heartbeat", "/api/license/heartbeat"):
            key = str(data.get("key", ""))
            token = str(data.get("token", ""))
            hwid = str(data.get("hwid", ""))
            res = MANAGER.heartbeat(key, token, hwid)
            self._send_json(res, 200 if res.get("ok") else 403)
            return

        # 3. Création de licence par Admin
        if parsed.path in ("/api/admin/create", "/api/license/create"):
            if not self._is_admin_auth():
                self._send_json({"ok": False, "error": "Non autorisé"}, 401)
                return
            plan = str(data.get("plan", "1mois"))
            email = str(data.get("email", ""))
            custom_key = data.get("custom_key")
            res = MANAGER.create_key(plan, email, custom_key)
            self._send_json({"ok": True, "license": res})
            return

        # 4. Révocation / Ban en direct par Admin
        if parsed.path in ("/api/admin/revoke", "/api/license/revoke"):
            if not self._is_admin_auth():
                self._send_json({"ok": False, "error": "Non autorisé"}, 401)
                return
            key = str(data.get("key", ""))
            revoke = bool(data.get("revoke", True))
            ok = MANAGER.revoke_key(key, revoke)
            self._send_json({"ok": ok, "key": key, "revoked": revoke})
            return

        # 5. Webhook Stripe (création automatique à l'achat)
        if parsed.path == "/api/webhook/stripe":
            event_type = data.get("type", "")
            logger.info("[STRIPE WEBHOOK] Événement reçu : %s", event_type)
            if event_type == "checkout.session.completed":
                obj = data.get("data", {}).get("object", {})
                email = obj.get("customer_details", {}).get("email") or obj.get("customer_email") or ""
                amount = obj.get("amount_total", 0) / 100.0
                
                # Détermine la formule par le montant
                plan = "1mois"
                if amount < 6.0:
                    plan = "7jours"
                elif amount < 15.0:
                    plan = "1mois"
                elif amount < 35.0:
                    plan = "1an"
                else:
                    plan = "vie"

                lic = MANAGER.create_key(plan, email)
                logger.info("[STRIPE AUTO-PROVISION] Licence %s générée pour %s (%s€)", lic["key"], email, amount)
                self._send_json({"ok": True, "created": lic})
                return

            self._send_json({"ok": True, "received": True})
            return

        self._send_json({"error": "Endpoint not found"}, 404)


def run_server():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), ArceusServerHandler)
    logger.info("═════════════════════════════════════════════════════════════")
    logger.info(" ARCEUS // SERVEUR CENTRAL D'AUTHENTIFICATION & ANTI-TAMPER")
    logger.info(" Port d'écoute : %d", PORT)
    logger.info(" Admin Password : %s", ADMIN_PASSWORD)
    logger.info(" Endpoints : /api/auth/login, /api/auth/heartbeat, /admin")
    logger.info("═════════════════════════════════════════════════════════════")
    server.serve_forever()


if __name__ == "__main__":
    run_server()

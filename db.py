from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
import json
import logging
import os
from pathlib import Path
import sqlite3
import threading
import time
from typing import Any, Dict, List, Optional, Tuple
import httpx

from econ_defs import (
    AppliedSticker,
    CSOEconItem,
    CSOEconItemEquipped,
    RARITY_MAP,
    WEAPON_DEF_INDEX,
    resolve_loadout_slot,
)

logger = logging.getLogger("cs2_skin_loader")

API_BASE_FR = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/fr"
API_BASE_EN = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en"

CATEGORY_ORDER: Dict[str, int] = {
    "Couteaux": 1,
    "Knives": 1,
    "Gants": 2,
    "Gloves": 2,
    "Fusils": 3,
    "Rifles": 3,
    "Pistolets": 4,
    "Pistols": 4,
    "PM": 5,
    "SMGs": 5,
    "Lourde": 6,
    "Heavy": 6,
    "Agents": 7,
    "Musiques": 8,
    "Caisses": 9,
    "Clés": 10,
    "Équipement": 11,
}


@dataclass
class SkinCatalogEntry:
    skin_id: str
    name: str
    weapon_id: str
    weapon_name: str
    category_name: str
    paint_index: int
    min_float: float
    max_float: float
    rarity_id: str
    rarity_name: str
    rarity_color: str
    rarity_rank: int
    stattrak_available: bool
    image_url: str


@dataclass
class StickerCatalogEntry:
    sticker_id: str
    def_index: int
    name: str
    rarity_name: str
    rarity_color: str
    rarity_rank: int
    image_url: str


@dataclass
class ImportedInventoryRow:
    item_id: int
    skin_id: str
    skin_name: str
    weapon_id: str
    weapon_name: str
    category_name: str
    def_index: int
    paint_index: int
    paint_seed: int
    paint_wear: float
    quality: int
    rarity: int
    stattrak_count: int
    custom_name: str
    equip_t: bool
    equip_ct: bool
    equipped_t: bool
    equipped_ct: bool
    image_url: str
    rarity_color: str
    stickers: List[Dict[str, Any]]


def compute_rarity_rank(rarity_id: str, category_name: str) -> int:
    cat_lower = category_name.lower()
    if "couteau" in cat_lower or "knive" in cat_lower or "gant" in cat_lower or "glove" in cat_lower:
        return 7
    return RARITY_MAP.get(rarity_id, 3)


def _fetch_endpoint_json(endpoint_file: str) -> List[Dict[str, Any]]:
    urls = [f"{API_BASE_FR}/{endpoint_file}", f"{API_BASE_EN}/{endpoint_file}"]
    with httpx.Client(timeout=35.0, follow_redirects=True) as client:
        for url in urls:
            try:
                logger.info("Téléchargement %s", url)
                resp = client.get(url)
                resp.raise_for_status()
                data = resp.json()
                if isinstance(data, list):
                    return data
            except Exception as exc:
                logger.warning("Échec %s (%s)", url, exc)
    return []


class SkinDatabase:
    def __init__(self, db_path: Path, socache_path: Path) -> None:
        self.db_path = db_path
        self.socache_path = socache_path
        self._lock = threading.Lock()
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS catalog (
                    skin_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    weapon_id TEXT NOT NULL,
                    weapon_name TEXT NOT NULL,
                    category_name TEXT NOT NULL,
                    paint_index INTEGER NOT NULL,
                    min_float REAL NOT NULL,
                    max_float REAL NOT NULL,
                    rarity_id TEXT NOT NULL,
                    rarity_name TEXT NOT NULL,
                    rarity_color TEXT NOT NULL,
                    rarity_rank INTEGER NOT NULL DEFAULT 3,
                    stattrak_available INTEGER NOT NULL,
                    image_url TEXT NOT NULL
                )
                """
            )
            cat_cols = {r[1] for r in cursor.execute("PRAGMA table_info(catalog)").fetchall()}
            if "rarity_rank" not in cat_cols:
                cursor.execute("ALTER TABLE catalog ADD COLUMN rarity_rank INTEGER NOT NULL DEFAULT 3")

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS stickers (
                    sticker_id TEXT PRIMARY KEY,
                    def_index INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    rarity_name TEXT NOT NULL,
                    rarity_color TEXT NOT NULL,
                    rarity_rank INTEGER NOT NULL DEFAULT 3,
                    image_url TEXT NOT NULL
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS inventory (
                    item_id INTEGER PRIMARY KEY,
                    skin_id TEXT NOT NULL DEFAULT '',
                    skin_name TEXT NOT NULL,
                    weapon_id TEXT NOT NULL,
                    weapon_name TEXT NOT NULL DEFAULT '',
                    category_name TEXT NOT NULL DEFAULT 'Armes',
                    def_index INTEGER NOT NULL,
                    paint_index INTEGER NOT NULL,
                    paint_seed INTEGER NOT NULL,
                    paint_wear REAL NOT NULL,
                    quality INTEGER NOT NULL,
                    rarity INTEGER NOT NULL,
                    stattrak_count INTEGER NOT NULL,
                    custom_name TEXT NOT NULL,
                    equip_t INTEGER NOT NULL,
                    equip_ct INTEGER NOT NULL,
                    image_url TEXT DEFAULT '',
                    rarity_color TEXT DEFAULT '#e4ae39',
                    stickers_json TEXT DEFAULT '[]'
                )
                """
            )
            inv_cols = {r[1] for r in cursor.execute("PRAGMA table_info(inventory)").fetchall()}
            if "skin_id" not in inv_cols:
                cursor.execute("ALTER TABLE inventory ADD COLUMN skin_id TEXT DEFAULT ''")
            if "image_url" not in inv_cols:
                cursor.execute("ALTER TABLE inventory ADD COLUMN image_url TEXT DEFAULT ''")
            if "rarity_color" not in inv_cols:
                cursor.execute("ALTER TABLE inventory ADD COLUMN rarity_color TEXT DEFAULT '#e4ae39'")
            if "weapon_name" not in inv_cols:
                cursor.execute("ALTER TABLE inventory ADD COLUMN weapon_name TEXT DEFAULT ''")
            if "category_name" not in inv_cols:
                cursor.execute("ALTER TABLE inventory ADD COLUMN category_name TEXT DEFAULT 'Armes'")
            if "stickers_json" not in inv_cols:
                cursor.execute("ALTER TABLE inventory ADD COLUMN stickers_json TEXT DEFAULT '[]'")
            self.conn.commit()

    def needs_full_sync(self) -> bool:
        with self._lock:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(DISTINCT category_name) FROM catalog")
            cat_cnt = int(cur.fetchone()[0] or 0)
            cur.execute("SELECT COUNT(*) FROM stickers")
            st_cnt = int(cur.fetchone()[0] or 0)
            return cat_cnt < 8 or st_cnt == 0

    def sync_catalog_from_api(self, _api_url: Optional[str] = None) -> int:
        endpoints = ["skins.json", "agents.json", "music_kits.json", "crates.json", "keys.json", "stickers.json"]
        results: Dict[str, List[Dict[str, Any]]] = {}
        with ThreadPoolExecutor(max_workers=6) as pool:
            future_map = {pool.submit(_fetch_endpoint_json, ep): ep for ep in endpoints}
            for fut, ep in future_map.items():
                results[ep] = fut.result()

        catalog_rows: List[Tuple[Any, ...]] = []

        # 1. SKINS (Armes, Couteaux, Gants)
        for item in results.get("skins.json", []):
            paint_str = item.get("paint_index")
            if not paint_str:
                continue
            try:
                paint_idx = int(paint_str)
            except ValueError:
                continue
            weapon_obj = item.get("weapon") or {}
            category_obj = item.get("category") or {}
            rarity_obj = item.get("rarity") or {}

            weapon_id = str(weapon_obj.get("id") or "weapon_ak47")
            weapon_name = str(weapon_obj.get("name") or "Arme")
            category_name = str(category_obj.get("name") or "Autre")
            min_f = float(item.get("min_float") if item.get("min_float") is not None else 0.0)
            max_f = float(item.get("max_float") if item.get("max_float") is not None else 1.0)
            rarity_id = str(rarity_obj.get("id") or "rarity_rare_weapon")
            rarity_name = str(rarity_obj.get("name") or "Standard")
            rarity_color = str(rarity_obj.get("color") or "#4b69ff")
            rarity_rank = compute_rarity_rank(rarity_id, category_name)
            stattrak = 1 if item.get("stattrak") else 0
            image_url = str(item.get("image") or "")

            catalog_rows.append(
                (
                    str(item.get("id")),
                    str(item.get("name")),
                    weapon_id,
                    weapon_name,
                    category_name,
                    paint_idx,
                    min_f,
                    max_f,
                    rarity_id,
                    rarity_name,
                    rarity_color,
                    rarity_rank,
                    stattrak,
                    image_url,
                )
            )

        # 2. AGENTS (Personnages CT & T)
        for idx, item in enumerate(results.get("agents.json", []), start=1):
            rarity_obj = item.get("rarity") or {}
            team_obj = item.get("team") or {}
            team_id = str(team_obj.get("id") or "terrorist")
            team_label = "Agents Anti-Terroristes (CT)" if "counter" in team_id.lower() else "Agents Terroristes (T)"
            def_idx = int(item.get("def_index") or (4700 + idx))
            r_id = str(rarity_obj.get("id") or "rarity_legendary_character")
            r_name = str(rarity_obj.get("name") or "Agent")
            r_color = str(rarity_obj.get("color") or "#d32ce6")
            r_rank = RARITY_MAP.get(r_id, 5)
            catalog_rows.append(
                (
                    str(item.get("id") or f"agent-{def_idx}"),
                    str(item.get("name") or "Agent"),
                    f"agent_{def_idx}",
                    team_label,
                    "Agents",
                    def_idx,
                    0.0,
                    0.0,
                    r_id,
                    r_name,
                    r_color,
                    r_rank,
                    0,
                    str(item.get("image") or ""),
                )
            )

        # 3. MUSIQUES (Disques de musique)
        for idx, item in enumerate(results.get("music_kits.json", []), start=1):
            name_str = str(item.get("name") or "Kit de musique")
            is_st = "stattrak" in name_str.lower()
            group_label = "Kits de musique StatTrak™" if is_st else "Kits de musique"
            rarity_obj = item.get("rarity") or {}
            def_idx = int(str(item.get("def_index") or idx).split("_")[0] if str(item.get("def_index") or "").isdigit() else idx)
            r_id = str(rarity_obj.get("id") or "rarity_rare")
            r_name = str(rarity_obj.get("name") or "Haute qualité")
            r_color = str(rarity_obj.get("color") or "#4b69ff")
            catalog_rows.append(
                (
                    str(item.get("id") or f"music-{idx}"),
                    name_str,
                    f"music_kit_{def_idx}",
                    group_label,
                    "Musiques",
                    def_idx,
                    0.0,
                    0.0,
                    r_id,
                    r_name,
                    r_color,
                    5 if is_st else 4,
                    1 if is_st else 0,
                    str(item.get("image") or ""),
                )
            )

        # 4. CAISSES (Cases, Capsules, Souvenirs)
        for idx, item in enumerate(results.get("crates.json", []), start=1):
            crate_type = str(item.get("type") or "Caisse")
            rarity_obj = item.get("rarity") or {}
            def_idx = int(item.get("def_index") or (4000 + idx)) if str(item.get("def_index") or "").isdigit() else (4000 + idx)
            r_name = str(rarity_obj.get("name") or "Conteneur")
            r_color = str(rarity_obj.get("color") or "#e4ae39")
            catalog_rows.append(
                (
                    str(item.get("id") or f"crate-{idx}"),
                    str(item.get("name") or "Caisse"),
                    f"crate_{def_idx}",
                    crate_type,
                    "Caisses",
                    def_idx,
                    0.0,
                    0.0,
                    "rarity_rare",
                    r_name,
                    r_color,
                    4,
                    0,
                    str(item.get("image") or ""),
                )
            )

        # 5. CLÉS (Keys)
        for idx, item in enumerate(results.get("keys.json", []), start=1):
            def_idx = 1203 + idx
            catalog_rows.append(
                (
                    str(item.get("id") or f"key-{idx}"),
                    str(item.get("name") or "Clé de caisse"),
                    f"key_{def_idx}",
                    "Clés de caisses CS2",
                    "Clés",
                    def_idx,
                    0.0,
                    0.0,
                    "rarity_rare",
                    "Clé officielle",
                    "#e4ae39",
                    5,
                    0,
                    str(item.get("image") or ""),
                )
            )

        # 6. STICKERS
        sticker_rows: List[Tuple[Any, ...]] = []
        for idx, item in enumerate(results.get("stickers.json", []), start=1):
            def_raw = item.get("def_index")
            def_idx = int(def_raw) if str(def_raw or "").isdigit() else idx
            rarity_obj = item.get("rarity") or {}
            r_id = str(rarity_obj.get("id") or "rarity_rare")
            r_name = str(rarity_obj.get("name") or "Sticker")
            r_color = str(rarity_obj.get("color") or "#4b69ff")
            r_rank = RARITY_MAP.get(r_id, 3)
            img = str(item.get("image") or "")
            if not img:
                continue
            sticker_rows.append(
                (
                    str(item.get("id") or f"sticker-{def_idx}"),
                    def_idx,
                    str(item.get("name") or f"Sticker #{def_idx}"),
                    r_name,
                    r_color,
                    r_rank,
                    img,
                )
            )

        with self._lock:
            cur = self.conn.cursor()
            cur.executemany(
                """
                INSERT OR REPLACE INTO catalog (
                    skin_id, name, weapon_id, weapon_name, category_name,
                    paint_index, min_float, max_float, rarity_id, rarity_name,
                    rarity_color, rarity_rank, stattrak_available, image_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                catalog_rows,
            )
            if sticker_rows:
                cur.executemany(
                    """
                    INSERT OR REPLACE INTO stickers (
                        sticker_id, def_index, name, rarity_name,
                        rarity_color, rarity_rank, image_url
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    sticker_rows,
                )
            self.conn.commit()

        logger.info("%d objets catalogue + %d stickers indexés", len(catalog_rows), len(sticker_rows))
        return len(catalog_rows)

    def search_stickers(self, query: str = "", limit: int = 120) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM stickers WHERE 1=1"
        params: List[Any] = []
        if query.strip():
            sql += " AND (LOWER(name) LIKE ? OR CAST(def_index AS TEXT) = ?)"
            q_like = f"%{query.strip().lower()}%"
            params.extend([q_like, query.strip()])
        sql += " ORDER BY rarity_rank DESC, def_index DESC LIMIT ?"
        params.append(limit)

        with self._lock:
            cur = self.conn.cursor()
            cur.execute(sql, params)
            rows = cur.fetchall()
        return [
            asdict(
                StickerCatalogEntry(
                    sticker_id=str(r["sticker_id"]),
                    def_index=int(r["def_index"]),
                    name=str(r["name"]),
                    rarity_name=str(r["rarity_name"]),
                    rarity_color=str(r["rarity_color"]),
                    rarity_rank=int(r["rarity_rank"]),
                    image_url=str(r["image_url"]),
                )
            )
            for r in rows
        ]

    def get_skin_by_id(self, skin_id: str) -> Optional[SkinCatalogEntry]:
        with self._lock:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM catalog WHERE skin_id = ?", (skin_id,))
            r = cur.fetchone()
            if not r:
                return None
            return SkinCatalogEntry(
                skin_id=r["skin_id"],
                name=r["name"],
                weapon_id=r["weapon_id"],
                weapon_name=r["weapon_name"],
                category_name=r["category_name"],
                paint_index=int(r["paint_index"]),
                min_float=float(r["min_float"]),
                max_float=float(r["max_float"]),
                rarity_id=r["rarity_id"],
                rarity_name=r["rarity_name"],
                rarity_color=r["rarity_color"],
                rarity_rank=int(r["rarity_rank"]),
                stattrak_available=bool(r["stattrak_available"]),
                image_url=r["image_url"],
            )

    def search_catalog(
        self,
        query: str = "",
        category: str = "Toutes",
        weapon_name: str = "Toutes",
        rarity_rank: int = 0,
        only_stattrak: bool = False,
        sort_by: str = "rarity_desc",
    ) -> List[Dict[str, object]]:
        sql = "SELECT * FROM catalog WHERE 1=1"
        params: List[object] = []

        if category and category != "Toutes":
            sql += " AND category_name = ?"
            params.append(category)

        if weapon_name and weapon_name != "Toutes":
            sql += " AND weapon_name = ?"
            params.append(weapon_name)

        if rarity_rank > 0:
            sql += " AND rarity_rank = ?"
            params.append(rarity_rank)

        if only_stattrak:
            sql += " AND stattrak_available = 1"

        if query.strip():
            sql += " AND (LOWER(name) LIKE ? OR LOWER(weapon_name) LIKE ? OR CAST(paint_index AS TEXT) = ?)"
            q_like = f"%{query.strip().lower()}%"
            params.extend([q_like, q_like, query.strip()])

        order_map = {
            "rarity_desc": "rarity_rank DESC, name ASC",
            "rarity_asc": "rarity_rank ASC, name ASC",
            "name_asc": "name ASC",
            "paint_asc": "paint_index ASC",
            "float_asc": "min_float ASC, rarity_rank DESC",
        }
        sql += f" ORDER BY {order_map.get(sort_by, order_map['rarity_desc'])}"

        with self._lock:
            cur = self.conn.cursor()
            cur.execute(sql, params)
            rows = cur.fetchall()

        return [
            {
                **asdict(
                    SkinCatalogEntry(
                        skin_id=r["skin_id"],
                        name=r["name"],
                        weapon_id=r["weapon_id"],
                        weapon_name=r["weapon_name"],
                        category_name=r["category_name"],
                        paint_index=int(r["paint_index"]),
                        min_float=float(r["min_float"]),
                        max_float=float(r["max_float"]),
                        rarity_id=r["rarity_id"],
                        rarity_name=r["rarity_name"],
                        rarity_color=r["rarity_color"],
                        rarity_rank=int(r["rarity_rank"]),
                        stattrak_available=bool(r["stattrak_available"]),
                        image_url=r["image_url"],
                    )
                ),
                "skin_name": r["name"],
                "stattrak": bool(r["stattrak_available"]),
            }
            for r in rows
        ]

    def get_navigation_metadata(self) -> Dict[str, object]:
        with self._lock:
            cur = self.conn.cursor()
            cur.execute(
                """
                SELECT category_name, COUNT(*) as cnt, COUNT(DISTINCT weapon_name) as w_cnt
                FROM catalog
                GROUP BY category_name
                """
            )
            cat_rows = [
                {
                    "name": str(r["category_name"]),
                    "count": int(r["cnt"]),
                    "weapon_count": int(r["w_cnt"]),
                }
                for r in cur.fetchall()
                if r["category_name"]
            ]
            cat_rows.sort(key=lambda x: (CATEGORY_ORDER.get(str(x["name"]), 99), str(x["name"])))

            cur.execute(
                """
                SELECT
                    category_name,
                    weapon_id,
                    weapon_name,
                    COUNT(*) as cnt,
                    MAX(rarity_rank) as top_rank,
                    image_url,
                    rarity_color
                FROM (
                    SELECT * FROM catalog ORDER BY rarity_rank ASC, paint_index DESC
                )
                GROUP BY category_name, weapon_name
                ORDER BY weapon_name ASC
                """
            )
            weapons_by_cat: Dict[str, List[Dict[str, object]]] = {}
            for r in cur.fetchall():
                c_name = str(r["category_name"])
                img_u = str(r["image_url"] or "")
                w_name = str(r["weapon_name"])
                w_entry = {
                    "weapon_id": str(r["weapon_id"]),
                    "name": w_name,
                    "weapon_name": w_name,
                    "category": c_name,
                    "count": int(r["cnt"]),
                    "preview_image": img_u,
                    "icon": img_u,
                    "accent_color": str(r["rarity_color"] or "#e4ae39"),
                }
                weapons_by_cat.setdefault(c_name, []).append(w_entry)

            total = sum(int(c["count"]) for c in cat_rows)
            for c in cat_rows:
                w_list = weapons_by_cat.get(str(c["name"]), [])
                icon_u = w_list[0]["preview_image"] if w_list else ""
                c["icon_url"] = icon_u
                c["icon"] = icon_u

            return {
                "total": total,
                "categories": cat_rows,
                "weapons_by_category": weapons_by_cat,
            }

    def import_econ_item(
        self,
        entry: SkinCatalogEntry,
        paint_wear: float,
        paint_seed: int,
        stattrak_count: int,
        custom_name: str,
        equip_t: bool,
        equip_ct: bool,
        stickers_raw: Optional[List[Dict[str, Any]]] = None,
    ) -> CSOEconItem:
        item_id = int(time.time() * 1000)
        def_index = WEAPON_DEF_INDEX.get(entry.weapon_id, entry.paint_index if entry.category_name in ("Agents", "Musiques", "Caisses", "Clés") else 7)
        is_special = "knife" in entry.weapon_id or "bayonet" in entry.weapon_id or "gloves" in entry.weapon_id
        quality = 3 if is_special else (9 if stattrak_count >= 0 else 4)
        rarity = RARITY_MAP.get(entry.rarity_id, 4)
        clean_stickers: List[Dict[str, Any]] = stickers_raw or []

        with self._lock:
            cur = self.conn.cursor()
            if entry.category_name not in ("Caisses", "Clés"):
                if entry.category_name in ("Couteaux", "Gants", "Musiques"):
                    cur.execute("DELETE FROM inventory WHERE category_name = ?", (entry.category_name,))
                else:
                    cur.execute("DELETE FROM inventory WHERE weapon_id = ?", (entry.weapon_id,))

            cur.execute(
                """
                INSERT INTO inventory (
                    item_id, skin_id, skin_name, weapon_id, weapon_name, category_name, def_index, paint_index,
                    paint_seed, paint_wear, quality, rarity, stattrak_count,
                    custom_name, equip_t, equip_ct, image_url, rarity_color, stickers_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item_id,
                    entry.skin_id,
                    entry.name,
                    entry.weapon_id,
                    entry.weapon_name,
                    entry.category_name,
                    def_index,
                    entry.paint_index,
                    paint_seed,
                    paint_wear,
                    quality,
                    rarity,
                    stattrak_count,
                    custom_name,
                    1 if equip_t else 0,
                    1 if equip_ct else 0,
                    entry.image_url,
                    entry.rarity_color,
                    json.dumps(clean_stickers, ensure_ascii=False),
                ),
            )
            self.conn.commit()
        self.export_socache()

        equipped: List[CSOEconItemEquipped] = []
        slot_t = resolve_loadout_slot(entry.weapon_id, entry.category_name, is_ct=False)
        slot_ct = resolve_loadout_slot(entry.weapon_id, entry.category_name, is_ct=True)
        if equip_t and slot_t >= 0:
            equipped.append(CSOEconItemEquipped(new_class=2, new_slot=slot_t))
        if equip_ct and slot_ct >= 0:
            equipped.append(CSOEconItemEquipped(new_class=3, new_slot=slot_ct))

        applied_stickers = [
            AppliedSticker(
                slot=int(s.get("slot", 0)),
                sticker_id=int(s.get("sticker_id") or s.get("def_index") or 0),
                name=str(s.get("name", "")),
                image_url=str(s.get("image_url", "")),
                wear=float(s.get("wear", 0.0)),
                scale=float(s.get("scale", 1.0)),
                rotation=float(s.get("rotation", 0.0)),
                offset_x=float(s.get("offset_x", 0.0)),
                offset_y=float(s.get("offset_y", 0.0)),
            )
            for s in clean_stickers
            if s and int(s.get("sticker_id") or s.get("def_index") or 0) > 0
        ]

        return CSOEconItem(
            item_id=item_id,
            account_id=int(os.environ.get("CS2_STEAM_ACCOUNT_ID", "100000001")),
            def_index=def_index,
            inventory_pos=(1 << 30) | (item_id & 0xFFFF),
            quality=quality,
            rarity=rarity,
            paint_index=entry.paint_index if entry.category_name not in ("Agents", "Musiques", "Caisses", "Clés") else 0,
            paint_seed=paint_seed,
            paint_wear=paint_wear,
            custom_name=custom_name,
            stattrak_count=stattrak_count,
            stickers=applied_stickers,
            equipped_state=equipped,
        )

    def list_inventory(self) -> List[ImportedInventoryRow]:
        with self._lock:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM inventory ORDER BY equip_t DESC, equip_ct DESC, item_id DESC")
            rows = cur.fetchall()
        result: List[ImportedInventoryRow] = []
        for r in rows:
            try:
                st_list = json.loads(str(r["stickers_json"] or "[]"))
            except Exception:
                st_list = []
            eq_t = bool(r["equip_t"])
            eq_ct = bool(r["equip_ct"])
            result.append(
                ImportedInventoryRow(
                    item_id=int(r["item_id"]),
                    skin_id=str(r["skin_id"] or ""),
                    skin_name=str(r["skin_name"]),
                    weapon_id=str(r["weapon_id"]),
                    weapon_name=str(r["weapon_name"] or r["weapon_id"]),
                    category_name=str(r["category_name"] or "Armes"),
                    def_index=int(r["def_index"]),
                    paint_index=int(r["paint_index"]),
                    paint_seed=int(r["paint_seed"]),
                    paint_wear=float(r["paint_wear"]),
                    quality=int(r["quality"]),
                    rarity=int(r["rarity"]),
                    stattrak_count=int(r["stattrak_count"]),
                    custom_name=str(r["custom_name"]),
                    equip_t=eq_t,
                    equip_ct=eq_ct,
                    equipped_t=eq_t,
                    equipped_ct=eq_ct,
                    image_url=str(r["image_url"] or ""),
                    rarity_color=str(r["rarity_color"] or "#e4ae39"),
                    stickers=st_list,
                )
            )
        return result

    def delete_inventory_item(self, item_id: int) -> None:
        with self._lock:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM inventory WHERE item_id = ?", (item_id,))
            self.conn.commit()
        self.export_socache()

    def export_socache(self) -> Path:
        rows = self.list_inventory()
        account_id = int(os.environ.get("CS2_STEAM_ACCOUNT_ID", "100000001"))
        econ_items = []
        for idx, r in enumerate(rows, start=1):
            equipped: List[CSOEconItemEquipped] = []
            slot_t = resolve_loadout_slot(r.weapon_id, r.category_name, is_ct=False)
            slot_ct = resolve_loadout_slot(r.weapon_id, r.category_name, is_ct=True)
            if r.equip_t and slot_t >= 0:
                equipped.append(CSOEconItemEquipped(new_class=2, new_slot=slot_t))
            if r.equip_ct and slot_ct >= 0:
                equipped.append(CSOEconItemEquipped(new_class=3, new_slot=slot_ct))
            applied_stickers = [
                AppliedSticker(
                    slot=int(s.get("slot", 0)),
                    sticker_id=int(s.get("sticker_id") or s.get("def_index") or 0),
                    name=str(s.get("name", "")),
                    image_url=str(s.get("image_url", "")),
                    wear=float(s.get("wear", 0.0)),
                    scale=float(s.get("scale", 1.0)),
                    rotation=float(s.get("rotation", 0.0)),
                    offset_x=float(s.get("offset_x", 0.0)),
                    offset_y=float(s.get("offset_y", 0.0)),
                )
                for s in r.stickers
                if s and int(s.get("sticker_id") or s.get("def_index") or 0) > 0
            ]
            item = CSOEconItem(
                item_id=r.item_id,
                account_id=account_id,
                def_index=r.def_index,
                inventory_pos=(1 << 30) | idx,
                quality=r.quality,
                rarity=r.rarity,
                paint_index=r.paint_index if r.category_name not in ("Agents", "Musiques", "Caisses", "Clés") else 0,
                paint_seed=r.paint_seed,
                paint_wear=r.paint_wear,
                custom_name=r.custom_name,
                stattrak_count=r.stattrak_count,
                stickers=applied_stickers,
                equipped_state=equipped,
            )
            econ_items.append(item.to_socache_dict())

        payload = {
            "type_id": 1,
            "description": "CGCClientSharedObjectTypeCache<CSOEconItem>",
            "owner_soid": {"type": 1, "id": account_id},
            "objects": econ_items,
        }
        tmp_path = self.socache_path.with_suffix(".json.tmp")
        tmp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        os.replace(str(tmp_path), str(self.socache_path))
        return self.socache_path

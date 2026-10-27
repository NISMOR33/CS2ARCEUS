from dataclasses import dataclass, field
import os
import struct
import zlib
from typing import Any, Dict, List, Tuple

# Attributs officiels CEconItem / CSOEconItem (Source 2 GC Schema)
ATTR_PAINT_INDEX: int = 6
ATTR_PAINT_SEED: int = 7
ATTR_PAINT_WEAR: int = 8
ATTR_KILLEATER_SCORE: int = 80
ATTR_KILLEATER_TYPE: int = 81

# Slots Stickers 0..4 (5 slots CS2) : stride = 4
# +0 = ID (uint32), +1 = Wear (float), +2 = Scale (float), +3 = Rotation (float)
ATTR_STICKER_ID_BASE: int = 113
ATTR_STICKER_WEAR_BASE: int = 114
ATTR_STICKER_SCALE_BASE: int = 115
ATTR_STICKER_ROTATION_BASE: int = 116
# CS2 Call to Arms free-placement offsets (slot 0..4 : 278 + slot*2 = offset_x, 279 + slot*2 = offset_y)
ATTR_STICKER_OFFSET_X_BASE: int = 278
ATTR_STICKER_OFFSET_Y_BASE: int = 279

WEAPON_DEF_INDEX: Dict[str, int] = {
    "weapon_deagle": 1,
    "weapon_elite": 2,
    "weapon_fiveseven": 3,
    "weapon_glock": 4,
    "weapon_ak47": 7,
    "weapon_aug": 8,
    "weapon_awp": 9,
    "weapon_famas": 10,
    "weapon_g3sg1": 11,
    "weapon_galilar": 13,
    "weapon_m249": 14,
    "weapon_m4a1": 16,
    "weapon_mac10": 17,
    "weapon_p90": 19,
    "weapon_mp5sd": 23,
    "weapon_ump45": 24,
    "weapon_xm1014": 25,
    "weapon_bizon": 26,
    "weapon_mag7": 27,
    "weapon_negev": 28,
    "weapon_sawedoff": 29,
    "weapon_tec9": 30,
    "weapon_hkp2000": 32,
    "weapon_mp7": 33,
    "weapon_mp9": 34,
    "weapon_nova": 35,
    "weapon_p250": 36,
    "weapon_scar20": 38,
    "weapon_sg556": 39,
    "weapon_ssg08": 40,
    "weapon_m4a1_silencer": 60,
    "weapon_usp_silencer": 61,
    "weapon_cz75a": 63,
    "weapon_revolver": 64,
    "weapon_bayonet": 500,
    "weapon_knife_css": 503,
    "weapon_knife_flip": 505,
    "weapon_knife_gut": 506,
    "weapon_knife_karambit": 507,
    "weapon_knife_m9_bayonet": 508,
    "weapon_knife_tactical": 509,
    "weapon_knife_falchion": 512,
    "weapon_knife_survival_bowie": 514,
    "weapon_knife_butterfly": 515,
    "weapon_knife_push": 516,
    "weapon_knife_cord": 517,
    "weapon_knife_canis": 518,
    "weapon_knife_ursus": 519,
    "weapon_knife_gypsy_jackknife": 520,
    "weapon_knife_outdoor": 521,
    "weapon_knife_stiletto": 522,
    "weapon_knife_widowmaker": 523,
    "weapon_knife_skeleton": 525,
    "weapon_knife_kukri": 526,
    "studded_bloodhound_gloves": 5027,
    "sporty_gloves": 5030,
    "slick_gloves": 5031,
    "leather_handwraps": 5032,
    "motorcycle_gloves": 5033,
    "specialist_gloves": 5034,
    "studded_hydra_gloves": 5035,
    "studded_brokenfang_gloves": 4725,
}

# Table réelle des emplacements d'équipement CS2 Loadout 2.0 (loadout_slot_t)
# Source : Valve CS2 Schema (loadout_slot_t)
# 0 = LOADOUT_SLOT_MELEE (Couteau)
# 2..6 = LOADOUT_SLOT_SECONDARY0..4 (5 emplacements Pistolets)
# 8..12 = LOADOUT_SLOT_SMG0..4 (5 emplacements Mid-Tier : PM + Pompe + Mitrailleuses)
# 14..18 = LOADOUT_SLOT_RIFLE0..4 (5 emplacements Fusils)
# 38 = LOADOUT_SLOT_CLOTHING_CUSTOMPLAYER (Agent T / CT)
# 41 = LOADOUT_SLOT_CLOTHING_HANDS (Gants)
# 54 = LOADOUT_SLOT_MUSICKIT (Kit de musique)
WEAPON_LOADOUT_SLOT: Dict[str, int] = {
    # Pistolets (2..6)
    "weapon_glock": 2,
    "weapon_hkp2000": 2,
    "weapon_usp_silencer": 2,
    "weapon_elite": 3,
    "weapon_p250": 4,
    "weapon_tec9": 5,
    "weapon_fiveseven": 5,
    "weapon_cz75a": 5,
    "weapon_deagle": 6,
    "weapon_revolver": 6,
    # Mid-Tier : PM & Lourdes (8..12)
    "weapon_mac10": 8,
    "weapon_mp9": 8,
    "weapon_mp7": 9,
    "weapon_mp5sd": 9,
    "weapon_ump45": 9,
    "weapon_p90": 10,
    "weapon_bizon": 10,
    "weapon_nova": 11,
    "weapon_xm1014": 11,
    "weapon_sawedoff": 11,
    "weapon_mag7": 11,
    "weapon_m249": 12,
    "weapon_negev": 12,
    # Fusils (14..18)
    "weapon_galilar": 14,
    "weapon_famas": 14,
    "weapon_ak47": 15,
    "weapon_m4a1": 15,
    "weapon_m4a1_silencer": 15,
    "weapon_ssg08": 16,
    "weapon_sg556": 17,
    "weapon_aug": 17,
    "weapon_awp": 18,
    "weapon_g3sg1": 18,
    "weapon_scar20": 18,
}


def resolve_loadout_slot(weapon_id: str, category_name: str, is_ct: bool) -> int:
    if weapon_id in WEAPON_LOADOUT_SLOT:
        return WEAPON_LOADOUT_SLOT[weapon_id]
    if "knife" in weapon_id or "bayonet" in weapon_id or category_name == "Couteaux":
        return 0
    if "gloves" in weapon_id or "handwraps" in weapon_id or category_name == "Gants":
        return 41
    if category_name == "Agents":
        return 38
    if category_name == "Musiques":
        return 54
    return -1


RARITY_MAP: Dict[str, int] = {
    "rarity_common_weapon": 1,
    "rarity_common": 1,
    "rarity_uncommon_weapon": 2,
    "rarity_uncommon": 2,
    "rarity_rare_weapon": 3,
    "rarity_rare": 3,
    "rarity_rare_character": 3,
    "rarity_mythical_weapon": 4,
    "rarity_mythical": 4,
    "rarity_mythical_character": 4,
    "rarity_legendary_weapon": 5,
    "rarity_legendary": 5,
    "rarity_legendary_character": 5,
    "rarity_ancient_weapon": 6,
    "rarity_ancient": 6,
    "rarity_ancient_character": 6,
    "rarity_contraband": 7,
}


def float_to_ieee754_bits(value: float) -> int:
    packed = struct.pack("<f", value)
    return struct.unpack("<I", packed)[0]


def ieee754_bits_to_float(bits: int) -> float:
    packed = struct.pack("<I", bits & 0xFFFFFFFF)
    return struct.unpack("<f", packed)[0]


def _encode_varint(value: int) -> bytes:
    out = bytearray()
    val = value & 0xFFFFFFFFFFFFFFFF
    while val > 0x7F:
        out.append((val & 0x7F) | 0x80)
        val >>= 7
    out.append(val & 0x7F)
    return bytes(out)


def _decode_varint(data: bytes, offset: int) -> Tuple[int, int]:
    result = 0
    shift = 0
    pos = offset
    while pos < len(data):
        b = data[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            return result, pos
        shift += 7
    raise ValueError("Varint tronqué dans CEconItemPreviewDataBlock")


@dataclass
class AppliedSticker:
    slot: int
    sticker_id: int
    name: str
    image_url: str
    wear: float = 0.0
    scale: float = 1.0
    rotation: float = 0.0
    offset_x: float = 0.0
    offset_y: float = 0.0


def build_cs2_inspect_url(
    def_index: int,
    paint_index: int,
    paint_seed: int,
    paint_wear: float,
    rarity: int,
    quality: int,
    stattrak_count: int = -1,
    custom_name: str = "",
    stickers: List[AppliedSticker] = None,
    account_id: int = 0,
    item_id: int = 0,
) -> str:
    """
    Construit un lien officiel steam://rungame/730/.../+csgo_econ_action_preview
    strictement conforme au schéma Protobuf CEconItemPreviewDataBlock :
      - field 1 (0x08): accountid (varint)
      - field 2 (0x10): itemid (varint)
      - field 3 (0x18): defindex (varint)
      - field 4 (0x20): paintindex (varint)
      - field 5 (0x28): rarity (varint)
      - field 6 (0x30): quality (varint)
      - field 7 (0x38): paintwear (varint des bits IEEE-754 uint32)
      - field 8 (0x40): paintseed (varint)
      - field 9 (0x48): killeaterscoretype (varint)
      - field 10 (0x50): killeatervalue (varint)
      - field 11 (0x5A): customname (bytes length-delimited)
      - field 12 (0x62): stickers (repeated Sticker message :
            1=slot [0x08], 2=sticker_id [0x10], 3=wear [0x1D],
            4=scale [0x25], 5=rotation [0x2D], 7=offset_x [0x3D], 8=offset_y [0x45])
    """
    proto = bytearray()
    if account_id > 0:
        proto.append(0x08)
        proto.extend(_encode_varint(account_id))
    if item_id > 0:
        proto.append(0x10)
        proto.extend(_encode_varint(item_id))

    # Field 3 (tag 0x18): defindex
    proto.append(0x18)
    proto.extend(_encode_varint(def_index))
    # Field 4 (tag 0x20): paintindex
    proto.append(0x20)
    proto.extend(_encode_varint(paint_index))
    # Field 5 (tag 0x28): rarity
    proto.append(0x28)
    proto.extend(_encode_varint(rarity))
    # Field 6 (tag 0x30): quality
    proto.append(0x30)
    proto.extend(_encode_varint(quality))
    # Field 7 (tag 0x38): paintwear (uint32 IEEE-754 bits en varint)
    proto.append(0x38)
    proto.extend(_encode_varint(float_to_ieee754_bits(paint_wear)))
    # Field 8 (tag 0x40): paintseed
    proto.append(0x40)
    proto.extend(_encode_varint(paint_seed))

    # Field 9 (tag 0x48) & Field 10 (tag 0x50): killeaterscoretype & killeatervalue
    if stattrak_count >= 0:
        proto.extend(b"\x48\x00\x50")
        proto.extend(_encode_varint(stattrak_count))

    # Field 11 (tag 0x5A): customname (wire_type = 2)
    if custom_name:
        name_bytes = custom_name.encode("utf-8")[:32]
        proto.append(0x5A)
        proto.extend(_encode_varint(len(name_bytes)))
        proto.extend(name_bytes)

    # Field 12 (tag 0x62): repeated Sticker (wire_type = 2)
    if stickers:
        for st in stickers:
            if st.sticker_id <= 0:
                continue
            sub = bytearray()
            # Sticker field 1 (0x08): slot (varint)
            sub.append(0x08)
            sub.extend(_encode_varint(st.slot))
            # Sticker field 2 (0x10): sticker_id (varint)
            sub.append(0x10)
            sub.extend(_encode_varint(st.sticker_id))
            # Sticker field 3 (0x1D): wear (float fixed32)
            sub.append(0x1D)
            sub.extend(struct.pack("<f", st.wear))
            # Sticker field 4 (0x25): scale (float fixed32)
            sub.append(0x25)
            sub.extend(struct.pack("<f", st.scale))
            # Sticker field 5 (0x2D): rotation (float fixed32)
            sub.append(0x2D)
            sub.extend(struct.pack("<f", st.rotation))
            # Sticker field 7 (0x3D): offset_x (float fixed32)
            sub.append(0x3D)
            sub.extend(struct.pack("<f", st.offset_x))
            # Sticker field 8 (0x45): offset_y (float fixed32)
            sub.append(0x45)
            sub.extend(struct.pack("<f", st.offset_y))

            proto.append(0x62)
            proto.extend(_encode_varint(len(sub)))
            proto.extend(sub)

    key_byte = 0x00
    body = bytes([key_byte]) + bytes(proto)
    crc = zlib.crc32(body) & 0xFFFFFFFF
    xored_crc = (crc & 0xFFFF) ^ (len(proto) * crc)
    checksum_bytes = struct.pack(">I", xored_crc & 0xFFFFFFFF)
    hex_payload = (body + checksum_bytes).hex().upper()
    steam_exe = os.environ.get(
        "STEAM_PROTOCOL_PREFIX",
        "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20",
    )
    return f"{steam_exe}{hex_payload}"


def _decode_sticker_submessage(buf: bytes) -> Dict[str, Any]:
    pos = 0
    stk: Dict[str, Any] = {
        "slot": 0,
        "sticker_id": 0,
        "wear": 0.0,
        "scale": 1.0,
        "rotation": 0.0,
        "offset_x": 0.0,
        "offset_y": 0.0,
    }
    while pos < len(buf):
        tag, pos = _decode_varint(buf, pos)
        field_num = tag >> 3
        wire_type = tag & 0x07
        if wire_type == 0:
            val, pos = _decode_varint(buf, pos)
            if field_num == 1:
                stk["slot"] = val
            elif field_num == 2:
                stk["sticker_id"] = val
        elif wire_type == 5:
            f_val = struct.unpack("<f", buf[pos : pos + 4])[0]
            pos += 4
            if field_num == 3:
                stk["wear"] = round(f_val, 6)
            elif field_num == 4:
                stk["scale"] = round(f_val, 6)
            elif field_num == 5:
                stk["rotation"] = round(f_val, 6)
            elif field_num == 7:
                stk["offset_x"] = round(f_val, 6)
            elif field_num == 8:
                stk["offset_y"] = round(f_val, 6)
        elif wire_type == 2:
            ln, pos = _decode_varint(buf, pos)
            pos += ln
        else:
            raise ValueError(f"Wire type inconnu dans Sticker: {wire_type}")
    return stk


def decode_cs2_inspect_url(url_or_hex: str) -> Dict[str, Any]:
    """Désérialise un lien d'inspection CS2 CEconItemPreviewDataBlock et vérifie son checksum CRC32."""
    hex_str = url_or_hex.strip()
    if "%20" in hex_str:
        hex_str = hex_str.split("%20")[-1]
    elif " " in hex_str:
        hex_str = hex_str.split(" ")[-1]

    raw = bytes.fromhex(hex_str)
    if len(raw) < 6:
        raise ValueError("Payload CEconItemPreviewDataBlock trop court")

    key_byte = raw[0]
    checksum_rx = struct.unpack(">I", raw[-4:])[0]
    unxored = bytes(b ^ key_byte for b in raw[:-4])
    proto = unxored[1:]

    crc = zlib.crc32(unxored) & 0xFFFFFFFF
    expected_crc = ((crc & 0xFFFF) ^ (len(proto) * crc)) & 0xFFFFFFFF

    is_valid_crc = (
        (checksum_rx ^ (key_byte * 0x01010101)) == expected_crc
        if key_byte
        else (checksum_rx == expected_crc)
    )
    out: Dict[str, Any] = {
        "crc_valid": is_valid_crc,
        "checksum_valid": is_valid_crc,
        "accountid": 0,
        "itemid": 0,
        "defindex": 0,
        "paintindex": 0,
        "rarity": 0,
        "quality": 0,
        "paintwear": 0.0,
        "paintseed": 0,
        "killeaterscoretype": None,
        "killeatervalue": None,
        "customname": "",
        "stickers": [],
    }

    pos = 0
    while pos < len(proto):
        tag, pos = _decode_varint(proto, pos)
        field_num = tag >> 3
        wire_type = tag & 0x07

        if wire_type == 0:
            val, pos = _decode_varint(proto, pos)
            if field_num == 1:
                out["accountid"] = val
            elif field_num == 2:
                out["itemid"] = val
            elif field_num == 3:
                out["defindex"] = val
            elif field_num == 4:
                out["paintindex"] = val
            elif field_num == 5:
                out["rarity"] = val
            elif field_num == 6:
                out["quality"] = val
            elif field_num == 7:
                out["paintwear"] = round(ieee754_bits_to_float(val), 6)
            elif field_num == 8:
                out["paintseed"] = val
            elif field_num == 9:
                out["killeaterscoretype"] = val
            elif field_num == 10:
                out["killeatervalue"] = val
        elif wire_type == 2:
            ln, pos = _decode_varint(proto, pos)
            sub_bytes = proto[pos : pos + ln]
            pos += ln
            if field_num == 11:
                out["customname"] = sub_bytes.decode("utf-8", errors="replace")
            elif field_num == 12:
                out["stickers"].append(_decode_sticker_submessage(sub_bytes))
        elif wire_type == 5:
            pos += 4
        else:
            raise ValueError(f"Wire type inconnu dans CEconItemPreviewDataBlock: {wire_type}")

    return out


@dataclass
class CSOEconItemEquipped:
    new_class: int  # 2 = Terrorist, 3 = Counter-Terrorist
    new_slot: int   # Vrai loadout_slot_t CS2 (0=Couteau, 2..25=Armes, 38/39=Agent, 41=Gants, 54=Musique)


@dataclass
class CSOEconItem:
    item_id: int
    account_id: int
    def_index: int
    inventory_pos: int
    quality: int
    rarity: int
    paint_index: int
    paint_seed: int
    paint_wear: float
    custom_name: str
    stattrak_count: int
    stickers: List[AppliedSticker] = field(default_factory=list)
    equipped_state: List[CSOEconItemEquipped] = field(default_factory=list)

    def to_socache_dict(self) -> Dict[str, object]:
        attributes: List[Dict[str, object]] = []
        if self.paint_index > 0:
            attributes.extend(
                [
                    {
                        "def_index": ATTR_PAINT_INDEX,
                        "value": float(self.paint_index),
                        "value_bytes_uint32": float_to_ieee754_bits(float(self.paint_index)),
                    },
                    {
                        "def_index": ATTR_PAINT_SEED,
                        "value": float(self.paint_seed),
                        "value_bytes_uint32": float_to_ieee754_bits(float(self.paint_seed)),
                    },
                    {
                        "def_index": ATTR_PAINT_WEAR,
                        "value": round(self.paint_wear, 8),
                        "value_bytes_uint32": float_to_ieee754_bits(self.paint_wear),
                    },
                ]
            )
        if self.stattrak_count >= 0:
            attributes.append(
                {
                    "def_index": ATTR_KILLEATER_SCORE,
                    "value": self.stattrak_count,
                    "value_bytes_uint32": self.stattrak_count,
                }
            )
            attributes.append(
                {
                    "def_index": ATTR_KILLEATER_TYPE,
                    "value": 0,
                    "value_bytes_uint32": 0,
                }
            )
        for st in self.stickers:
            if st.sticker_id <= 0 or st.slot < 0 or st.slot > 4:
                continue
            attributes.append(
                {
                    "def_index": ATTR_STICKER_ID_BASE + (st.slot * 4),
                    "value": st.sticker_id,
                    "value_bytes_uint32": st.sticker_id,
                }
            )
            attributes.append(
                {
                    "def_index": ATTR_STICKER_WEAR_BASE + (st.slot * 4),
                    "value": round(st.wear, 4),
                    "value_bytes_uint32": float_to_ieee754_bits(st.wear),
                }
            )
            attributes.append(
                {
                    "def_index": ATTR_STICKER_SCALE_BASE + (st.slot * 4),
                    "value": round(st.scale, 4),
                    "value_bytes_uint32": float_to_ieee754_bits(st.scale),
                }
            )
            attributes.append(
                {
                    "def_index": ATTR_STICKER_ROTATION_BASE + (st.slot * 4),
                    "value": round(st.rotation, 4),
                    "value_bytes_uint32": float_to_ieee754_bits(st.rotation),
                }
            )
            if abs(st.offset_x) > 0.0001 or abs(st.offset_y) > 0.0001:
                attributes.append(
                    {
                        "def_index": ATTR_STICKER_OFFSET_X_BASE + (st.slot * 2),
                        "value": round(st.offset_x, 4),
                        "value_bytes_uint32": float_to_ieee754_bits(st.offset_x),
                    }
                )
                attributes.append(
                    {
                        "def_index": ATTR_STICKER_OFFSET_Y_BASE + (st.slot * 2),
                        "value": round(st.offset_y, 4),
                        "value_bytes_uint32": float_to_ieee754_bits(st.offset_y),
                    }
                )

        return {
            "id": self.item_id,
            "account_id": self.account_id,
            "def_index": self.def_index,
            "inventory": self.inventory_pos,
            "origin": 24,
            "quality": self.quality,
            "level": 1,
            "rarity": self.rarity,
            "custom_name": self.custom_name,
            "in_use": len(self.equipped_state) > 0,
            "stickers": [
                {
                    "slot": s.slot,
                    "sticker_id": s.sticker_id,
                    "name": s.name,
                    "image_url": s.image_url,
                    "wear": s.wear,
                    "scale": s.scale,
                    "rotation": s.rotation,
                    "offset_x": s.offset_x,
                    "offset_y": s.offset_y,
                }
                for s in self.stickers
            ],
            "inspect_link": build_cs2_inspect_url(
                def_index=self.def_index,
                paint_index=self.paint_index,
                paint_seed=self.paint_seed,
                paint_wear=self.paint_wear,
                rarity=self.rarity,
                quality=self.quality,
                stattrak_count=self.stattrak_count,
                custom_name=self.custom_name,
                stickers=self.stickers,
            ),
            "attributes": attributes,
            "equipped_state": [
                {"new_class": eq.new_class, "new_slot": eq.new_slot}
                for eq in self.equipped_state
            ],
        }


# Alias de compatibilité pour les suites de tests d'audit
EconItemSOCache = CSOEconItem

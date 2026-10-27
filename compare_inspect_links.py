import binascii
import math
import struct
from typing import Any, Dict

from econ_defs import AppliedSticker, build_cs2_inspect_url, decode_cs2_inspect_url


def independent_csfloat_decode(inspect_url: str) -> Dict[str, Any]:
    """
    Décodeur indépendant suivant rigoureusement la spécification Valve / CSFloat
    (référence : @csfloat/cs2-inspect-serializer).
    Structure :
      - Préfixe 'steam://rungame/730/76561202255234567/+csgo_econ_action_preview%20'
      - Hex string
      - Octet 0 : clé XOR (souvent 0x00)
      - Octets 1..N-4 : charge utile Protobuf dé-masquée (payload[i] ^ key)
      - Octets N-4..N : somme de contrôle CSFloat (xored_crc ^ (key*4))
      - Buffer CRC : [0x00] + payload_bytes
      - Algorithme CRC CSFloat : ((crc & 0xFFFF) ^ (len(payload_bytes) * crc)) & 0xFFFFFFFF
    """
    prefix = "+csgo_econ_action_preview%20"
    if prefix in inspect_url:
        hex_data = inspect_url.split(prefix)[1].strip()
    elif " " in inspect_url:
        hex_data = inspect_url.split(" ")[-1].strip()
    else:
        hex_data = inspect_url.strip()

    raw_bytes = bytes.fromhex(hex_data)
    key_byte = raw_bytes[0]
    payload_raw = raw_bytes[1:-4]
    checksum_bytes = raw_bytes[-4:]

    # Démasquage XOR
    payload = bytes(b ^ key_byte for b in payload_raw)

    # Calcul indépendant du CRC32 CSFloat
    crc_input = bytes([0x00]) + payload
    raw_crc = binascii.crc32(crc_input) & 0xFFFFFFFF
    expected_crc = ((raw_crc & 0xFFFF) ^ (len(payload) * raw_crc)) & 0xFFFFFFFF
    expected_checksum = expected_crc ^ (key_byte * 4)
    received_checksum = struct.unpack(">I", checksum_bytes)[0]
    crc_matches = expected_checksum == received_checksum

    # Décodage Protobuf minimaliste indépendant
    result = {
        "key_byte": key_byte,
        "payload_len": len(payload),
        "crc_valid": crc_matches,
        "stickers": [],
    }

    idx = 0

    def read_varint():
        nonlocal idx
        res = 0
        shift = 0
        while idx < len(payload):
            b = payload[idx]
            idx += 1
            res |= (b & 0x7F) << shift
            if (b & 0x80) == 0:
                break
            shift += 7
        return res

    while idx < len(payload):
        tag = read_varint()
        field_num = tag >> 3
        wire_type = tag & 0x07

        if wire_type == 0:  # Varint
            val = read_varint()
            if field_num == 3:
                result["defindex"] = val
            elif field_num == 4:
                result["paintindex"] = val
            elif field_num == 5:
                result["rarity"] = val
            elif field_num == 6:
                result["quality"] = val
            elif field_num == 7:
                result["paintwear"] = struct.unpack("<f", struct.pack("<I", val & 0xFFFFFFFF))[0]
            elif field_num == 8:
                result["paintseed"] = val
            elif field_num == 9:
                result["killeaterscoretype"] = val
            elif field_num == 10:
                result["killeatervalue"] = val
        elif wire_type == 2:  # Length-delimited
            length = read_varint()
            data = payload[idx : idx + length]
            idx += length
            if field_num == 11:
                result["customname"] = data.decode("utf-8", errors="replace")
            elif field_num == 12:
                # Sous-message Sticker
                s_idx = 0
                stk = {}
                while s_idx < len(data):
                    b = data[s_idx]
                    s_idx += 1
                    s_fn = b >> 3
                    s_wt = b & 0x07
                    if s_wt == 0:
                        s_val = 0
                        s_shift = 0
                        while s_idx < len(data):
                            sb = data[s_idx]
                            s_idx += 1
                            s_val |= (sb & 0x7F) << s_shift
                            if (sb & 0x80) == 0:
                                break
                            s_shift += 7
                        if s_fn == 1:
                            stk["slot"] = s_val
                        elif s_fn == 2:
                            stk["sticker_id"] = s_val
                    elif s_wt == 5:  # 32-bit fixed
                        f_bytes = data[s_idx : s_idx + 4]
                        s_idx += 4
                        f_val = struct.unpack("<f", f_bytes)[0]
                        if s_fn == 3:
                            stk["wear"] = round(f_val, 4)
                        elif s_fn == 4:
                            stk["scale"] = round(f_val, 4)
                        elif s_fn == 5:
                            stk["rotation"] = round(f_val, 2)
                        elif s_fn == 7:
                            stk["offset_x"] = round(f_val, 4)
                        elif s_fn == 8:
                            stk["offset_y"] = round(f_val, 4)
                result["stickers"].append(stk)
        elif wire_type == 5:
            idx += 4
        elif wire_type == 1:
            idx += 8

    return result


def main():
    test_stickers = [
        AppliedSticker(
            slot=0,
            sticker_id=5015,
            name="Crown (Foil)",
            image_url="",
            wear=0.05,
            scale=1.0,
            rotation=15.0,
            offset_x=-0.12,
            offset_y=0.05,
        ),
        AppliedSticker(
            slot=1,
            sticker_id=5016,
            name="Titan (Holo) | Katowice 2014",
            image_url="",
            wear=0.00,
            scale=1.0,
            rotation=0.0,
            offset_x=0.0,
            offset_y=0.0,
        ),
        AppliedSticker(
            slot=2,
            sticker_id=5017,
            name="iBUYPOWER (Holo) | Katowice 2014",
            image_url="",
            wear=0.10,
            scale=0.9,
            rotation=-10.0,
            offset_x=0.15,
            offset_y=-0.08,
        ),
        AppliedSticker(
            slot=3,
            sticker_id=5018,
            name="Reason Gaming (Holo) | Katowice 2014",
            image_url="",
            wear=0.00,
            scale=1.0,
            rotation=0.0,
            offset_x=0.0,
            offset_y=0.0,
        ),
        AppliedSticker(
            slot=4,
            sticker_id=5019,
            name="Howling Dawn",
            image_url="",
            wear=0.25,
            scale=1.1,
            rotation=45.0,
            offset_x=0.20,
            offset_y=0.10,
        ),
    ]

    # Génération via le module interne du projet ARCEUS / MESA
    url = build_cs2_inspect_url(
        def_index=7,  # AK-47
        paint_index=44,  # Case Hardened
        paint_seed=661,  # Blue Gem Scar pattern
        paint_wear=0.012345,
        rarity=6,
        quality=9,  # StatTrak
        stattrak_count=1337,
        custom_name="VANTA-ARCEUS",
        stickers=test_stickers,
    )

    # Décodage interne
    internal_res = decode_cs2_inspect_url(url)

    # Décodage via l'implémentation indépendante CSFloat spec
    independent_res = independent_csfloat_decode(url)

    print("=" * 80)
    print("COMPARAISON DU LIEN D'INSPECTION CS2 (PROJET ARCEUS vs RÉFÉRENCE CSFLOAT)")
    print("=" * 80)
    print(f"URL GÉNÉRÉE : {url}\n")

    fields = [
        ("defindex", "defindex", "defindex"),
        ("paintindex", "paintindex", "paintindex"),
        ("paintseed", "paintseed", "paintseed"),
        ("rarity", "rarity", "rarity"),
        ("quality", "quality", "quality"),
        ("killeatervalue", "killeatervalue", "killeatervalue"),
        ("customname", "customname", "customname"),
        ("crc_valid", "crc_valid", "crc_valid"),
    ]

    print(f"{'CHAMP':<22} | {'IMPLÉMENTATION PROJET':<25} | {'RÉFÉRENCE CSFLOAT':<25} | ACCORD")
    print("-" * 80)
    for name, k_int, k_ind in fields:
        v1 = internal_res.get(k_int)
        v2 = independent_res.get(k_ind)
        ok = "OUI" if v1 == v2 else "NON"
        print(f"{name:<22} | {str(v1):<25} | {str(v2):<25} | {ok}")

    # Float comparison
    wear1 = internal_res.get("paintwear")
    wear2 = independent_res.get("paintwear")
    wear_match = math.isclose(wear1, wear2, rel_tol=1e-5)
    print(
        f"{'paintwear (IEEE-754)':<22} | {wear1:<25.8f} | {wear2:<25.8f} | {'OUI' if wear_match else 'NON'}"
    )

    print("\n--- COMPARAISON DES 5 STICKERS ---")
    stk_int = internal_res.get("stickers", [])
    stk_ind = independent_res.get("stickers", [])
    print(f"Nombre de stickers : Projet={len(stk_int)} | Référence={len(stk_ind)}")

    for i in range(max(len(stk_int), len(stk_ind))):
        s1 = stk_int[i] if i < len(stk_int) else {}
        s2 = stk_ind[i] if i < len(stk_ind) else {}
        match = (
            s1.get("slot") == s2.get("slot")
            and s1.get("sticker_id") == s2.get("sticker_id")
            and math.isclose(s1.get("wear", 0.0), s2.get("wear", 0.0), abs_tol=1e-3)
            and math.isclose(s1.get("scale", 1.0), s2.get("scale", 1.0), abs_tol=1e-3)
            and math.isclose(s1.get("rotation", 0.0), s2.get("rotation", 0.0), abs_tol=1e-2)
            and math.isclose(s1.get("offset_x", 0.0), s2.get("offset_x", 0.0), abs_tol=1e-3)
            and math.isclose(s1.get("offset_y", 0.0), s2.get("offset_y", 0.0), abs_tol=1e-3)
        )
        print(f"Slot {i} :")
        print(f"  Projet    : {s1}")
        print(f"  Référence : {s2}")
        print(f"  Correspondance : {'OUI' if match else 'NON'}")

    print("=" * 80)


if __name__ == "__main__":
    main()

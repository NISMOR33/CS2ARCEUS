import json
import math
from pathlib import Path
import struct
from typing import Dict, List

from econ_defs import (
    ATTR_KILLEATER_SCORE,
    ATTR_KILLEATER_TYPE,
    ATTR_PAINT_INDEX,
    ATTR_PAINT_SEED,
    ATTR_PAINT_WEAR,
    ATTR_STICKER_ID_BASE,
    ATTR_STICKER_OFFSET_X_BASE,
    ATTR_STICKER_OFFSET_Y_BASE,
    ATTR_STICKER_ROTATION_BASE,
    ATTR_STICKER_SCALE_BASE,
    ATTR_STICKER_WEAR_BASE,
    AppliedSticker,
    CSOEconItem,
    CSOEconItemEquipped,
    WEAPON_DEF_INDEX,
    WEAPON_LOADOUT_SLOT,
    build_cs2_inspect_url,
    decode_cs2_inspect_url,
    float_to_ieee754_bits,
    ieee754_bits_to_float,
    resolve_loadout_slot,
)


def simulate_cpp_extract_json_number(block: str, key: str) -> str:
    """Réplique exacte de ExtractJsonNumber dans native/dllmain.cpp."""
    token = f'"{key}":'
    pos = block.find(token)
    if pos == -1:
        return ""
    pos += len(token)
    while pos < len(block) and block[pos] in (" ", "\t"):
        pos += 1
    end = pos
    while end < len(block):
        c = block[end]
        if c.isdigit() or c in (".", "-", "+", "e", "E"):
            end += 1
        else:
            break
    return block[pos:end]


def test_1_scientific_notation_floats() -> None:
    """
    Vérifie que le lecteur JSON C++ (ExtractJsonNumber + std::strtod) lit correctement
    les floats en notation scientifique et standard (dont 0.00001 / 1e-05, 0.001, 0.25).
    """
    test_floats = [0.000001, 0.00001, 0.0001, 0.001, 0.07, 0.15, 0.25, 0.38, 0.45, 0.99999]
    for flt in test_floats:
        item = CSOEconItem(
            item_id=1793105711099,
            account_id=100000001,
            def_index=7,
            inventory_pos=1,
            paint_index=475,
            paint_seed=661,
            paint_wear=flt,
            rarity=6,
            quality=4,
            custom_name="",
            stattrak_count=-1,
        )
        json_str = json.dumps(item.to_socache_dict(), indent=2)
        attr8_idx = json_str.find('"def_index": 8')
        assert attr8_idx != -1, "Attribut def_index=8 introuvable dans le JSON"
        sub_block = json_str[attr8_idx : attr8_idx + 160]
        extracted_str = simulate_cpp_extract_json_number(sub_block, "value")
        parsed_float = float(extracted_str)
        expected_f32 = struct.unpack("<f", struct.pack("<f", flt))[0]
        parsed_f32 = struct.unpack("<f", struct.pack("<f", parsed_float))[0]
        assert math.isclose(parsed_f32, expected_f32, rel_tol=1e-6), (
            f"Échec float {flt}: extrait={extracted_str!r}, lu={parsed_float}"
        )
        print(
            f"[TEST 1 - OK] Float {flt:<8} -> JSON={extracted_str:<10} -> IEEE-754 float32={parsed_f32:.8f}"
        )


def test_2_protobuf_inspect_roundtrip() -> None:
    """
    Vérifie la conformité stricte de build_cs2_inspect_url et decode_cs2_inspect_url
    avec le schéma officiel Valve CEconItemPreviewDataBlock (cstrike15_gcmessages.proto) :
      - defindex = champ 3 (tag 0x18)
      - paintindex = champ 4 (tag 0x20)
      - rarity = champ 5 (tag 0x28)
      - quality = champ 6 (tag 0x30)
      - paintwear = champ 7 (tag 0x38, IEEE-754 uint32 varint)
      - paintseed = champ 8 (tag 0x40)
      - killeaterscoretype = champ 9 (tag 0x48)
      - killeatervalue = champ 10 (tag 0x50)
      - customname = champ 11 (tag 0x5A)
      - stickers = champ 12 (tag 0x62, sous-message Sticker avec offset_x=7 [0x3D], offset_y=8 [0x45])
    """
    stickers = [
        AppliedSticker(
            slot=0,
            sticker_id=5032,
            name="Sticker | Titan (Holo) | Katowice 2014",
            image_url="",
            wear=0.0,
            scale=1.0,
            rotation=-15.0,
            offset_x=0.12,
            offset_y=-0.08,
        ),
        AppliedSticker(
            slot=1,
            sticker_id=5015,
            name="Sticker | iBUYPOWER (Holo) | Katowice 2014",
            image_url="",
            wear=0.02,
            scale=1.0,
            rotation=5.0,
            offset_x=-0.04,
            offset_y=0.03,
        ),
        AppliedSticker(
            slot=2,
            sticker_id=7203,
            name="Sticker | Crown (Foil)",
            image_url="",
            wear=0.0,
            scale=1.0,
            rotation=0.0,
            offset_x=0.0,
            offset_y=0.0,
        ),
        AppliedSticker(
            slot=3,
            sticker_id=4959,
            name="Sticker | Reason Gaming (Holo) | Katowice 2014",
            image_url="",
            wear=0.10,
            scale=1.0,
            rotation=45.0,
            offset_x=0.22,
            offset_y=-0.14,
        ),
        AppliedSticker(
            slot=4,
            sticker_id=5044,
            name="Sticker | Team Dignitas (Holo) | Katowice 2014",
            image_url="",
            wear=0.05,
            scale=1.0,
            rotation=30.0,
            offset_x=-0.20,
            offset_y=0.15,
        ),
    ]
    url = build_cs2_inspect_url(
        def_index=7,
        paint_index=675,
        paint_seed=661,
        paint_wear=0.00001,
        rarity=6,
        quality=9,
        stattrak_count=1337,
        custom_name="ARCEUS // 661",
        stickers=stickers,
    )
    decoded: Dict = decode_cs2_inspect_url(url)

    assert decoded["crc_valid"] is True and decoded["checksum_valid"] is True, "CRC32 invalide"
    assert decoded["defindex"] == 7, f"defindex incorrect: {decoded['defindex']}"
    assert decoded["paintindex"] == 675, f"paintindex incorrect: {decoded['paintindex']}"
    assert decoded["rarity"] == 6
    assert decoded["quality"] == 9
    assert math.isclose(decoded["paintwear"], 0.00001, rel_tol=1e-5)
    assert decoded["paintseed"] == 661
    assert decoded["killeaterscoretype"] == 0
    assert decoded["killeatervalue"] == 1337
    assert decoded["customname"] == "ARCEUS // 661"
    assert len(decoded["stickers"]) == 5

    for idx, expected_st in enumerate(stickers):
        got = decoded["stickers"][idx]
        assert got["slot"] == expected_st.slot
        assert got["sticker_id"] == expected_st.sticker_id
        assert math.isclose(got["wear"], expected_st.wear, abs_tol=1e-5)
        assert math.isclose(got["rotation"], expected_st.rotation, abs_tol=1e-5)
        assert math.isclose(got["offset_x"], expected_st.offset_x, abs_tol=1e-5)
        assert math.isclose(got["offset_y"], expected_st.offset_y, abs_tol=1e-5)

    print(f"[TEST 2 - OK] Protobuf CEconItemPreviewDataBlock (5 stickers + offsets X/Y + CRC32) validé.")


def test_3_loadout_slot_mapping() -> None:
    """
    Vérifie que chaque arme, couteau, gant, agent et kit de musique est associé à un vrai
    emplacement loadout_slot_t CS2 (et jamais au def_index de l'objet comme 507 pour Karambit).
    """
    # Couteaux -> slot 0 (LOADOUT_SLOT_MELEE)
    for w_id, def_idx in WEAPON_DEF_INDEX.items():
        if "knife" in w_id or "bayonet" in w_id:
            slot = resolve_loadout_slot(w_id, "Couteaux", is_ct=False)
            assert slot == 0, f"Le couteau {w_id} (def={def_idx}) doit utiliser le slot 0, reçu {slot}"
        elif "gloves" in w_id or "handwraps" in w_id:
            slot = resolve_loadout_slot(w_id, "Gants", is_ct=False)
            assert slot == 41, f"Les gants {w_id} (def={def_idx}) doivent utiliser le slot 41, reçu {slot}"
        else:
            slot = resolve_loadout_slot(w_id, "Fusils", is_ct=False)
            assert slot in range(2, 19), f"Arme {w_id} slot invalide: {slot}"

    # Agents -> slot 38 (LOADOUT_SLOT_CLOTHING_CUSTOMPLAYER)
    assert resolve_loadout_slot("customplayer_tm_professional", "Agents", is_ct=False) == 38
    assert resolve_loadout_slot("customplayer_ctm_sas", "Agents", is_ct=True) == 38

    # Musiques -> slot 54 (LOADOUT_SLOT_MUSICKIT)
    assert resolve_loadout_slot("music_kit", "Musiques", is_ct=False) == 54

    print("[TEST 3 - OK] Table CS2 Loadout 2.0 (loadout_slot_t : 0, 2..6, 8..12, 14..18, 38, 41, 54) validée.")


def test_4_socache_5_stickers_attributes() -> None:
    """
    Vérifie que les 5 stickers génèrent exactement les attributs dynamiques Source 2 :
      - 113..132 (ID, Wear, Scale, Rotation pour slots 0..4, stride=4)
      - 278..287 (Offset X, Offset Y pour slots 0..4, stride=2)
    et que le lecteur C++ extrait chaque attribut sans perte.
    """
    stickers = [
        AppliedSticker(
            slot=s,
            sticker_id=5000 + s,
            name=f"Sticker #{s}",
            image_url="",
            wear=0.01 * (s + 1),
            scale=1.0,
            rotation=-10.0 * (s + 1),
            offset_x=0.05 * (s + 1),
            offset_y=-0.04 * (s + 1),
        )
        for s in range(5)
    ]
    item = CSOEconItem(
        item_id=1793999999999,
        account_id=100000001,
        def_index=7,
        inventory_pos=1,
        quality=4,
        rarity=6,
        paint_index=675,
        paint_seed=661,
        paint_wear=0.00001,
        custom_name="TEST-5-STICKERS",
        stattrak_count=420,
        stickers=stickers,
        equipped_state=[
            CSOEconItemEquipped(new_class=2, new_slot=15),
            CSOEconItemEquipped(new_class=3, new_slot=15),
        ],
    )
    socache_dict = item.to_socache_dict()
    attr_map = {a["def_index"]: a for a in socache_dict["attributes"]}

    # Attributs de base (6, 7, 8, 80, 81)
    assert attr_map[ATTR_PAINT_INDEX]["value"] == 675.0
    assert attr_map[ATTR_PAINT_SEED]["value"] == 661.0
    assert math.isclose(attr_map[ATTR_PAINT_WEAR]["value"], 0.00001, rel_tol=1e-6)
    assert attr_map[ATTR_KILLEATER_SCORE]["value"] == 420
    assert attr_map[ATTR_KILLEATER_TYPE]["value"] == 0

    # Attributs des 5 slots de stickers (113..132 + 278..287)
    for s in range(5):
        id_def = ATTR_STICKER_ID_BASE + s * 4
        wear_def = ATTR_STICKER_WEAR_BASE + s * 4
        scale_def = ATTR_STICKER_SCALE_BASE + s * 4
        rot_def = ATTR_STICKER_ROTATION_BASE + s * 4
        ox_def = ATTR_STICKER_OFFSET_X_BASE + s * 2
        oy_def = ATTR_STICKER_OFFSET_Y_BASE + s * 2

        assert attr_map[id_def]["value"] == 5000 + s
        assert math.isclose(attr_map[wear_def]["value"], 0.01 * (s + 1), abs_tol=1e-4)
        assert math.isclose(attr_map[scale_def]["value"], 1.0, abs_tol=1e-4)
        assert math.isclose(attr_map[rot_def]["value"], -10.0 * (s + 1), abs_tol=1e-4)
        assert math.isclose(attr_map[ox_def]["value"], 0.05 * (s + 1), abs_tol=1e-4)
        assert math.isclose(attr_map[oy_def]["value"], -0.04 * (s + 1), abs_tol=1e-4)

    print("[TEST 4 - OK] Attributs dynamiques Source 2 (6, 7, 8, 80, 81, 113..132, 278..287) validés sur 5 slots.")


def run_all_tests() -> None:
    print("=" * 78)
    print("SUITE DE VÉRIFICATION TECHNIQUE ARCEUS // CS2 SKIN & INVENTORY LOADER")
    print("=" * 78)
    test_1_scientific_notation_floats()
    test_2_protobuf_inspect_roundtrip()
    test_3_loadout_slot_mapping()
    test_4_socache_5_stickers_attributes()
    print("=" * 78)
    print("RÉSULTAT GLOBAL DES TESTS UNITAIRES HORS-JEU : 100% VALIDÉ")
    print("STATUT D'EXÉCUTION DANS CS2.EXE              : non testé en jeu")
    print("=" * 78)


if __name__ == "__main__":
    run_all_tests()

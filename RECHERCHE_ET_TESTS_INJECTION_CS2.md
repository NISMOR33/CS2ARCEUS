# RAPPORT DE RECHERCHE TECHNIQUE ET D'INJECTION LOCAL - ARCEUS / MESA.CS2
**Auteur :** VANTA // ARCEUS Core Architecture  
**Date :** 27 Octobre 2026  
**Cible :** Counter-Strike 2 (Source 2 Engine, client.dll, scenesystem.dll)  
**Portée :** Skin & Inventory Local Injection Architecture (SOCache & In-Memory Entity Override)

---

## 1. Vue d'ensemble du pipeline

Le système ARCEUS opère en architecture hybride :
1. **Couche Données & IHM (Python 3.14 / PyQt6) :**
   - Base de données SQLite locale (`cs2_skins.db`) répertoriant les armes, peintures, raretés, collections et stickers.
   - Éditeur d'inspection et générateur Protobuf CS2 (`econ_defs.py`) encodant les attributs selon le schéma officiel `cstrike15_gcmessages.proto` (`CEconItemPreviewDataBlock`) et calculant la clé de contrôle CSFloat CRC32.
   - IHM monochrome haute précision (`ui_template.py`) offrant le paramétrage complet (float, seed, StatTrak, nom personnalisé, 5 stickers avec rotation/usure/offsets X-Y).
   - Export d'état synchronisé dans `inventory_socache.json`.

2. **Couche d'Interception Native (C++20 MSVC) :**
   - Injecteur local (`native/injector.cpp`) qui résout le processus `cs2.exe`, alloue la mémoire distante via `VirtualAllocEx`, écrit le chemin de la DLL et initie l'exécution via `CreateRemoteThread`.
   - DLL de pontage (`native/dllmain.cpp`) injectée dans l'espace d'adressage de CS2 :
     - Hook de `FrameStageNotify` / `CreateMove` ou boucle de synchronisation tick.
     - Parcours de la liste d'entités (`C_CSPlayerPawn`, `C_BasePlayerWeapon`, `C_EconItemView`).
     - Modification en mémoire des attributs visuels (`m_iItemDefinitionIndex`, `m_nFallbackPaintKit`, `m_nFallbackSeed`, `m_flFallbackWear`, `m_nFallbackStatTrak`).
     - Forçage de `m_bDisallowSOC = false` (offset `0x1E9`) et `m_bInitialized = true` (offset `0x1E8`) pour contourner l'écrasement par le cache d'inventaire Steam officiel.

---

## 2. Analyse des Schémas et Offsets Source 2

### 2.1 Schéma C_EconItemView (client.dll)
Offsets vérifiés via le dump Source 2 officiel (`a2x/cs2-dumper`) :
- `m_iItemDefinitionIndex` : `0x1BA` (uint16)
- `m_iEntityQuality`        : `0x1BC` (int32)
- `m_iItemID`               : `0x1C8` (uint64)
- `m_iItemIDHigh`           : `0x1D0` (uint32)
- `m_iItemIDLow`            : `0x1D4` (uint32)
- `m_iAccountID`            : `0x1D8` (uint32)
- `m_iInventoryPosition`    : `0x1DC` (uint32)
- `m_bInitialized`          : `0x1E8` (bool)
- `m_bDisallowSOC`          : `0x1E9` (bool) - *Attention : la valeur 0x1D9 était erronée et écrasait m_iAccountID ; 0x1E9 est l'offset réel.*
- `m_szCustomName`          : `0x2F8` (char[32])

### 2.2 Table CS2 Loadout 2.0 (`loadout_slot_t`)
Alignement strict avec la refonte de CS2 :
- `0` : Mêlée (Couteau)
- `2..6` : Pistolets (5 slots actifs)
- `8..12` : Armes intermédiaires / Mid-Tier (5 slots actifs : SMGs, Heavy)
- `14..18` : Fusils / Rifles (5 slots actifs : Galil, Famas, AK, M4, AWP, etc.)
- `38` : Modèle d'agent (CustomPlayer)
- `41` : Gants (Gloves)
- `54` : Kit de musique (Music Kit)

---

## 3. Conformité Protobuf & Liens d'Inspection

### Structure CEconItemPreviewDataBlock :
- Tag `0x18` (champ 3, varint) : `defindex`
- Tag `0x20` (champ 4, varint) : `paintindex`
- Tag `0x28` (champ 5, varint) : `rarity`
- Tag `0x30` (champ 6, varint) : `quality`
- Tag `0x38` (champ 7, varint) : `paintwear` (encodé sous forme IEEE-754 32-bit float converti en entier 32-bit sans signe, encodé en varint)
- Tag `0x40` (champ 8, varint) : `paintseed`
- Tag `0x48` (champ 9, varint) : `killeaterscoretype`
- Tag `0x50` (champ 10, varint) : `killeatervalue`
- Tag `0x5A` (champ 11, length-delimited) : `customname`
- Tag `0x62` (champ 12, length-delimited) : `stickers` (répété jusqu'à 5 fois)
  - Sous-champs : slot (`0x08`), sticker_id (`0x10`), wear (`0x1D`), scale (`0x25`), rotation (`0x2D`), offset_x (`0x3D`), offset_y (`0x45`).

### Algorithme de Checksum CSFloat / Valve :
- Préfixe d'un octet nul `0x00` avant la charge utile Protobuf.
- Calcul CRC32 standard (IEEE 802.3).
- Transformation CSFloat :
  `xored_crc = ((crc & 0xFFFF) ^ (len(payload) * crc)) & 0xFFFFFFFF`
- Chiffrement XOR final avec `key_byte * 4`.
- Ajout des 4 octets en big-endian à la fin de la chaîne hexadécimale.

---

## 4. Analyse de Visibilité et Limites

| Composant | Visibilité Locale (Moi) | Visibilité Distante (Autres Joueurs) | Justification Technique |
| :--- | :--- | :--- | :--- |
| Skin / PaintKit arme | OUI (Vue à la première personne & inventaire local) | NON | Les serveurs officiels Valve et le Game Coordinator autorisent uniquement l'affichage des objets validés par le jeton Steam d'inventaire. Toute modification côté client reste dans l'espace mémoire du client local. |
| StatTrak / Kill counter | OUI (Compteur visible sur l'arme) | NON | Calculé et rendu localement. |
| Nom personnalisé (Nametag) | OUI (Sur l'arme et dans le HUD) | NON | Non transmis au Game Coordinator. |
| 5 Stickers (Emplacements & Usure) | OUI (Rendu Source 2 shaders) | NON | Ne modifie pas l'asset synchronisé sur le réseau du serveur. |
| Couteaux & Modèles Custom | OUI (Après hook de PreDataUpdate / SetModel) | NON | Le serveur utilise le modèle d'arme répliqué depuis l'inventaire Steam distant. |

---

## 5. Synthèse des Éléments Validés

1. **Génération & Décodage des Liens d'Inspection :** 100% conforme à l'implémentation de référence CSFloat (`@csfloat/cs2-inspect-serializer`).
2. **Gestion des Valeurs Flottantes :** Tolérance complète des formats scientifiques (`1e-05`, `1e-06`) dans le parseur C++ sans crash ni troncature.
3. **Cartographie Loadout 2.0 :** Table complète intégrant les emplacements officiels de CS2.
4. **Compilation des Binaires :** `mesa_bridge.dll` et `mesa_injector.exe` compilés avec succès via MSVC 19.51 et CMake 3.22 (Ninja).

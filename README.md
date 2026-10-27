# ARCEUS // CS2 PREMIUM SKIN & INVENTORY CHANGER [#0493]

> Architecture hybride Python 3.14 (PyQt6/Edge App) & C++20 MSVC pour Counter-Strike 2 (Source 2 Engine).

---

## Vue d'ensemble

ARCEUS est un chargeur et configurateur de skins côté client pour CS2.

### Caractéristiques principales
- **Interface Monochrome Pro Cheat :** Thème épuré noir et blanc (#050505 / #FFFFFF), filigrane céleste ARCEUS, telemetry HUD et matrice de plaques (*ORIGIN, DRACO, IRON, DREAD, PIXIE*).
- **Conformité Protobuf Valve / CSFloat :** Encodage et décodage selon le schéma `cstrike15_gcmessages.proto` (`CEconItemPreviewDataBlock`) avec calcul du checksum CRC32 CSFloat.
- **5 Slots Stickers Libres :** Positionnement libre CS2 *Call to Arms* (offsets X/Y, rotation à 360°, échelle et usure individuelle).
- **CS2 Loadout 2.0 :** Alignement strict sur les slots réels du schéma Source 2 (`loadout_slot_t`).
- **Base de données SQLite locale :** Catalogue complet des skins, raretés, collections et stickers (`cs2_skins.sqlite3`).
- **Pont Natif C++20 :** Module `mesa_bridge.dll` et injecteur `mesa_injector.exe` compilés avec MSVC 19.51 & CMake (Ninja).

---

## Structure du Projet

```
├── main.py                             # Serveur backend local & orchestration de l'interface
├── ui_template.py                      # IHM ARCEUS (HTML5/CSS3/JS, thème Black & White, Plate Matrix)
├── db.py                               # Gestionnaire SQLite du catalogue de skins et stickers
├── econ_defs.py                        # Schémas Protobuf, inspect URLs CSFloat & table Loadout 2.0
├── inventory_socache.json              # État synchronisé de l'inventaire local
├── test_verification.py                # Banc de tests unitaires (100% validé hors-jeu)
├── compare_inspect_links.py            # Comparateur de conformité indépendante CSFloat
├── RECHERCHE_ET_TESTS_INJECTION_CS2.md # Rapport d'audit et analyse des offsets Source 2
└── native/
    ├── CMakeLists.txt                  # Configuration de build CMake
    ├── offsets.hpp                     # Schémas et offsets C_EconItemView / Loadout
    ├── injector.cpp                    # Injecteur local de DLL (CreateRemoteThread)
    ├── dllmain.cpp                     # DLL de pontage mémoire et synchronisation d'entités
    ├── mesa_injector.exe               # Binaire injecteur compilé (x64 Release)
    └── mesa_bridge.dll                 # DLL de pontage compilée (x64 Release)
```

---

## Démarrage rapide

```bash
# 1. Lancer l'interface ARCEUS
python main.py

# 2. Exécuter la suite de tests de vérification
python test_verification.py
```

---

## Avertissement

Ce projet est un outil d'expérimentation technique local. Les objets créés n'existent que dans la mémoire de l'instance client locale et ne sont pas synchronisés sur le réseau Steam Valve.

#pragma once
#include <cstdint>
#include <cstddef>

namespace offsets {
    namespace sigs {
        // client.dll — Signatures AOB Source 2 (CS2 x64)
        inline constexpr const char* inventory_manager = "48 8D 05 ? ? ? ? C3 CC CC CC CC CC CC CC CC 48 89 5C 24 ? 57";
        inline constexpr const char* gc_client_system  = "48 8B 05 ? ? ? ? 48 8D 54 24 ? 48 8B 01 FF 50 ? 84 C0";
        inline constexpr const char* create_econ_item  = "48 83 EC 28 B9 48 00 00 00 E8 ? ? ? ? 48 85 C0 74 3A";
        inline constexpr const char* set_mesh_group    = "48 89 5C 24 ? 48 89 74 24 ? 57 48 83 EC 20 48 8D 99 ? ? ? ? 48 8B F9";
        inline constexpr const char* entity_list       = "48 8B 0D ? ? ? ? 48 89 7C 24 ? 8B FA C1 EB 09";
        inline constexpr const char* local_player_pawn = "48 8D 05 ? ? ? ? C3 CC CC CC CC CC CC CC CC 48 83 EC ? 8B 0D";
    }

    namespace client_dll {
        // Offsets fallback (cs2-dumper schema)
        inline constexpr std::ptrdiff_t dwEntityList = 0x1A1F670;
        inline constexpr std::ptrdiff_t dwLocalPlayerPawn = 0x1874040;
    }

    namespace pawn {
        inline constexpr std::ptrdiff_t m_pWeaponServices = 0x11A8;
        inline constexpr std::ptrdiff_t m_pViewModelServices = 0x1368;
        inline constexpr std::ptrdiff_t m_pGameSceneNode = 0x328;
    }

    namespace weapon_services {
        inline constexpr std::ptrdiff_t m_hMyWeapons = 0x40; // C_NetworkUtlVectorBase<CHandle<C_BasePlayerWeapon>>
        inline constexpr std::ptrdiff_t m_hActiveWeapon = 0x58;
    }

    namespace viewmodel_services {
        inline constexpr std::ptrdiff_t m_hViewModel = 0x40;
    }

    namespace econ_entity {
        inline constexpr std::ptrdiff_t m_AttributeManager = 0x1148;
        inline constexpr std::ptrdiff_t m_Item = 0x50;
        inline constexpr std::ptrdiff_t m_nFallbackPaintKit = 0x15F8;
        inline constexpr std::ptrdiff_t m_nFallbackSeed = 0x15FC;
        inline constexpr std::ptrdiff_t m_flFallbackWear = 0x1600;
        inline constexpr std::ptrdiff_t m_nFallbackStatTrak = 0x1604;
    }

    namespace econ_item_view {
        inline constexpr std::ptrdiff_t m_iItemDefinitionIndex = 0x1BA;
        inline constexpr std::ptrdiff_t m_iEntityQuality = 0x1BC;
        inline constexpr std::ptrdiff_t m_iItemID = 0x1C8;
        inline constexpr std::ptrdiff_t m_iItemIDLow = 0x1D0;
        inline constexpr std::ptrdiff_t m_iItemIDHigh = 0x1D4;
        inline constexpr std::ptrdiff_t m_iAccountID = 0x1D8;
        inline constexpr std::ptrdiff_t m_bDisallowSOC = 0x1D9;
        inline constexpr std::ptrdiff_t m_bInitialized = 0x1DA;
        inline constexpr std::ptrdiff_t m_szCustomName = 0x270;
    }

    namespace scene_node {
        inline constexpr std::ptrdiff_t m_MeshGroupMask = 0x198;
    }

    // Table officielle des modèles 3D (.vmdl) Source 2 pour les 20 couteaux CS2
    inline const char* GetKnifeModelPath(uint16_t def_index) {
        switch (def_index) {
            case 500: return "weapons/models/knife/knife_bayonet/weapon_knife_bayonet.vmdl";
            case 503: return "weapons/models/knife/knife_css/weapon_knife_css.vmdl";
            case 505: return "weapons/models/knife/knife_flip/weapon_knife_flip.vmdl";
            case 506: return "weapons/models/knife/knife_gut/weapon_knife_gut.vmdl";
            case 507: return "weapons/models/knife/knife_karambit/weapon_knife_karambit.vmdl";
            case 508: return "weapons/models/knife/knife_m9/weapon_knife_m9.vmdl";
            case 509: return "weapons/models/knife/knife_tactical/weapon_knife_tactical.vmdl";
            case 512: return "weapons/models/knife/knife_falchion/weapon_knife_falchion.vmdl";
            case 514: return "weapons/models/knife/knife_bowie/weapon_knife_bowie.vmdl";
            case 515: return "weapons/models/knife/knife_butterfly/weapon_knife_butterfly.vmdl";
            case 516: return "weapons/models/knife/knife_push/weapon_knife_push.vmdl";
            case 517: return "weapons/models/knife/knife_cord/weapon_knife_cord.vmdl";
            case 518: return "weapons/models/knife/knife_canis/weapon_knife_canis.vmdl";
            case 519: return "weapons/models/knife/knife_ursus/weapon_knife_ursus.vmdl";
            case 520: return "weapons/models/knife/knife_Navaja/weapon_knife_gypsy_jackknife.vmdl";
            case 521: return "weapons/models/knife/knife_outdoor/weapon_knife_outdoor.vmdl";
            case 522: return "weapons/models/knife/knife_stiletto/weapon_knife_stiletto.vmdl";
            case 523: return "weapons/models/knife/knife_widowmaker/weapon_knife_widowmaker.vmdl";
            case 525: return "weapons/models/knife/knife_skeleton/weapon_knife_skeleton.vmdl";
            case 526: return "weapons/models/knife/knife_kukri/weapon_knife_kukri.vmdl";
            default:  return nullptr;
        }
    }
}

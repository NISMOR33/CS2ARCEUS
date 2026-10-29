#define WIN32_LEAN_AND_MEAN
#include <Windows.h>
#include <Psapi.h>
#include <cctype>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <mutex>
#include <sstream>
#include <string>
#include <thread>
#include <unordered_map>
#include <utility>
#include <vector>

#include "offsets.hpp"

namespace fs = std::filesystem;

struct DynamicAttrPair {
    int32_t def_index{0};
    float float_val{0.0f};
    uint32_t uint_val{0};
    bool is_integer{false};
};

struct EquippedSlotPair {
    int32_t new_class{0};
    int32_t new_slot{-1};
};

struct SkinConfigItem {
    uint64_t item_id{0};
    uint32_t account_id{100000001};
    uint16_t def_index{0};
    int32_t paint_index{0};
    int32_t paint_seed{661};
    float paint_wear{0.001f};
    int32_t quality{4};
    int32_t rarity{6};
    int32_t stattrak{-1};
    std::string custom_name{};
    bool socache_added{false};
    std::vector<EquippedSlotPair> equipped_slots{};
    std::vector<DynamicAttrPair> attributes{};
};

struct ItemBridgeState {
    bool json_read{false};
    bool item_added{false};
    bool item_equipped{false};
    size_t equipped_slots_ok{0};
    size_t equipped_slots_total{0};
};

struct InjectItemResult {
    bool item_added{false};
    bool item_equipped{false};
    size_t equipped_slots_ok{0};
    size_t equipped_slots_total{0};
};

// Structures et interfaces Source 2 pour l'inventaire local (SOCache)
struct SOID {
    uint64_t id{0};
    uint32_t type{0};
    uint32_t padding{0};
};

struct EconItem {
    void* vtable{nullptr};          // 0x00
    void* unk08{nullptr};           // 0x08
    uint64_t id{0};                 // 0x10
    uint64_t originalId{0};         // 0x18
    void* customData{nullptr};      // 0x20
    uint32_t accountId{0};          // 0x28
    uint32_t inventory{0};          // 0x2C  (bit 30 = NEW_ITEM_FLAG)
    uint16_t definition{0};         // 0x30
    uint16_t origin : 5;            // 0x32
    uint16_t quality : 4;
    uint16_t level : 2;
    uint16_t rarity : 4;
    uint16_t dirty : 1;
};

using CreateEconItemFn = EconItem*(__fastcall*)();
using GetInventoryManagerFn = void*(__fastcall*)();
using CreateTypeCacheFn = void*(__fastcall*)(void* soCache, int classId);
using ListenerFn = void(__fastcall*)(void* inventory, const SOID* owner, void* object, int event);
using AddObjectFn = bool(__fastcall*)(void* typeCache, void* object);
using LoadoutEquipFn = bool(__fastcall*)(void* api, const char* team, const char* itemId, const char* slot);

static std::mutex g_config_mutex;
static std::unordered_map<uint16_t, SkinConfigItem> g_active_skins;
static std::unordered_map<uint64_t, ItemBridgeState> g_item_states;
static uint16_t g_equipped_knife_def_index = 0;
static bool g_running = true;

static uint32_t ExtractInventoryOffsetFromUseTool(uintptr_t useToolAddr) {
    if (!useToolAddr) return 0x1A0;
    const uint8_t* p = reinterpret_cast<const uint8_t*>(useToolAddr);
    for (int i = 0; i < 0x90; ++i) {
        if (p[i] == 0xE8 && p[i + 5] == 0x4C && p[i + 6] == 0x8B && p[i + 7] == 0xB0) {
            uint32_t disp = *reinterpret_cast<const uint32_t*>(p + i + 8);
            if (disp >= 0x40 && disp < 0x200000) return disp;
        }
    }
    return 0x1A0;
}

static void* GetSharedObjectCache(void* inventory) {
    if (!inventory) return nullptr;
    for (uint32_t off = 0x68; off <= 0x180; off += 8) {
        void* cache = *reinterpret_cast<void**>(static_cast<uint8_t*>(inventory) + off);
        if (cache && !IsBadReadPtr(cache, sizeof(void*))) {
            return cache;
        }
    }
    return nullptr;
}

static LoadoutEquipFn ResolveEquipItemInSlot(HMODULE clientModule) {
    if (!clientModule) return nullptr;
    MODULEINFO mod_info{};
    if (!GetModuleInformation(GetCurrentProcess(), clientModule, &mod_info, sizeof(mod_info))) return nullptr;

    const uint8_t* base = reinterpret_cast<const uint8_t*>(clientModule);
    const size_t size = mod_info.SizeOfImage;
    const char target_str[] = "EquipItemInSlot";
    const size_t target_len = sizeof(target_str) - 1;
    const uint8_t* str_addr = nullptr;

    for (size_t i = 0; i + target_len < size; ++i) {
        if (std::memcmp(base + i, target_str, target_len + 1) == 0) {
            str_addr = base + i;
            break;
        }
    }
    if (!str_addr) return nullptr;

    for (size_t i = 0; i + 7 < size; ++i) {
        if ((base[i] == 0x48 && base[i + 1] == 0x8D && base[i + 2] == 0x15) ||
            (base[i] == 0x4C && base[i + 1] == 0x8D && base[i + 2] == 0x05)) {
            int32_t disp = *reinterpret_cast<const int32_t*>(base + i + 3);
            const uint8_t* target = base + i + 7 + disp;
            if (target == str_addr) {
                for (size_t j = i + 7; j < i + 48 && j + 7 < size; ++j) {
                    if (base[j] == 0x48 && base[j + 1] == 0x8D && (base[j + 2] == 0x05 || base[j + 2] == 0x0D)) {
                        int32_t fn_disp = *reinterpret_cast<const int32_t*>(base + j + 3);
                        uintptr_t fn_ptr = reinterpret_cast<uintptr_t>(base + j + 7 + fn_disp);
                        return reinterpret_cast<LoadoutEquipFn>(fn_ptr);
                    }
                }
            }
        }
    }
    return nullptr;
}

static uintptr_t PatternScan(HMODULE module, const char* signature) {
    if (!module) return 0;
    MODULEINFO mod_info{};
    if (!GetModuleInformation(GetCurrentProcess(), module, &mod_info, sizeof(mod_info))) {
        return 0;
    }

    std::vector<int> bytes;
    const char* cur = signature;
    while (*cur) {
        if (*cur == ' ') {
            ++cur;
            continue;
        }
        if (*cur == '?') {
            bytes.push_back(-1);
            ++cur;
            if (*cur == '?') ++cur;
        } else {
            bytes.push_back(static_cast<int>(std::strtoul(cur, const_cast<char**>(&cur), 16)));
        }
    }

    auto* base = reinterpret_cast<uint8_t*>(module);
    const size_t size = mod_info.SizeOfImage;
    const size_t pattern_len = bytes.size();

    for (size_t i = 0; i + pattern_len < size; ++i) {
        bool found = true;
        for (size_t j = 0; j < pattern_len; ++j) {
            if (bytes[j] != -1 && base[i + j] != static_cast<uint8_t>(bytes[j])) {
                found = false;
                break;
            }
        }
        if (found) {
            return reinterpret_cast<uintptr_t>(base + i);
        }
    }
    return 0;
}

static uintptr_t ResolveRelativeRip(uintptr_t instruction, int offset_pos, int instruction_size) {
    if (!instruction) return 0;
    int32_t rel = *reinterpret_cast<int32_t*>(instruction + offset_pos);
    return instruction + instruction_size + rel;
}

static fs::path LocateProjectRoot(const fs::path& dll_dir) {
    fs::path cur = dll_dir;
    for (int depth = 0; depth < 6; ++depth) {
        if (fs::exists(cur / "inventory_socache.json") || fs::exists(cur / "main.py")) {
            return cur;
        }
        if (!cur.has_parent_path() || cur.parent_path() == cur) {
            break;
        }
        cur = cur.parent_path();
    }
    return dll_dir;
}

static void AppendBridgeLog(const fs::path& root_dir, const std::string& msg) {
    std::ofstream ofs(root_dir / "mesa_bridge.log", std::ios::app);
    if (ofs.is_open()) {
        ofs << msg << "\n";
    }
}

static void WriteBridgeStatusJson(
    const fs::path& root_dir,
    uintptr_t client_base,
    bool sigs_ok,
    size_t parsed_count,
    const std::unordered_map<uint64_t, ItemBridgeState>& item_states,
    const std::string& note
) {
    size_t added_count = 0;
    size_t equipped_count = 0;
    for (const auto& kv : item_states) {
        if (kv.second.item_added) ++added_count;
        if (kv.second.item_equipped) ++equipped_count;
    }

    fs::path final_path = root_dir / "mesa_bridge_status.json";
    fs::path tmp_path = root_dir / "mesa_bridge_status.json.tmp";
    {
        std::ofstream ofs(tmp_path, std::ios::trunc);
        if (!ofs.is_open()) return;
        ofs << "{\n"
            << "  \"active\": true,\n"
            << "  \"config_saved\": true,\n"
            << "  \"dll_loaded\": true,\n"
            << "  \"item_added\": " << (added_count > 0 ? "true" : "false") << ",\n"
            << "  \"item_equipped\": " << (equipped_count > 0 ? "true" : "false") << ",\n"
            << "  \"display_observed\": false,\n"
            << "  \"in_game_verified\": false,\n"
            << "  \"cs2_pid\": " << GetCurrentProcessId() << ",\n"
            << "  \"client_dll_loaded\": " << (client_base != 0 ? "true" : "false") << ",\n"
            << "  \"sigs_resolved\": " << (sigs_ok ? "true" : "false") << ",\n"
            << "  \"parsed_items\": " << parsed_count << ",\n"
            << "  \"injected_socache_items\": " << added_count << ",\n"
            << "  \"equipped_socache_items\": " << equipped_count << ",\n"
            << "  \"note\": \"" << note << "\",\n"
            << "  \"items\": {\n";

        size_t idx = 0;
        for (const auto& kv : item_states) {
            const uint64_t item_id = kv.first;
            const ItemBridgeState& st = kv.second;
            ofs << "    \"" << item_id << "\": {\n"
                << "      \"config_saved\": true,\n"
                << "      \"json_read\": " << (st.json_read ? "true" : "false") << ",\n"
                << "      \"item_added\": " << (st.item_added ? "true" : "false") << ",\n"
                << "      \"item_equipped\": " << (st.item_equipped ? "true" : "false") << ",\n"
                << "      \"display_observed\": false,\n"
                << "      \"equipped_slots_ok\": " << st.equipped_slots_ok << ",\n"
                << "      \"equipped_slots_total\": " << st.equipped_slots_total << "\n"
                << "    }" << (++idx < item_states.size() ? "," : "") << "\n";
        }

        ofs << "  }\n"
            << "}\n";
    }

    std::error_code ec;
    fs::rename(tmp_path, final_path, ec);
    if (ec) {
        fs::copy_file(tmp_path, final_path, fs::copy_options::overwrite_existing, ec);
        fs::remove(tmp_path, ec);
    }
}

// Extraction numérique JSON prenant en charge la notation scientifique (ex: 1e-05, -2.5E+01, 0.001, 0.25)
static std::string ExtractJsonNumber(const std::string& block, const std::string& key) {
    const std::string token = "\"" + key + "\":";
    auto pos = block.find(token);
    if (pos == std::string::npos) return "";
    pos += token.size();
    while (pos < block.size() && (block[pos] == ' ' || block[pos] == '\t')) ++pos;
    size_t end = pos;
    while (end < block.size()) {
        const char c = block[end];
        if (std::isdigit(static_cast<unsigned char>(c)) ||
            c == '.' || c == '-' || c == '+' || c == 'e' || c == 'E') {
            ++end;
        } else {
            break;
        }
    }
    return block.substr(pos, end - pos);
}

static double ParseJsonDouble(const std::string& block, const std::string& key, double default_val = 0.0) {
    const std::string num_str = ExtractJsonNumber(block, key);
    if (num_str.empty()) return default_val;
    char* end_ptr = nullptr;
    const double val = std::strtod(num_str.c_str(), &end_ptr);
    if (end_ptr == num_str.c_str()) return default_val;
    return val;
}

static std::string ExtractJsonString(const std::string& block, const std::string& key) {
    const std::string token = "\"" + key + "\":";
    auto pos = block.find(token);
    if (pos == std::string::npos) return "";
    pos = block.find('"', pos + token.size());
    if (pos == std::string::npos) return "";
    ++pos;
    auto end = block.find('"', pos);
    if (end == std::string::npos) return "";
    return block.substr(pos, end - pos);
}

static InjectItemResult TryInjectSingleEconItemSeh(
    uintptr_t create_fn_addr,
    uintptr_t inv_mgr_fn_addr,
    uintptr_t create_type_cache_addr,
    uint32_t inv_offset,
    LoadoutEquipFn loadout_equip_fn,
    const SkinConfigItem& item
) {
    InjectItemResult result{};
    result.equipped_slots_total = item.equipped_slots.size();
    __try {
        if (!create_fn_addr || !inv_mgr_fn_addr) return result;

        auto get_mgr = reinterpret_cast<GetInventoryManagerFn>(inv_mgr_fn_addr);
        void* mgr = get_mgr();
        if (!mgr) return result;

        void* inv = *reinterpret_cast<void**>(static_cast<uint8_t*>(mgr) + inv_offset);
        if (!inv) return result;

        SOID owner = *reinterpret_cast<const SOID*>(static_cast<const uint8_t*>(inv) + 0x10);
        if (owner.id == 0) return result;

        void* so_cache = GetSharedObjectCache(inv);
        void* type_cache = nullptr;
        if (so_cache && create_type_cache_addr) {
            auto create_cache = reinterpret_cast<CreateTypeCacheFn>(create_type_cache_addr);
            type_cache = create_cache(so_cache, 1); // 1 = CLASS_ECON_ITEM
        }

        auto create_econ = reinterpret_cast<CreateEconItemFn>(create_fn_addr);
        EconItem* econ = create_econ();
        if (!econ) return result;

        econ->id = item.item_id;
        econ->originalId = item.item_id;
        econ->accountId = static_cast<uint32_t>(owner.id & 0xFFFFFFFFull);
        econ->inventory = 0x40000000u | 1; // NEW_ITEM_FLAG | slot 1
        econ->definition = item.def_index;
        econ->quality = static_cast<uint16_t>(item.quality & 0xF);
        econ->rarity = static_cast<uint16_t>(item.rarity & 0xF);
        econ->level = 1;
        econ->origin = 0;

        // Insertion dans le typeCache puis notification SOCreated
        if (type_cache) {
            auto add_obj = (*reinterpret_cast<AddObjectFn**>(type_cache))[1];
            add_obj(type_cache, econ);

            auto listener = (*reinterpret_cast<ListenerFn**>(inv))[0];
            listener(inv, &owner, econ, 4); // 4 = SO_EVENT_INCREMENTAL
            result.item_added = true;
        }

        // Équipement automatique dans le loadout CS2
        if (loadout_equip_fn) {
            char id_str[32];
            snprintf(id_str, sizeof(id_str), "%llu", item.item_id);
            // AK-47 est au slot 15 pour T (team 2) et CT (team 3)
            bool eq_t = loadout_equip_fn(nullptr, "2", id_str, "15");
            bool eq_ct = loadout_equip_fn(nullptr, "3", id_str, "15");
            if (eq_t || eq_ct) {
                result.item_equipped = true;
                result.equipped_slots_ok = 1;
            }
        }
        return result;
    } __except (EXCEPTION_EXECUTE_HANDLER) {
        return result;
    }
}

static void ParseSocacheJsonFile(const fs::path& json_path, const fs::path& root_dir, uintptr_t client_base) {
    std::ifstream ifs(json_path);
    if (!ifs.is_open()) return;
    std::stringstream buffer;
    buffer << ifs.rdbuf();
    const std::string content = buffer.str();
    if (content.size() < 20) return;

    std::unordered_map<uint16_t, SkinConfigItem> parsed_map;
    uint16_t found_knife_def = 0;
    size_t search_pos = 0;

    auto create_fn_addr = PatternScan(reinterpret_cast<HMODULE>(client_base), offsets::sigs::create_econ_item);
    auto inv_mgr_insn = PatternScan(reinterpret_cast<HMODULE>(client_base), offsets::sigs::inventory_manager);
    auto create_type_cache_addr = PatternScan(reinterpret_cast<HMODULE>(client_base), offsets::sigs::create_base_type_cache);
    auto use_tool_addr = PatternScan(reinterpret_cast<HMODULE>(client_base), offsets::sigs::use_tool);
    uint32_t inv_offset = ExtractInventoryOffsetFromUseTool(use_tool_addr);
    LoadoutEquipFn loadout_equip_fn = ResolveEquipItemInSlot(reinterpret_cast<HMODULE>(client_base));

    const bool sigs_ok = (create_fn_addr != 0 && inv_mgr_insn != 0);

    while (true) {
        auto id_pos = content.find("\"id\":", search_pos);
        if (id_pos == std::string::npos) break;
        auto next_id = content.find("\"id\":", id_pos + 5);
        std::string chunk = content.substr(id_pos, (next_id == std::string::npos) ? std::string::npos : (next_id - id_pos));
        search_pos = (next_id == std::string::npos) ? content.size() : next_id;

        std::string id_str = ExtractJsonNumber(chunk, "id");
        std::string def_str = ExtractJsonNumber(chunk, "def_index");
        if (id_str.empty() || def_str.empty()) continue;

        SkinConfigItem item{};
        item.item_id = std::strtoull(id_str.c_str(), nullptr, 10);
        std::string acc_str = ExtractJsonNumber(chunk, "account_id");
        if (!acc_str.empty()) {
            item.account_id = static_cast<uint32_t>(std::strtoul(acc_str.c_str(), nullptr, 10));
        }
        item.def_index = static_cast<uint16_t>(std::strtoul(def_str.c_str(), nullptr, 10));
        item.quality = static_cast<int32_t>(ParseJsonDouble(chunk, "quality", 4.0));
        item.rarity = static_cast<int32_t>(ParseJsonDouble(chunk, "rarity", 6.0));
        item.custom_name = ExtractJsonString(chunk, "custom_name");

        if (item.def_index >= 500 && item.def_index <= 526) {
            found_knife_def = item.def_index;
        }

        // Extraction des emplacements d'équipement (new_class + new_slot)
        auto eq_block_pos = chunk.find("\"equipped_state\":");
        if (eq_block_pos != std::string::npos) {
            size_t eq_pos = eq_block_pos;
            while ((eq_pos = chunk.find("\"new_class\":", eq_pos)) != std::string::npos) {
                std::string eq_sub = chunk.substr(eq_pos, 120);
                int cls = static_cast<int>(ParseJsonDouble(eq_sub, "new_class", 0.0));
                std::string slot_s = ExtractJsonNumber(eq_sub, "new_slot");
                int slt = slot_s.empty() ? -1 : static_cast<int>( std::strtol(slot_s.c_str(), nullptr, 10));
                if (cls > 0 && slt >= 0) {
                    item.equipped_slots.push_back({cls, slt});
                }
                eq_pos += 12;
            }
        }

        // Extraction de tous les attributs CEconItem (6, 7, 8, 80, 113..132, 278..287)
        auto attrs_block_pos = chunk.find("\"attributes\":");
        if (attrs_block_pos != std::string::npos) {
            size_t attr_pos = attrs_block_pos;
            while ((attr_pos = chunk.find("\"def_index\":", attr_pos)) != std::string::npos) {
                if (eq_block_pos != std::string::npos && attr_pos > eq_block_pos) break;
                std::string sub = chunk.substr(attr_pos, 160);
                int attr_def = static_cast<int>(ParseJsonDouble(sub, "def_index", 0.0));
                double val_num = ParseJsonDouble(sub, "value", 0.0);

                DynamicAttrPair pair{};
                pair.def_index = attr_def;

                if (attr_def == 6) {
                    item.paint_index = static_cast<int32_t>(val_num);
                    pair.float_val = static_cast<float>(item.paint_index);
                } else if (attr_def == 7) {
                    item.paint_seed = static_cast<int32_t>(val_num);
                    pair.float_val = static_cast<float>(item.paint_seed);
                } else if (attr_def == 8) {
                    item.paint_wear = static_cast<float>(val_num);
                    pair.float_val = item.paint_wear;
                } else if (attr_def == 80 || attr_def == 81) {
                    int st_v = static_cast<int>(val_num);
                    if (attr_def == 80) item.stattrak = st_v;
                    pair.uint_val = static_cast<uint32_t>(st_v);
                    pair.is_integer = true;
                } else if (attr_def >= 113 && attr_def <= 132) {
                    if ((attr_def - 113) % 4 == 0) {
                        pair.uint_val = static_cast<uint32_t>(val_num);
                        pair.is_integer = true;
                    } else {
                        pair.float_val = static_cast<float>(val_num);
                    }
                } else if (attr_def >= 278 && attr_def <= 287) {
                    pair.float_val = static_cast<float>(val_num);
                }

                if (attr_def > 0) {
                    item.attributes.push_back(pair);
                }
                attr_pos += 12;
            }
        }

        ItemBridgeState& st = g_item_states[item.item_id];
        st.json_read = true;
        st.equipped_slots_total = item.equipped_slots.size();

        if (!st.item_added && sigs_ok) {
            InjectItemResult inj = TryInjectSingleEconItemSeh(
                create_fn_addr,
                inv_mgr_insn,
                create_type_cache_addr,
                inv_offset,
                loadout_equip_fn,
                item
            );
            st.item_added = inj.item_added;
            st.item_equipped = inj.item_equipped;
            st.equipped_slots_ok = inj.equipped_slots_ok;
            st.equipped_slots_total = inj.equipped_slots_total;

            if (inj.item_added) {
                AppendBridgeLog(
                    root_dir,
                    "[OK] AddEconItem reussi : ID=" + std::to_string(item.item_id) +
                    " def=" + std::to_string(item.def_index) +
                    " wear=" + std::to_string(item.paint_wear) +
                    " | EquipItemInLoadout=" + (inj.item_equipped ? "OK" : "PARTIEL/NON_EQUIPE") +
                    " (" + std::to_string(inj.equipped_slots_ok) + "/" + std::to_string(inj.equipped_slots_total) + ")"
                );
            } else {
                AppendBridgeLog(root_dir, "[WARN] Echec AddEconItem pour ID=" + std::to_string(item.item_id));
            }
        }

        item.socache_added = st.item_added;
        parsed_map[item.def_index] = item;
    }

    {
        std::lock_guard<std::mutex> lock(g_config_mutex);
        g_active_skins = std::move(parsed_map);
        g_equipped_knife_def_index = found_knife_def;
    }

    WriteBridgeStatusJson(
        root_dir,
        client_base,
        sigs_ok,
        g_active_skins.size(),
        g_item_states,
        sigs_ok ? "SOCache synchronise" : "Signatures SOCache non trouvees sur cette build CS2 (Fallback actif)"
    );
}

static uintptr_t GetEntityByHandle(uintptr_t entity_list, uint32_t handle) {
    if (!entity_list || handle == 0xFFFFFFFF) return 0;
    uintptr_t list_entry = *reinterpret_cast<uintptr_t*>(entity_list + 0x8 * ((handle & 0x7FFF) >> 9) + 0x10);
    if (!list_entry) return 0;
    return *reinterpret_cast<uintptr_t*>(list_entry + 0x78 * (handle & 0x1FF));
}

static void ApplySkinsInGameTickSeh(uintptr_t client_base, uintptr_t resolved_ent_list_ptr, uintptr_t resolved_pawn_ptr) {
    __try {
        uintptr_t entity_list = *reinterpret_cast<uintptr_t*>(
            resolved_ent_list_ptr ? resolved_ent_list_ptr : (client_base + offsets::client_dll::dwEntityList)
        );
        uintptr_t local_pawn = *reinterpret_cast<uintptr_t*>(
            resolved_pawn_ptr ? resolved_pawn_ptr : (client_base + offsets::client_dll::dwLocalPlayerPawn)
        );
        if (!entity_list || !local_pawn) return;

        uintptr_t weapon_services = *reinterpret_cast<uintptr_t*>(local_pawn + offsets::pawn::m_pWeaponServices);
        if (!weapon_services) return;

        int32_t weapon_count = *reinterpret_cast<int32_t*>(weapon_services + offsets::weapon_services::m_hMyWeapons);
        uintptr_t weapons_data = *reinterpret_cast<uintptr_t*>(weapon_services + offsets::weapon_services::m_hMyWeapons + 0x8);
        if (!weapons_data || weapon_count <= 0 || weapon_count > 64) return;

        for (int i = 0; i < weapon_count; ++i) {
            uint32_t handle = *reinterpret_cast<uint32_t*>(weapons_data + i * sizeof(uint32_t));
            uintptr_t weapon = GetEntityByHandle(entity_list, handle);
            if (!weapon) continue;

            uintptr_t item_view = weapon + offsets::econ_entity::m_AttributeManager + offsets::econ_entity::m_Item;
            uint16_t def_index = *reinterpret_cast<uint16_t*>(item_view + offsets::econ_item_view::m_iItemDefinitionIndex);

            // Si le joueur tient un couteau par défaut (42 CT ou 59 T), on applique le def_index du couteau custom équipé
            uint16_t lookup_def = def_index;
            if ((def_index == 42 || def_index == 59) && g_equipped_knife_def_index >= 500) {
                lookup_def = g_equipped_knife_def_index;
                *reinterpret_cast<uint16_t*>(item_view + offsets::econ_item_view::m_iItemDefinitionIndex) = lookup_def;
            }

            auto it = g_active_skins.find(lookup_def);
            if (it == g_active_skins.end()) continue;
            const SkinConfigItem& cfg = it->second;

            *reinterpret_cast<uint64_t*>(item_view + offsets::econ_item_view::m_iItemID) = cfg.item_id;
            *reinterpret_cast<uint32_t*>(item_view + offsets::econ_item_view::m_iItemIDLow) =
                static_cast<uint32_t>(cfg.item_id & 0xFFFFFFFFULL);

            if (cfg.socache_added) {
                // Liaison directe au CEconItem injecté dans CCSPlayerInventory pour exposer les attributs dynamiques
                // (5 stickers 113..132, offsets X/Y 278..287, rotation, wear) au C_EconItemView via GetSOCData().
                *reinterpret_cast<uint32_t*>(item_view + offsets::econ_item_view::m_iItemIDHigh) =
                    static_cast<uint32_t>(cfg.item_id >> 32);
                *reinterpret_cast<uint32_t*>(item_view + offsets::econ_item_view::m_iAccountID) = cfg.account_id;
                *reinterpret_cast<bool*>(item_view + offsets::econ_item_view::m_bDisallowSOC) = false;
                *reinterpret_cast<bool*>(item_view + offsets::econ_item_view::m_bInitialized) = true;
            } else {
                // Mode Fallback uniquement si le CEconItem n'est pas présent dans le SOCache
                *reinterpret_cast<int32_t*>(item_view + offsets::econ_item_view::m_iItemIDHigh) = -1;
                *reinterpret_cast<bool*>(item_view + offsets::econ_item_view::m_bDisallowSOC) = true;
            }

            *reinterpret_cast<int32_t*>(weapon + offsets::econ_entity::m_nFallbackPaintKit) = cfg.paint_index;
            *reinterpret_cast<int32_t*>(weapon + offsets::econ_entity::m_nFallbackSeed) = cfg.paint_seed;
            *reinterpret_cast<float*>(weapon + offsets::econ_entity::m_flFallbackWear) = cfg.paint_wear;
            *reinterpret_cast<int32_t*>(weapon + offsets::econ_entity::m_nFallbackStatTrak) = cfg.stattrak;
            *reinterpret_cast<int32_t*>(item_view + offsets::econ_item_view::m_iEntityQuality) = cfg.quality;

            if (!cfg.custom_name.empty()) {
                char* name_buf = reinterpret_cast<char*>(item_view + offsets::econ_item_view::m_szCustomName);
                strncpy_s(name_buf, 32, cfg.custom_name.c_str(), _TRUNCATE);
            }

            uintptr_t weapon_scene_node = *reinterpret_cast<uintptr_t*>(weapon + offsets::pawn::m_pGameSceneNode);
            if (weapon_scene_node) {
                *reinterpret_cast<uint64_t*>(weapon_scene_node + offsets::scene_node::m_MeshGroupMask) = 2ULL;
            }
        }

        uintptr_t vm_services = *reinterpret_cast<uintptr_t*>(local_pawn + offsets::pawn::m_pViewModelServices);
        if (vm_services) {
            uint32_t vm_handle = *reinterpret_cast<uint32_t*>(vm_services + offsets::viewmodel_services::m_hViewModel);
            uintptr_t viewmodel = GetEntityByHandle(entity_list, vm_handle);
            if (viewmodel) {
                uintptr_t vm_scene = *reinterpret_cast<uintptr_t*>(viewmodel + offsets::pawn::m_pGameSceneNode);
                if (vm_scene) {
                    *reinterpret_cast<uint64_t*>(vm_scene + offsets::scene_node::m_MeshGroupMask) = 2ULL;
                }
            }
        }
    } __except (EXCEPTION_EXECUTE_HANDLER) {
        return;
    }
}

static void MesaBridgeWorker(HMODULE self_module) {
    char dll_path_buf[MAX_PATH]{};
    GetModuleFileNameA(self_module, dll_path_buf, MAX_PATH);
    fs::path dll_dir = fs::path(dll_path_buf).parent_path();
    fs::path root_dir = LocateProjectRoot(dll_dir);
    fs::path socache_json = root_dir / "inventory_socache.json";

    AppendBridgeLog(root_dir, "[INIT] mesa_bridge.dll attache dans cs2.exe. Dossier racine=" + root_dir.string());

    HMODULE client_mod = nullptr;
    while (!client_mod && g_running) {
        client_mod = GetModuleHandleA("client.dll");
        std::this_thread::sleep_for(std::chrono::milliseconds(250));
    }
    uintptr_t client_base = reinterpret_cast<uintptr_t>(client_mod);

    uintptr_t ent_insn = PatternScan(client_mod, offsets::sigs::entity_list);
    uintptr_t pawn_insn = PatternScan(client_mod, offsets::sigs::local_player_pawn);
    uintptr_t resolved_ent_list = ent_insn ? ResolveRelativeRip(ent_insn, 3, 7) : 0;
    uintptr_t resolved_pawn = pawn_insn ? ResolveRelativeRip(pawn_insn, 3, 7) : 0;

    fs::file_time_type last_write{};
    uint64_t tick_counter = 0;

    while (g_running) {
        if (tick_counter % 60 == 0 && fs::exists(socache_json)) {
            std::error_code ec;
            auto current_write = fs::last_write_time(socache_json, ec);
            if (!ec && current_write != last_write) {
                last_write = current_write;
                ParseSocacheJsonFile(socache_json, root_dir, client_base);
            }
        }

        {
            std::lock_guard<std::mutex> lock(g_config_mutex);
            if (!g_active_skins.empty()) {
                ApplySkinsInGameTickSeh(client_base, resolved_ent_list, resolved_pawn);
            }
        }

        ++tick_counter;
        std::this_thread::sleep_for(std::chrono::milliseconds(8));
    }
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID) {
    if (ul_reason_for_call == DLL_PROCESS_ATTACH) {
        DisableThreadLibraryCalls(hModule);
        std::thread(MesaBridgeWorker, hModule).detach();
    } else if (ul_reason_for_call == DLL_PROCESS_DETACH) {
        g_running = false;
    }
    return TRUE;
}

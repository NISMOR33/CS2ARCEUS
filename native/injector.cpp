#define WIN32_LEAN_AND_MEAN
#include <Windows.h>
#include <TlHelp32.h>
#include <cstdint>
#include <cwctype>
#include <filesystem>
#include <iostream>
#include <string>

namespace fs = std::filesystem;

static std::wstring ToLowerW(std::wstring s) {
    for (auto& ch : s) {
        ch = static_cast<wchar_t>(std::towlower(ch));
    }
    return s;
}

static DWORD FindProcessId(const std::wstring& process_name) {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) {
        return 0;
    }

    PROCESSENTRY32W entry{};
    entry.dwSize = sizeof(entry);

    if (Process32FirstW(snapshot, &entry)) {
        do {
            if (ToLowerW(process_name) == ToLowerW(entry.szExeFile)) {
                CloseHandle(snapshot);
                return entry.th32ProcessID;
            }
        } while (Process32NextW(snapshot, &entry));
    }

    CloseHandle(snapshot);
    return 0;
}

static bool IsModuleLoadedInProcess(DWORD pid, const std::wstring& dll_filename) {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid);
    if (snapshot == INVALID_HANDLE_VALUE) {
        return false;
    }

    MODULEENTRY32W mod{};
    mod.dwSize = sizeof(mod);
    const std::wstring target = ToLowerW(dll_filename);

    if (Module32FirstW(snapshot, &mod)) {
        do {
            if (ToLowerW(mod.szModule) == target) {
                CloseHandle(snapshot);
                return true;
            }
        } while (Module32NextW(snapshot, &mod));
    }

    CloseHandle(snapshot);
    return false;
}

static bool InjectBridgeDll(DWORD pid, const fs::path& dll_path) {
    const std::wstring dll_name = dll_path.filename().wstring();
    if (IsModuleLoadedInProcess(pid, dll_name)) {
        std::cout << "[+] " << dll_path.filename().string() << " est deja charge dans cs2.exe (PID " << pid << ").\n";
        return true;
    }

    const std::wstring full_path = fs::absolute(dll_path).wstring();
    const size_t bytes_len = (full_path.size() + 1) * sizeof(wchar_t);

    HANDLE proc = OpenProcess(
        PROCESS_CREATE_THREAD | PROCESS_QUERY_INFORMATION | PROCESS_VM_OPERATION | PROCESS_VM_WRITE | PROCESS_VM_READ,
        FALSE,
        pid
    );
    if (!proc) {
        std::cerr << "[!] OpenProcess a echoue (code " << GetLastError() << "). Lance en Administrateur.\n";
        return false;
    }

    void* remote_mem = VirtualAllocEx(proc, nullptr, bytes_len, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (!remote_mem) {
        CloseHandle(proc);
        return false;
    }

    if (!WriteProcessMemory(proc, remote_mem, full_path.c_str(), bytes_len, nullptr)) {
        VirtualFreeEx(proc, remote_mem, 0, MEM_RELEASE);
        CloseHandle(proc);
        return false;
    }

    HMODULE kernel32 = GetModuleHandleW(L"kernel32.dll");
    auto load_lib = reinterpret_cast<LPTHREAD_START_ROUTINE>(GetProcAddress(kernel32, "LoadLibraryW"));
    HANDLE thread = CreateRemoteThread(proc, nullptr, 0, load_lib, remote_mem, 0, nullptr);
    if (!thread) {
        VirtualFreeEx(proc, remote_mem, 0, MEM_RELEASE);
        CloseHandle(proc);
        return false;
    }

    DWORD wait_res = WaitForSingleObject(thread, 5000);
    DWORD exit_code = 0;
    GetExitCodeThread(thread, &exit_code);

    CloseHandle(thread);
    VirtualFreeEx(proc, remote_mem, 0, MEM_RELEASE);
    CloseHandle(proc);

    if (wait_res != WAIT_OBJECT_0 || exit_code == 0) {
        std::cerr << "[!] LoadLibraryW a echoue dans cs2.exe (wait=" << wait_res << ", exit=" << exit_code << ").\n";
        return false;
    }

    if (!IsModuleLoadedInProcess(pid, dll_name)) {
        std::cerr << "[!] Verification module echouee apres LoadLibraryW.\n";
        return false;
    }

    return true;
}

int main(int argc, char* argv[]) {
    fs::path dll_path = fs::current_path() / "mesa_bridge.dll";
    if (argc > 1) {
        dll_path = argv[1];
    }

    if (!fs::exists(dll_path)) {
        std::cerr << "[!] Introuvable : " << dll_path.string() << "\n";
        return 1;
    }

    DWORD pid = FindProcessId(L"cs2.exe");
    if (!pid) {
        std::cerr << "[!] cs2.exe n'est pas lance. Demarre CS2 d'abord.\n";
        return 2;
    }

    if (InjectBridgeDll(pid, dll_path)) {
        std::cout << "[+] mesa_bridge.dll confirme et actif dans cs2.exe (PID " << pid << ").\n";
        return 0;
    }
    return 3;
}

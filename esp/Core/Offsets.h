#ifndef Offsets_h
#define Offsets_h

#include <cstdint>

namespace AotForm
{
    struct Offsets
    {
        static const uint32_t Il2Cpp = 0x0;
        static const uint32_t UnityCpp = 0x0;
        static const uint32_t InitBase = 0xA988FDC;
        static const uint32_t StaticClass = 0x5C;

        // Match Related
        static const uint32_t CurrentMatch = 0x50;
        static const uint32_t MatchStatus = 0x8C;
        static const uint32_t LocalPlayer = 0x94;
        static const uint32_t LocalPlayerAttributes = 0x4BC;
        static const uint32_t DictionaryEntities = 0x68;

        // Player
        static const uint32_t TeamID = 0x29C;
        static const uint32_t Player_IsDead = 0x50;
        static const uint32_t Player_Name = 0x2DC;
        static const uint32_t Player_Data = 0x48;
        static const uint32_t Player_ShadowBase = 0x18B8;
        static const uint32_t XPose = 0x78;
        static const uint32_t AvatarManager = 0x4C0;
        static const uint32_t Avatar = 0xA8;
        static const uint32_t Avatar_IsVisible = 0x95;
        static const uint32_t Avatar_Data = 0x14;
        static const uint32_t Avatar_Data_IsTeam = 0x59;
        static const uint32_t Avatar_Data_IsBot = 0x2E4;
        static const uint32_t PlayerID = 0x268;
        static const uint32_t BaseProfileInfo = 0x18CC;
        static const uint32_t IsClientBot = 0x2E4;

        // Camera
        static const uint32_t FollowCamera = 0x450;
        static const uint32_t Camera = 0x18;
        static const uint32_t MainCameraTransform = 0x24C;
        static const uint32_t AimRotation = 0x400;
        static const uint32_t ViewMatrix = 0xE8;

        // Loot / ESP Items
        static const uint32_t Loot_ID = 0x8;
        static const uint32_t Loot_Pos = 0x48;
        static const uint32_t LevelObjectManager = 0x60;
        static const uint32_t LevelObjectList = 0x30;

        // Observer
        static const uint32_t CurrentObserver = 0xB4;
        static const uint32_t ObserverPlayer = 0x28;

        // Weapon
        static const uint32_t Weapon = 0x3F4;
        static const uint32_t WeaponData = 0x58;
        static const uint32_t WeaponRecoil = 0xC;
        static const uint32_t UnkPlayerWeaponInfoClass = 0x4A8;
        static const uint32_t IsCombineWeapon = 0xD8;
        static const uint32_t WeaponOnHand = 0x54;
        static const uint32_t CombineWeaponOnHand = 0x58;
        static const uint32_t WeaponInfo = 0x64;
        static const uint32_t WeaponID = 0x14;
        static const uint32_t Weapon_Damage = 0x8;

        // Silent Aim / Aim Info
        static const uint32_t LastAimingInfoFromWeapon = 0x978;
        static const uint32_t StartPosition = 0x38;
        static const uint32_t RayDir = 0x2C;
        static const uint32_t LockedAimingCollider = 0x54;
        static const uint32_t HeadCollider = 0x4A4;

        // Aiming (firing/rotate)
        static const uint32_t LocalPlayerIsFiring = 0x48C;
        static const uint32_t SilentAimShoot = 0x48C;
        static const uint32_t SilentAimRotate = 0x4A0;

        // Aimkill
        static const uint32_t LocalPlayer_Target = 0x48;
        static const uint32_t Enemy_Knockdowns = 0x68;
        static const uint32_t Player_Inventory = 0x1B0;

        // Misc
        static const uint32_t PlayerAttributes = 0x4B0;
        static const uint32_t NoReload = 0x99;
        static const uint32_t RunSpeedUpScale = 0x1D8;
        static const uint32_t FallingSpeedUpScale = 0x1B8;
        static const uint32_t GameTimer = 0x10;
        static const uint32_t FixedDeltaTime = 0x24;
        static const uint32_t BuffWeaponMoveSpeedScale = 0xBC;
        static const uint32_t InSnowSlideWayDashing = 0x15E8;
        static const uint32_t m_ReviveHP = 0xF4;
        static const uint32_t isBotOffs = 0xC0;

        // Jump / misc
        static const uint32_t highjumpff = 0x893EC6C;

        // Legacy aim aliases
        static const uint32_t sAim1 = 0x540;
        static const uint32_t sAim2 = 0x978;
        static const uint32_t sAim3 = 0x38;
        static const uint32_t sAim4 = 0x2C;

        // Portuguese aim aliases
        static const uint32_t pomba = 0x540;
        static const uint32_t bisteca = 0x978;
        static const uint32_t arma = 0x38;
        static const uint32_t tiro = 0x2C;

        static const uint32_t TeleportMark_UIInGameScene = 0x8;
        static const uint32_t TeleportMark_BigMapCtrl = 0x218;
        static const uint32_t TeleportMark_MapContentCtrl = 0x54;
        static const uint32_t TeleportMark_LocalMapMarkController = 0x90;
        static const uint32_t TeleportMark_MarkPos = 0x58;
    };

    enum class Bones : uint32_t
    {
        Head = 0x458,
        Neck = 0x460,
        Hip = 0x45C,
        LeftShoulder = 0x48C,
        RightShoulder = 0x490,
        LeftElbow = 0x4A0,
        RightElbow = 0x49C,
        LeftWrist = 0x498,
        RightWrist = 0x494,
        LeftHand = 0x484,
        RightHand = 0x454,
        LeftAnkle = 0x474,
        RightAnkle = 0x478,
        LeftFoot = 0x464,
        RightFoot = 0x480,
        Root = 0x46c
    };
}

#endif

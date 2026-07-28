#import "GameLogic.h"

#pragma mark - Function Game

uint64_t getMatchGame(uint64_t Moudule_Base) {
    uint64_t GameFacade_TypeInfo = ReadAddr<uint64_t>(Moudule_Base + AotForm::Offsets::InitBase);
    uint64_t GameFacade_Static = ReadAddr<uint64_t>(GameFacade_TypeInfo + 0xB8);
    return ReadAddr<uint64_t>(GameFacade_Static + 0x0);
}

uint64_t getMatch(uint64_t matchgame) {
    return ReadAddr<uint64_t>(matchgame + AotForm::Offsets::CurrentMatch);
}

uint64_t CameraMain(uint64_t matchgame) {
    uint64_t CameraControllerManager = ReadAddr<uint64_t>(matchgame + 0xD8);
    return ReadAddr<uint64_t>(CameraControllerManager + AotForm::Offsets::Camera);
}

float* GetViewMatrix(uint64_t cameraMain) {
    uint64_t v1 = ReadAddr<uint64_t>(cameraMain + 0x10);
    
    static float matrix[16];
    for (int i = 0; i < 16; i++) {
        matrix[i] = ReadAddr<float>(v1 + AotForm::Offsets::ViewMatrix + i * 0x4);
    }
    
    return matrix;
}

uint64_t getTransNode(uint64_t BodyPart) {
    return ReadAddr<uint64_t>(BodyPart + 0x10);
}

uint64_t getHead(uint64_t player) {
    uint64_t BodyPart = ReadAddr<uint64_t>(player + (uint32_t)AotForm::Bones::Head);
    return getTransNode(BodyPart);
}

uint64_t getRightToeNode(uint64_t player) {
    uint64_t BodyPart = ReadAddr<uint64_t>(player + (uint32_t)AotForm::Bones::RightFoot);
    return getTransNode(BodyPart);
}

uint64_t getLocalPlayer(uint64_t match) {
    return ReadAddr<uint64_t>(match + AotForm::Offsets::LocalPlayer);
}

bool isLocalTeamMate(uint64_t localPlayer, uint64_t Player) {
    int myTeamID = ReadAddr<int>(localPlayer + AotForm::Offsets::TeamID);
    int TeamID = ReadAddr<int>(Player + AotForm::Offsets::TeamID);
    
    return myTeamID == TeamID;
}

int GetDataUInt16(uint64_t player, int varID) {
    uint64_t IPRIDataPool = ReadAddr<uint64_t>(player + AotForm::Offsets::PlayerAttributes);
    if (isVaildPtr(IPRIDataPool)) {
        uint64_t v2 = ReadAddr<uint64_t>(IPRIDataPool + 0x10);
        uint64_t v4 = ReadAddr<uint64_t>(v2 + 0x8 * varID + 0x20);
        int v6 = ReadAddr<int>(v4 + 0x18);
        return v6;
    }
    return 0;
}

int get_CurHP(uint64_t Player) {
    return GetDataUInt16(Player, 0);
}

int get_MaxHP(uint64_t Player) {
    return GetDataUInt16(Player, 1);
}
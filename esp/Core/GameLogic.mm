#import "GameLogic.h"

#pragma mark - Function Game

uint64_t getMatchGame(uint64_t Moudule_Base) {
    uint64_t GameFacade_TypeInfo = ReadAddr<uint64_t>(Moudule_Base + 0xA988FDC);
    uint64_t GameFacade_Static = ReadAddr<uint64_t>(GameFacade_TypeInfo + 0x5C);
    return ReadAddr<uint64_t>(GameFacade_Static + 0x0);
}

uint64_t getMatch(uint64_t matchgame) {
    return ReadAddr<uint64_t>(matchgame + 0x50);
}

uint64_t CameraMain(uint64_t matchgame) {
    uint64_t CameraControllerManager = ReadAddr<uint64_t>(matchgame + 0x450);
    return ReadAddr<uint64_t>(CameraControllerManager + 0x18);
}

float* GetViewMatrix(uint64_t cameraMain) {
    uint64_t v1 = ReadAddr<uint64_t>(cameraMain + 0x10);
    
    static float matrix[16];
    for (int i = 0; i < 16; i++) {
        matrix[i] = ReadAddr<float>(v1 + 0xE8 + i * 0x4);
    }
    
    return matrix;
}

uint64_t getTransNode(uint64_t BodyPart) {
    return ReadAddr<uint64_t>(BodyPart + 0x10);
}

uint64_t getHead(uint64_t player) {
    uint64_t BodyPart = ReadAddr<uint64_t>(player + 0x458);
    return getTransNode(BodyPart);
}

uint64_t getRightToeNode(uint64_t player) {
    uint64_t BodyPart = ReadAddr<uint64_t>(player + 0x480);
    return getTransNode(BodyPart);
}

uint64_t getLocalPlayer(uint64_t match) {
    return ReadAddr<uint64_t>(match + 0x94);
}

bool isLocalTeamMate(uint64_t localPlayer, uint64_t Player) {
    COW_GamePlay_PlayerID_o myPlayerID = ReadAddr<COW_GamePlay_PlayerID_o>(localPlayer + 0x268);
    COW_GamePlay_PlayerID_o PlayerID = ReadAddr<COW_GamePlay_PlayerID_o>(Player + 0x268);
    
    int myTeamID = myPlayerID.m_TeamID;
    int TeamID = PlayerID.m_TeamID;
    
    return myTeamID == TeamID;
}

int GetDataUInt16(uint64_t player, int varID) {
    uint64_t IPRIDataPool = ReadAddr<uint64_t>(player + 0x48);
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
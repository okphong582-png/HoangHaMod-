#import "esp.h"
#import <objc/runtime.h>

#define sWidth  [UIScreen mainScreen].bounds.size.width
#define sHeight [UIScreen mainScreen].bounds.size.height

uint64_t Moudule_Base = 0;
static pid_t g_GamePID = -1;
static char g_StatusText[256] = "[HUD] Searching for Free Fire process...";
static UIColor *g_StatusColor = nil;

@interface ESP_View ()
@property (nonatomic, strong) CADisplayLink *displayLinkDATA;
@property (nonatomic, strong) NSMutableArray<NSValue *> *playersData;
@end

@implementation ESP_View

- (instancetype)initWithFrame:(CGRect)frame
{
    self = [super initWithFrame:frame];
    if (self) {
        self.backgroundColor = [UIColor clearColor];
        self.userInteractionEnabled = NO;

        _enableBox = YES;
        _enableLine = YES;
        _enableName = YES;
        _enableInfo = YES;

        _playersData = [NSMutableArray array];
        g_StatusColor = [UIColor yellowColor];

        self.displayLinkDATA = [CADisplayLink displayLinkWithTarget:self selector:@selector(update_data)];
        [self.displayLinkDATA addToRunLoop:[NSRunLoop mainRunLoop] forMode:NSRunLoopCommonModes];
    }
    return self;
}

- (void)dealloc {
    [self.displayLinkDATA invalidate];
    self.displayLinkDATA = nil;
}

- (void)update_data
{
    // Check process health
    if (g_GamePID > 0) {
        if (kill(g_GamePID, 0) != 0) {
            Moudule_Base = 0;
            g_GamePID = -1;
        }
    }

    // Auto scan for game process base address
    if (Moudule_Base == 0 || g_GamePID <= 0) {
        const char* targets[] = {"freefireth", "freefiremax", "freefire", "FreeFire", "ShadowTrackerExtra"};
        for (int i = 0; i < 5; i++) {
            pid_t pid = GetGameProcesspid((char*)targets[i]);
            if (pid > 0) {
                vm_map_offset_t base = GetGameModule_Base((char*)targets[i]);
                if (base > 0 && isVaildPtr((long)base)) {
                    Moudule_Base = (uint64_t)base;
                    g_GamePID = pid;
                    break;
                }
            }
        }
    }

    if (Moudule_Base == 0 || g_GamePID <= 0) {
        snprintf(g_StatusText, sizeof(g_StatusText), "[HUD] Searching for Free Fire process...");
        g_StatusColor = [UIColor colorWithRed:1.0 green:0.8 blue:0.2 alpha:1.0];
        [self.playersData removeAllObjects];
        dispatch_async(dispatch_get_main_queue(), ^{
            [self setNeedsDisplay];
        });
        return;
    }

    uint64_t matchGame = getMatchGame(Moudule_Base);
    if (!isVaildPtr(matchGame)) {
        snprintf(g_StatusText, sizeof(g_StatusText), "[HUD] Free Fire (PID: %d | Base: 0x%llX) - Waiting for Match...", g_GamePID, (unsigned long long)Moudule_Base);
        g_StatusColor = [UIColor orangeColor];
        [self.playersData removeAllObjects];
        dispatch_async(dispatch_get_main_queue(), ^{
            [self setNeedsDisplay];
        });
        return;
    }

    uint64_t camera = CameraMain(matchGame);
    uint64_t match = getMatch(matchGame);
    uint64_t myPawnObject = getLocalPlayer(match);

    if (!isVaildPtr(camera) || !isVaildPtr(match) || !isVaildPtr(myPawnObject)) {
        snprintf(g_StatusText, sizeof(g_StatusText), "[HUD] Free Fire (PID: %d) - Loading Match Data...", g_GamePID);
        g_StatusColor = [UIColor yellowColor];
        [self.playersData removeAllObjects];
        dispatch_async(dispatch_get_main_queue(), ^{
            [self setNeedsDisplay];
        });
        return;
    }

    uint64_t mainCameraTransform = ReadAddr<uint64_t>(myPawnObject + AotForm::Offsets::MainCameraTransform);
    Vector3 myLocation = getPositionExt(mainCameraTransform);
    
    uint64_t player = ReadAddr<uint64_t>(match + AotForm::Offsets::DictionaryEntities);
    uint64_t tValue = ReadAddr<uint64_t>(player + 0x28);
    int coutValue = ReadAddr<int>(tValue + 0x18);
    
    float *matrix = GetViewMatrix(camera);
    NSMutableArray<NSValue *> *dataMutable = [NSMutableArray array];

    for (int i = 0; i < coutValue; i++) {
        uint64_t PawnObject = ReadAddr<uint64_t>(tValue + 0x20 + 8 * i);
        if (!isVaildPtr(PawnObject)) continue;

        bool isLocalTeam = isLocalTeamMate(myPawnObject, PawnObject);
        if (isLocalTeam) continue;
        
        NSString *Name = GetNickName(PawnObject);
        if (Name.length == 0) continue;

        int CurHP = get_CurHP(PawnObject);
        int MaxHP = get_MaxHP(PawnObject);

        Vector3 HeadLocation = getPositionExt(getHead(PawnObject));
        HeadLocation.y += 0.2f;

        Vector3 RightToePos = getPositionExt(getRightToeNode(PawnObject));
        
        Vector3 w2sHeadLocation = WorldToScreen(HeadLocation, matrix, sWidth, sHeight);
        Vector3 w2sRightToePos  = WorldToScreen(RightToePos, matrix, sWidth, sHeight);
        
        float dis = Vector3::Distance(myLocation, HeadLocation);
        if (dis > 350.0f) continue;

        float boxHeight = abs(w2sHeadLocation.y - w2sRightToePos.y);
        float boxWidth = boxHeight * 0.5f;

        ESPPlayerData pData;
        pData.headPos = w2sHeadLocation;
        pData.feetPos = w2sRightToePos;
        pData.width = boxWidth;
        pData.height = boxHeight;
        pData.distance = dis;
        pData.curHP = CurHP > 0 ? CurHP : 100;
        pData.maxHP = MaxHP > 0 ? MaxHP : 100;
        const char *cName = [Name UTF8String];
        strncpy(pData.name, cName ? cName : "Player", sizeof(pData.name) - 1);

        [dataMutable addObject:[NSValue valueWithBytes:&pData objCType:@encode(ESPPlayerData)]];
    }

    snprintf(g_StatusText, sizeof(g_StatusText), "[AOTFORM ESP] 🟢 In-Game (PID: %d | Enemies: %d)", g_GamePID, (int)dataMutable.count);
    g_StatusColor = [UIColor colorWithRed:0.0 green:1.0 blue:0.5 alpha:1.0];

    self.playersData = dataMutable;
    dispatch_async(dispatch_get_main_queue(), ^{
        [self setNeedsDisplay];
    });
}

- (void)drawRect:(CGRect)rect {
    [super drawRect:rect];

    CGContextRef ctx = UIGraphicsGetCurrentContext();
    if (!ctx) return;

    // Draw Status HUD Overlay (Top-left)
    NSString *statusStr = [NSString stringWithUTF8String:g_StatusText];
    NSDictionary *statusAttr = @{
        NSFontAttributeName: [UIFont boldSystemFontOfSize:13],
        NSForegroundColorAttributeName: g_StatusColor ? g_StatusColor : [UIColor yellowColor]
    };
    [statusStr drawAtPoint:CGPointMake(20, 25) withAttributes:statusAttr];

    for (NSValue *val in self.playersData) {
        ESPPlayerData pData;
        [val getValue:&pData];

        float x = pData.headPos.x - pData.width * 0.5f;
        float y = pData.headPos.y;

        // 1. Draw SnapLine (Top-Center of screen to Enemy Head)
        if (self.enableLine) {
            CGContextSetStrokeColorWithColor(ctx, [UIColor colorWithRed:1.0 green:0.2 blue:0.2 alpha:0.85].CGColor);
            CGContextSetLineWidth(ctx, 1.2);
            CGContextMoveToPoint(ctx, sWidth / 2, 0);
            CGContextAddLineToPoint(ctx, pData.headPos.x, pData.headPos.y);
            CGContextStrokePath(ctx);
        }

        // 2. Draw 2D Box
        if (self.enableBox) {
            CGContextSetStrokeColorWithColor(ctx, [UIColor colorWithRed:0.0 green:1.0 blue:0.4 alpha:0.9].CGColor);
            CGContextSetLineWidth(ctx, 1.8);
            CGContextStrokeRect(ctx, CGRectMake(x, y, pData.width, pData.height));
        }

        // 3. Draw Player Name
        if (self.enableName) {
            NSString *nameStr = [NSString stringWithUTF8String:pData.name];
            NSDictionary *attr = @{
                NSFontAttributeName: [UIFont boldSystemFontOfSize:11],
                NSForegroundColorAttributeName: [UIColor whiteColor]
            };
            CGSize textRect = [nameStr sizeWithAttributes:attr];
            [nameStr drawAtPoint:CGPointMake(pData.headPos.x - textRect.width / 2, y - 16) withAttributes:attr];
        }

        // 4. Draw Distance & Health Bar
        if (self.enableInfo) {
            // Distance text (meters)
            NSString *infoStr = [NSString stringWithFormat:@"%.0fm", pData.distance];
            NSDictionary *infoAttr = @{
                NSFontAttributeName: [UIFont systemFontOfSize:10 weight:UIFontWeightBold],
                NSForegroundColorAttributeName: [UIColor yellowColor]
            };
            CGSize infoSize = [infoStr sizeWithAttributes:infoAttr];
            [infoStr drawAtPoint:CGPointMake(pData.headPos.x - infoSize.width / 2, y + pData.height + 2) withAttributes:infoAttr];

            // Health Bar
            float hpPercent = (float)pData.curHP / (float)pData.maxHP;
            hpPercent = MAX(0.0f, MIN(1.0f, hpPercent));

            float barW = pData.width;
            float barH = 3.5f;
            float barX = x;
            float barY = y + pData.height + 15;

            // Background bar (black)
            CGContextSetFillColorWithColor(ctx, [UIColor colorWithWhite:0.1 alpha:0.7].CGColor);
            CGContextFillRect(ctx, CGRectMake(barX, barY, barW, barH));

            // HP fill (Green to Red)
            UIColor *hpColor = hpPercent > 0.5f ? [UIColor greenColor] : (hpPercent > 0.25f ? [UIColor orangeColor] : [UIColor redColor]);
            CGContextSetFillColorWithColor(ctx, hpColor.CGColor);
            CGContextFillRect(ctx, CGRectMake(barX, barY, barW * hpPercent, barH));
        }
    }
}

@end

#import "esp.h"

#define sWidth  [UIScreen mainScreen].bounds.size.width
#define sHeight [UIScreen mainScreen].bounds.size.height

@interface ESP_View ()
@property (nonatomic, strong) NSMutableArray<CALayer *> *layers;
@property (nonatomic, strong) CADisplayLink *displayLink;
@property (nonatomic, strong) CADisplayLink *displayLinkDATA;
@property (nonatomic, strong) NSArray<NSValue *> *boxesData;
@property (nonatomic, strong) UILabel *statusLabel;
@end

uint64_t Moudule_Base = -1;

@implementation ESP_View

- (instancetype)initWithFrame:(CGRect)frame
{
    self = [super initWithFrame:frame];
    if (self) {
        self.layers = [NSMutableArray array];
        self.backgroundColor = [UIColor clearColor];

        self.statusLabel = [[UILabel alloc] initWithFrame:CGRectMake(20, 20, 500, 30)];
        self.statusLabel.textColor = [UIColor yellowColor];
        self.statusLabel.font = [UIFont boldSystemFontOfSize:14];
        self.statusLabel.text = @"[HUD] Searching for Free Fire process...";
        self.statusLabel.layer.shadowColor = [UIColor blackColor].CGColor;
        self.statusLabel.layer.shadowOffset = CGSizeMake(1, 1);
        self.statusLabel.layer.shadowOpacity = 1.0;
        self.statusLabel.layer.shadowRadius = 1.0;
        [self addSubview:self.statusLabel];

        static dispatch_once_t onceToken;
        dispatch_once(&onceToken, ^{
            Moudule_Base = (uint64_t)GetGameModule_Base((char*)"freefireth");
        });

        self.displayLink = [CADisplayLink displayLinkWithTarget:self selector:@selector(updateBoxes)];
        [self.displayLink addToRunLoop:[NSRunLoop mainRunLoop] forMode:NSRunLoopCommonModes];
        
        self.displayLinkDATA = [CADisplayLink displayLinkWithTarget:self selector:@selector(update_data)];
        [self.displayLinkDATA addToRunLoop:[NSRunLoop mainRunLoop] forMode:NSRunLoopCommonModes];
    }
    return self;
}

- (void)layoutSubviews {
    [super layoutSubviews];
    if (self.superview) {
        self.frame = self.superview.bounds;
    }
    [self updateBoxes];
}

- (void)setBoxes:(NSArray<NSValue *> *)boxes
{
    _boxesData = [boxes copy];
    [self updateBoxes];
}

- (void)updateBoxes {
    if (!self.window) return;
    NSUInteger count = self.boxesData.count;
    
    if (count == 0)
    {
        for (CALayer *layer in self.layers)
        {
            [layer removeFromSuperlayer];
        }
        [self.layers removeAllObjects];
        return;
    }
    
    while (self.layers.count < count)
    {
        CALayer *layer = [CALayer layer];
        layer.borderColor = [UIColor colorWithRed:1 green:0 blue:0 alpha:0.8].CGColor;
        layer.borderWidth = 2.0;
        layer.cornerRadius = 3.0;
        [self.layer addSublayer:layer];
        [self.layers addObject:layer];
    }

    for (NSUInteger i = 0; i < self.layers.count; i++)
    {
        CALayer *layer = self.layers[i];

        if (i < count)
        {
            ESPBox box;
            [self.boxesData[i] getValue:&box];
            layer.hidden = NO;
            
            [CATransaction begin];
            [CATransaction setDisableActions:YES];
            layer.frame = CGRectMake(box.pos.x, box.pos.y, box.width, box.height);
            [CATransaction commit];

        } else {
            layer.hidden = YES;
        }
    }
}

- (void)dealloc {
    [self.displayLink invalidate];
    [self.displayLinkDATA invalidate];
    self.displayLink = nil;
    self.displayLinkDATA = nil;
    [[NSNotificationCenter defaultCenter] removeObserver:self];
}

static int g_GamePID = -1;

- (void)update_data
{
    CFTimeInterval t = CACurrentMediaTime();
    CGSize size = self.bounds.size;
    
    const NSInteger boxCount = 10;
    const CGFloat baseWidth = 60.0;
    const CGFloat baseHeight = 120.0;

    NSMutableArray<NSValue *> *boxesMutable = [NSMutableArray arrayWithCapacity:boxCount];
    int countObject = 0;

    if (g_GamePID > 0) {
        if (kill(g_GamePID, 0) != 0) {
            Moudule_Base = 0;
            g_GamePID = -1;
        }
    }

    if (Moudule_Base == -1 || Moudule_Base == 0) {
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

        if (Moudule_Base == -1 || Moudule_Base == 0) {
            dispatch_async(dispatch_get_main_queue(), ^{
                self.statusLabel.textColor = [UIColor yellowColor];
                self.statusLabel.text = @"[HUD] Searching for Free Fire process...";
            });
            self.boxes = @[];
            [self setNeedsDisplay];
            return;
        }

        NSLog(@"[ESP] found game with pid = %d, base = 0x%llx", g_GamePID, (unsigned long long)Moudule_Base);
        dispatch_async(dispatch_get_main_queue(), ^{
            self.statusLabel.textColor = [UIColor greenColor];
            self.statusLabel.text = [NSString stringWithFormat:@"[HUD] Found Free Fire (PID: %d | Base: 0x%llx)", g_GamePID, (unsigned long long)Moudule_Base];
        });
    }

    uint64_t matchGame = getMatchGame(Moudule_Base);
    if (!isVaildPtr(matchGame)) {
        dispatch_async(dispatch_get_main_queue(), ^{
            self.statusLabel.textColor = [UIColor orangeColor];
            self.statusLabel.text = [NSString stringWithFormat:@"[HUD] Free Fire Found (PID: %d) - Waiting for Match...", g_GamePID];
        });
        self.boxes = @[];
        [self setNeedsDisplay];
        return;
    }

    uint64_t camera = CameraMain(matchGame);
    if (!isVaildPtr(camera)) {
        self.boxes = @[];
        [self setNeedsDisplay];
        return;
    }

    uint64_t match = getMatch(matchGame);
    if (!isVaildPtr(match)) {
        self.boxes = @[];
        [self setNeedsDisplay];
        return;
    }

    uint64_t myPawnObject = getLocalPlayer(match);
    if (!isVaildPtr(myPawnObject)) {
        self.boxes = @[];
        [self setNeedsDisplay];
        return;
    }
    
    dispatch_async(dispatch_get_main_queue(), ^{
        self.statusLabel.textColor = [UIColor colorWithRed:0.0 green:1.0 blue:0.5 alpha:1.0];
        self.statusLabel.text = [NSString stringWithFormat:@"[HUD] Free Fire In-Game (PID: %d)", g_GamePID];
    });
    
    uint64_t mainCameraTransform = ReadAddr<uint64_t>(myPawnObject + 0x24C);
    Vector3 myLocation = getPositionExt(mainCameraTransform);
    
    uint64_t player = ReadAddr<uint64_t>(match + 0x68);
    uint64_t tValue = ReadAddr<uint64_t>(player + 0x28);
    int coutValue = ReadAddr<int>(tValue + 0x18);
    
    float *matrix = GetViewMatrix(camera);

    for (int i = 0; i < coutValue; i++) {
        uint64_t PawnObject = ReadAddr<uint64_t>(tValue + 0x20 + 8 * i);
        if (!isVaildPtr(PawnObject)) continue;

        bool isLocalTeam = isLocalTeamMate(myPawnObject, PawnObject);
        if (isLocalTeam) continue;
        
        NSString *Name = GetNickName(PawnObject);
        if (Name.length == 0) continue;

        int CurHP = get_CurHP(PawnObject);
        int MaxHP = get_MaxHP(PawnObject);

        Vector3 HeadLocation     = getPositionExt(getHead(PawnObject));
        HeadLocation.y           += 0.2f;

        Vector3 RightToePos      = getPositionExt(getRightToeNode(PawnObject));
        
        Vector3 w2sHeadLocation  = WorldToScreen(HeadLocation, matrix, sWidth, sHeight);
        Vector3 w2sRightToePos   = WorldToScreen(RightToePos, matrix, sWidth, sHeight);
        
        float dis = Vector3::Distance(myLocation, HeadLocation);
        if (dis > 220.0f) continue;
        
        countObject++;

        float boxHeight = abs(w2sHeadLocation.y - w2sRightToePos.y);
        float boxWidth = boxHeight * 0.5f;
        float x = w2sHeadLocation.x - boxWidth * 0.5f;
        float y = w2sHeadLocation.y;
        CGRect box = CGRectMake(x, y, boxWidth, boxHeight);

        ESPBox espBox;
        espBox.pos.x = x;
        espBox.pos.y = y;
        espBox.width = boxWidth;
        espBox.height = boxHeight;
        
        NSValue *val = [NSValue valueWithBytes:&espBox objCType:@encode(ESPBox)];
        [boxesMutable addObject:val];
    }

    NSLog(@"[Flork] Count: %d", countObject);
    
    self.boxes = boxesMutable;
    [self setNeedsDisplay];
}


@end

#import "esp.h"
#import <objc/runtime.h>

#define sWidth  [UIScreen mainScreen].bounds.size.width
#define sHeight [UIScreen mainScreen].bounds.size.height

uint64_t Moudule_Base = 0;
static pid_t g_GamePID = -1;

@interface ESP_View ()
@property (nonatomic, strong) CADisplayLink *displayLinkDATA;
@property (nonatomic, strong) NSMutableArray<NSValue *> *playersData;

// Floating Mod Menu UI
@property (nonatomic, strong) UIButton *floatingButton;
@property (nonatomic, strong) UIView *menuPanel;
@property (nonatomic, strong) UILabel *statusLabel;
@property (nonatomic, strong) UISwitch *boxSwitch;
@property (nonatomic, strong) UISwitch *lineSwitch;
@property (nonatomic, strong) UISwitch *nameSwitch;
@property (nonatomic, strong) UISwitch *infoSwitch;
@end

@implementation ESP_View

- (instancetype)initWithFrame:(CGRect)frame
{
    self = [super initWithFrame:frame];
    if (self) {
        self.backgroundColor = [UIColor clearColor];
        self.userInteractionEnabled = YES;

        _enableBox = YES;
        _enableLine = YES;
        _enableName = YES;
        _enableInfo = YES;

        _playersData = [NSMutableArray array];

        [self setupFloatingMenu];

        self.displayLinkDATA = [CADisplayLink displayLinkWithTarget:self selector:@selector(update_data)];
        [self.displayLinkDATA addToRunLoop:[NSRunLoop mainRunLoop] forMode:NSRunLoopCommonModes];
    }
    return self;
}

- (UIView *)hitTest:(CGPoint)point withEvent:(UIEvent *)event {
    // Expanded touch area around floating button for easy tapping
    CGRect btnTouchRect = CGRectInset(self.floatingButton.frame, -20, -20);
    if (CGRectContainsPoint(btnTouchRect, point)) {
        return self;
    }
    if (!self.menuPanel.hidden && CGRectContainsPoint(self.menuPanel.frame, point)) {
        return self;
    }
    return nil; // Transparent background canvas passes touches through to Free Fire!
}

- (void)touchesEnded:(NSSet<UITouch *> *)touches withEvent:(UIEvent *)event {
    UITouch *touch = [touches anyObject];
    if (!touch) return;
    CGPoint pt = [touch locationInView:self];

    // Check tap on floating button
    CGRect btnTouchRect = CGRectInset(self.floatingButton.frame, -20, -20);
    if (CGRectContainsPoint(btnTouchRect, pt)) {
        [self toggleMenu];
        return;
    }

    // Check tap inside menu panel when open
    if (!self.menuPanel.hidden) {
        CGPoint menuPt = [touch locationInView:self.menuPanel];
        CGFloat menuW = self.menuPanel.bounds.size.width;
        CGFloat menuH = self.menuPanel.bounds.size.height;

        if (CGRectContainsPoint(self.menuPanel.bounds, menuPt)) {
            // Close button area (top right)
            if (menuPt.x >= menuW - 50 && menuPt.y <= 45) {
                [self toggleMenu];
                return;
            }

            // Rescan button area (bottom)
            if (menuPt.y >= menuH - 50) {
                [self rescanGameProcess];
                return;
            }

            // Feature rows (y between 80 and 260)
            if (menuPt.y >= 80 && menuPt.y <= 260) {
                int index = (menuPt.y - 80) / 44;
                if (index >= 0 && index < 4) {
                    UISwitch *sw = nil;
                    if (index == 0) { self.enableBox = !self.enableBox; sw = self.boxSwitch; }
                    else if (index == 1) { self.enableLine = !self.enableLine; sw = self.lineSwitch; }
                    else if (index == 2) { self.enableName = !self.enableName; sw = self.nameSwitch; }
                    else if (index == 3) { self.enableInfo = !self.enableInfo; sw = self.infoSwitch; }

                    if (sw) [sw setOn:!sw.isOn animated:YES];
                    [self setNeedsDisplay];
                    return;
                }
            }
        }
    }
}

- (void)setupFloatingMenu {
    // 1. Floating Draggable Icon Button
    self.floatingButton = [UIButton buttonWithType:UIButtonTypeCustom];
    self.floatingButton.frame = CGRectMake(30, 80, 52, 52);
    self.floatingButton.backgroundColor = [UIColor colorWithRed:0.08 green:0.12 blue:0.22 alpha:0.92];
    self.floatingButton.layer.cornerRadius = 26;
    self.floatingButton.layer.borderColor = [UIColor colorWithRed:0.0 green:0.8 blue:1.0 alpha:0.9].CGColor;
    self.floatingButton.layer.borderWidth = 2.0;
    self.floatingButton.layer.shadowColor = [UIColor colorWithRed:0.0 green:0.8 blue:1.0 alpha:0.7].CGColor;
    self.floatingButton.layer.shadowOffset = CGSizeZero;
    self.floatingButton.layer.shadowRadius = 8.0;
    self.floatingButton.layer.shadowOpacity = 1.0;
    [self.floatingButton setTitle:@"⚡" forState:UIControlStateNormal];
    [self.floatingButton setTitleColor:[UIColor whiteColor] forState:UIControlStateNormal];
    self.floatingButton.titleLabel.font = [UIFont boldSystemFontOfSize:24];
    [self.floatingButton addTarget:self action:@selector(toggleMenu) forControlEvents:UIControlEventTouchUpInside];
    [self addSubview:self.floatingButton];

    UIPanGestureRecognizer *pan = [[UIPanGestureRecognizer alloc] initWithTarget:self action:@selector(handlePan:)];
    [self.floatingButton addGestureRecognizer:pan];

    // 2. Floating Mod Menu Panel Window
    CGFloat menuW = 290;
    CGFloat menuH = 320;
    self.menuPanel = [[UIView alloc] initWithFrame:CGRectMake((sWidth - menuW) / 2, (sHeight - menuH) / 2, menuW, menuH)];
    self.menuPanel.backgroundColor = [UIColor colorWithRed:0.08 green:0.10 blue:0.16 alpha:0.95];
    self.menuPanel.layer.cornerRadius = 16.0;
    self.menuPanel.layer.borderColor = [UIColor colorWithRed:0.0 green:0.8 blue:1.0 alpha:0.8].CGColor;
    self.menuPanel.layer.borderWidth = 1.5;
    self.menuPanel.layer.shadowColor = [UIColor blackColor].CGColor;
    self.menuPanel.layer.shadowOffset = CGSizeMake(0, 5);
    self.menuPanel.layer.shadowOpacity = 0.6;
    self.menuPanel.layer.shadowRadius = 12.0;
    self.menuPanel.hidden = YES;
    [self addSubview:self.menuPanel];

    // Title Bar
    UILabel *headerTitle = [[UILabel alloc] initWithFrame:CGRectMake(16, 12, 210, 24)];
    headerTitle.text = @"⚡ AOTFORM ESP MENU";
    headerTitle.textColor = [UIColor colorWithRed:0.2 green:0.85 blue:1.0 alpha:1.0];
    headerTitle.font = [UIFont boldSystemFontOfSize:15];
    [self.menuPanel addSubview:headerTitle];

    UIButton *closeBtn = [UIButton buttonWithType:UIButtonTypeCustom];
    closeBtn.frame = CGRectMake(menuW - 38, 10, 28, 28);
    [closeBtn setTitle:@"✕" forState:UIControlStateNormal];
    [closeBtn setTitleColor:[UIColor colorWithWhite:0.7 alpha:1.0] forState:UIControlStateNormal];
    closeBtn.titleLabel.font = [UIFont boldSystemFontOfSize:18];
    [closeBtn addTarget:self action:@selector(toggleMenu) forControlEvents:UIControlEventTouchUpInside];
    [self.menuPanel addSubview:closeBtn];

    // Separator line
    UIView *divider = [[UIView alloc] initWithFrame:CGRectMake(12, 42, menuW - 24, 1)];
    divider.backgroundColor = [UIColor colorWithWhite:0.25 alpha:0.5];
    [self.menuPanel addSubview:divider];

    // Status Badge
    self.statusLabel = [[UILabel alloc] initWithFrame:CGRectMake(14, 48, menuW - 28, 34)];
    self.statusLabel.numberOfLines = 2;
    self.statusLabel.textColor = [UIColor yellowColor];
    self.statusLabel.font = [UIFont systemFontOfSize:11];
    self.statusLabel.text = @"🔴 Searching for Free Fire process...";
    [self.menuPanel addSubview:self.statusLabel];

    // Feature Toggle Rows
    NSArray *titles = @[@"Khung ESP (Box 2D)", @"Đường Kẻ (SnapLine)", @"Tên Người Chơi (Name)", @"Máu & Khoảng Cách (HP/Dist)"];
    NSArray *selectors = @[@"boxChanged:", @"lineChanged:", @"nameChanged:", @"infoChanged:"];
    NSMutableArray *switches = [NSMutableArray array];

    for (int i = 0; i < 4; i++) {
        CGFloat yPos = 90 + i * 44;
        UILabel *label = [[UILabel alloc] initWithFrame:CGRectMake(16, yPos + 4, 180, 24)];
        label.text = titles[i];
        label.textColor = [UIColor whiteColor];
        label.font = [UIFont systemFontOfSize:13 weight:UIFontWeightMedium];
        [self.menuPanel addSubview:label];

        UISwitch *sw = [[UISwitch alloc] initWithFrame:CGRectMake(menuW - 66, yPos, 0, 0)];
        sw.on = YES;
        sw.onTintColor = [UIColor colorWithRed:0.0 green:0.7 blue:1.0 alpha:1.0];
        [sw addTarget:self action:NSSelectorFromString(selectors[i]) forControlEvents:UIControlEventValueChanged];
        [self.menuPanel addSubview:sw];
        [switches addObject:sw];
    }

    self.boxSwitch = switches[0];
    self.lineSwitch = switches[1];
    self.nameSwitch = switches[2];
    self.infoSwitch = switches[3];

    // Rescan Base Button
    UIButton *rescanBtn = [UIButton buttonWithType:UIButtonTypeCustom];
    rescanBtn.frame = CGRectMake(14, menuH - 44, menuW - 28, 32);
    rescanBtn.backgroundColor = [UIColor colorWithRed:0.14 green:0.22 blue:0.35 alpha:0.9];
    rescanBtn.layer.cornerRadius = 8.0;
    rescanBtn.layer.borderColor = [UIColor colorWithRed:0.2 green:0.7 blue:1.0 alpha:0.6].CGColor;
    rescanBtn.layer.borderWidth = 1.0;
    [rescanBtn setTitle:@"🔄 Quét Lại Game (Rescan Base)" forState:UIControlStateNormal];
    [rescanBtn setTitleColor:[UIColor colorWithRed:0.4 green:0.85 blue:1.0 alpha:1.0] forState:UIControlStateNormal];
    rescanBtn.titleLabel.font = [UIFont systemFontOfSize:12 weight:UIFontWeightBold];
    [rescanBtn addTarget:self action:@selector(rescanGameProcess) forControlEvents:UIControlEventTouchUpInside];
    [self.menuPanel addSubview:rescanBtn];
}

- (void)toggleMenu {
    self.menuPanel.hidden = !self.menuPanel.hidden;
}

- (void)handlePan:(UIPanGestureRecognizer *)pan {
    CGPoint translation = [pan translationInView:self];
    CGPoint newCenter = CGPointMake(pan.view.center.x + translation.x, pan.view.center.y + translation.y);
    newCenter.x = MAX(30, MIN(self.bounds.size.width - 30, newCenter.x));
    newCenter.y = MAX(30, MIN(self.bounds.size.height - 30, newCenter.y));
    pan.view.center = newCenter;
    [pan setTranslation:CGPointZero inView:self];
}

- (void)boxChanged:(UISwitch *)sender  { self.enableBox = sender.isOn;  [self setNeedsDisplay]; }
- (void)lineChanged:(UISwitch *)sender { self.enableLine = sender.isOn; [self setNeedsDisplay]; }
- (void)nameChanged:(UISwitch *)sender { self.enableName = sender.isOn; [self setNeedsDisplay]; }
- (void)infoChanged:(UISwitch *)sender { self.enableInfo = sender.isOn; [self setNeedsDisplay]; }

- (void)rescanGameProcess {
    Moudule_Base = 0;
    g_GamePID = -1;
    [self update_data];
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
        dispatch_async(dispatch_get_main_queue(), ^{
            self.statusLabel.textColor = [UIColor colorWithRed:1.0 green:0.4 blue:0.4 alpha:1.0];
            self.statusLabel.text = @"🔴 Chưa tìm thấy tiến trình Free Fire\n(Đang chờ mở game...)";
        });
        [self.playersData removeAllObjects];
        dispatch_async(dispatch_get_main_queue(), ^{
            [self setNeedsDisplay];
        });
        return;
    }

    uint64_t matchGame = getMatchGame(Moudule_Base);
    if (!isVaildPtr(matchGame)) {
        dispatch_async(dispatch_get_main_queue(), ^{
            self.statusLabel.textColor = [UIColor yellowColor];
            self.statusLabel.text = [NSString stringWithFormat:@"🟡 Đã kết nối PID: %d | Base: 0x%llX\n(Chờ vào trận đấu...)", g_GamePID, (unsigned long long)Moudule_Base];
        });
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
        dispatch_async(dispatch_get_main_queue(), ^{
            self.statusLabel.textColor = [UIColor yellowColor];
            self.statusLabel.text = [NSString stringWithFormat:@"🟡 Đã kết nối PID: %d\n(Tải dữ liệu trận đấu...)", g_GamePID];
        });
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

    dispatch_async(dispatch_get_main_queue(), ^{
        self.statusLabel.textColor = [UIColor colorWithRed:0.0 green:1.0 blue:0.5 alpha:1.0];
        self.statusLabel.text = [NSString stringWithFormat:@"🟢 In-Game (PID: %d)\n(Đã phát hiện: %d địch)", g_GamePID, (int)dataMutable.count];
    });

    self.playersData = dataMutable;
    dispatch_async(dispatch_get_main_queue(), ^{
        [self setNeedsDisplay];
    });
}

- (void)drawRect:(CGRect)rect {
    [super drawRect:rect];

    CGContextRef ctx = UIGraphicsGetCurrentContext();
    if (!ctx) return;

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

#ifndef esp_h
#define esp_h

#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>
#import "../Core/GameLogic.h"

struct ESPPlayerData {
    Vector3 headPos;
    Vector3 feetPos;
    float width;
    float height;
    float distance;
    int curHP;
    int maxHP;
    char name[64];
};

@interface ESP_View : UIView

- (instancetype)initWithFrame:(CGRect)frame;
- (void)update_data;
@end

#endif

//
//  HUDMainWindow.mm
//  TrollSpeed
//
//  Created by Lessica on 2024/1/24.
//

#import "HUDMainWindow.h"

@implementation HUDMainWindow

+ (BOOL)_isSystemWindow { return YES; }
- (BOOL)_isWindowServerHostingManaged { return NO; }
- (BOOL)_isSecure { return YES; }
- (BOOL)_shouldCreateContextAsSecure { return YES; }

- (UIView *)hitTest:(CGPoint)point withEvent:(UIEvent *)event {
    return nil; // Pass 100% of touch events through to Free Fire!
}

- (BOOL)pointInside:(CGPoint)point withEvent:(UIEvent *)event {
    return NO; // Pass 100% of touch events through to Free Fire!
}

@end

import SwiftUI
#if canImport(UIKit)
import UIKit
#endif

struct MainDashboardView: View {
    @Binding var isLoggedIn: Bool
    @Binding var userKey: String
    @Binding var remainingSeconds: Int
    @Binding var pcServerUrl: String
    
    @ObservedObject var vpnManager = VPNManager.shared
    
    @State private var toastMessage: String = ""
    @State private var showToast: Bool = false
    @State private var timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()
    
    // Links generated from PC server
    var teleLink: String { "\(pcServerUrl)/tele" }
    var freezeLink: String { "\(pcServerUrl)/freeze" }
    var ghostLink: String { "\(pcServerUrl)/ghost" }
    
    var body: some View {
        ZStack {
            // Dark OLED Gradient Background
            LinearGradient(
                gradient: Gradient(colors: [Color(hex: "05070e"), Color(hex: "090d16"), Color(hex: "05070e")]),
                startPoint: .top,
                endPoint: .bottom
            )
            .ignoresSafeArea()
            
            ScrollView(showsIndicators: false) {
                VStack(spacing: 20) {
                    
                    // Header Bar
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            HStack(spacing: 6) {
                                Circle()
                                    .fill(vpnManager.isConnected ? Color(hex: "00e676") : Color(hex: "ff3366"))
                                    .frame(width: 8, height: 8)
                                
                                Text(vpnManager.isConnected ? "CONNECTED TO PC" : "DISCONNECTED")
                                    .font(.system(size: 11, weight: .bold))
                                    .foregroundColor(vpnManager.isConnected ? Color(hex: "00e676") : Color(hex: "ff3366"))
                            }
                            
                            Text("HOANGHA VIP DASHBOARD")
                                .font(.system(size: 20, weight: .black, design: .rounded))
                                .foregroundColor(.white)
                        }
                        
                        Spacer()
                        
                        Button(action: { isLoggedIn = false }) {
                            Image(systemName: "power")
                                .font(.system(size: 16, weight: .bold))
                                .foregroundColor(Color(hex: "ff3366"))
                                .padding(12)
                                .background(Color(hex: "ff3366").opacity(0.12))
                                .clipShape(Circle())
                        }
                    }
                    .padding(.horizontal, 20)
                    .padding(.top, 15)
                    
                    // Card 1: Key Realtime Expiration Timer
                    VStack(alignment: .leading, spacing: 12) {
                        HStack {
                            Image(systemName: "clock.badge.checkmark.fill")
                                .foregroundColor(Color(hex: "00ffd2"))
                            Text("THỜI GIAN KEY REALTIME")
                                .font(.system(size: 12, weight: .bold))
                                .foregroundColor(Color(hex: "8e9baa"))
                            Spacer()
                            Text("VIP ACTIVE")
                                .font(.system(size: 10, weight: .bold))
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(Color(hex: "00ffd2").opacity(0.15))
                                .foregroundColor(Color(hex: "00ffd2"))
                                .cornerRadius(8)
                        }
                        
                        Text(formatTime(seconds: remainingSeconds))
                            .font(.system(size: 28, weight: .bold, design: .monospaced))
                            .foregroundColor(Color(hex: "00ffd2"))
                            .shadow(color: Color(hex: "00ffd2").opacity(0.4), radius: 8, x: 0, y: 0)
                        
                        HStack {
                            Text("Key: \(userKey)")
                                .font(.system(size: 12, weight: .semibold, design: .monospaced))
                                .foregroundColor(Color(hex: "64748b"))
                            Spacer()
                            Button(action: { copyToClipboard(userKey, label: "License Key") }) {
                                Image(systemName: "doc.on.doc")
                                    .font(.system(size: 12))
                                    .foregroundColor(Color(hex: "00ffd2"))
                            }
                        }
                    }
                    .padding(18)
                    .background(Color(hex: "0d1321").opacity(0.7))
                    .cornerRadius(18)
                    .overlay(
                        RoundedRectangle(cornerRadius: 18)
                            .stroke(Color(hex: "00ffd2").opacity(0.2), lineWidth: 1)
                    )
                    .padding(.horizontal, 20)
                    
                    // Card 2: VPN Route Control & Downloader
                    VStack(alignment: .leading, spacing: 14) {
                        HStack {
                            Image(systemName: "network.badge.shield.half.filled")
                                .foregroundColor(Color(hex: "00b0ff"))
                            Text("LUỒNG ĐI QUA VPN SERVER PC")
                                .font(.system(size: 12, weight: .bold))
                                .foregroundColor(Color(hex: "8e9baa"))
                        }
                        
                        Text(vpnManager.statusMessage)
                            .font(.system(size: 13, weight: .medium))
                            .foregroundColor(.white)
                        
                        Button(action: installVPN) {
                            HStack {
                                if vpnManager.isDownloadingProfile {
                                    ProgressView().progressViewStyle(CircularProgressViewStyle(tint: .white))
                                } else {
                                    Image(systemName: vpnManager.isConnected ? "checkmark.circle.fill" : "arrow.down.doc.fill")
                                    Text(vpnManager.isConnected ? "ĐÃ CÀI ĐẶT & KẾT NỐI VPN" : "TẢI VPN ĐI QUA SERVER PC")
                                        .font(.system(size: 14, weight: .bold))
                                }
                            }
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 14)
                            .background(vpnManager.isConnected ? Color(hex: "238636") : Color(hex: "00b0ff"))
                            .foregroundColor(.white)
                            .cornerRadius(12)
                        }
                    }
                    .padding(18)
                    .background(Color(hex: "0d1321").opacity(0.7))
                    .cornerRadius(18)
                    .overlay(
                        RoundedRectangle(cornerRadius: 18)
                            .stroke(Color(hex: "00b0ff").opacity(0.2), lineWidth: 1)
                    )
                    .padding(.horizontal, 20)
                    
                    // Card 3: 3-Mode Link Converter & Copy Links
                    VStack(alignment: .leading, spacing: 16) {
                        HStack {
                            Image(systemName: "link.circle.fill")
                                .foregroundColor(Color(hex: "9d4edd"))
                            Text("BỘ CHUYỂN ĐỔI & COPY 3 CHẾ ĐỘ LINK")
                                .font(.system(size: 12, weight: .bold))
                                .foregroundColor(Color(hex: "8e9baa"))
                        }
                        
                        // Mode 1: TeleKill Link
                        LinkRowView(
                            title: "⚡ TELEKILL BURST LINK",
                            urlStr: teleLink,
                            badgeColor: Color(hex: "ff4500"),
                            onCopy: { copyToClipboard(teleLink, label: "TeleKill Link") }
                        )
                        
                        // Mode 2: Freeze Link
                        LinkRowView(
                            title: "🧊 FREEZE ĐỊCH LINK",
                            urlStr: freezeLink,
                            badgeColor: Color(hex: "00aaff"),
                            onCopy: { copyToClipboard(freezeLink, label: "Freeze Link") }
                        )
                        
                        // Mode 3: Ghost Lag Link
                        LinkRowView(
                            title: "👻 GHOST LAG LINK",
                            urlStr: ghostLink,
                            badgeColor: Color(hex: "c084fc"),
                            onCopy: { copyToClipboard(ghostLink, label: "Ghost Link") }
                        )
                    }
                    .padding(18)
                    .background(Color(hex: "0d1321").opacity(0.7))
                    .cornerRadius(18)
                    .overlay(
                        RoundedRectangle(cornerRadius: 18)
                            .stroke(Color(hex: "9d4edd").opacity(0.2), lineWidth: 1)
                    )
                    .padding(.horizontal, 20)
                    
                    Spacer().frame(height: 30)
                }
            }
            
            // Toast Notification Overlay
            if showToast {
                VStack {
                    Spacer()
                    Text(toastMessage)
                        .font(.system(size: 13, weight: .bold))
                        .foregroundColor(Color(hex: "00ffd2"))
                        .padding(.horizontal, 20)
                        .padding(.vertical, 12)
                        .background(Color(hex: "0d1321").opacity(0.95))
                        .cornerRadius(25)
                        .overlay(
                            RoundedRectangle(cornerRadius: 25)
                                .stroke(Color(hex: "00ffd2"), lineWidth: 1)
                        )
                        .shadow(color: Color.black.opacity(0.5), radius: 10, x: 0, y: 5)
                        .padding(.bottom, 30)
                }
                .transition(.move(edge: .bottom).combined(with: .opacity))
            }
        }
        .onReceive(timer) { _ in
            if remainingSeconds > 0 {
                remainingSeconds -= 1
            }
        }
    }
    
    private func installVPN() {
        vpnManager.downloadAndInstallVPNProfile(serverUrl: pcServerUrl) { success in
            if success {
                triggerToast("Đã tải VPN & đồng bộ thiết bị thành công!")
            }
        }
    }
    
    private func copyToClipboard(_ text: String, label: String) {
        #if canImport(UIKit)
        UIPasteboard.general.string = text
        #endif
        triggerToast("Đã copy \(label)!")
    }
    
    private func triggerToast(_ msg: String) {
        toastMessage = msg
        withAnimation { showToast = true }
        DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
            withAnimation { showToast = false }
        }
    }
    
    private func formatTime(seconds: Int) -> String {
        let days = seconds / 86400
        let hours = (seconds % 86400) / 3600
        let mins = (seconds % 3600) / 60
        let secs = seconds % 60
        return String(format: "%02dd %02dh %02dm %02ds", days, hours, mins, secs)
    }
}

// Subview for Link Row
struct LinkRowView: View {
    let title: String
    let urlStr: String
    let badgeColor: Color
    let onCopy: () -> Void
    
    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack {
                Text(title)
                    .font(.system(size: 11, weight: .bold))
                    .foregroundColor(badgeColor)
                Spacer()
                Button(action: onCopy) {
                    HStack(spacing: 4) {
                        Image(systemName: "doc.on.doc.fill")
                            .font(.system(size: 10))
                        Text("COPY LINK")
                            .font(.system(size: 10, weight: .bold))
                    }
                    .padding(.horizontal, 10)
                    .padding(.vertical, 6)
                    .background(badgeColor.opacity(0.18))
                    .foregroundColor(badgeColor)
                    .cornerRadius(8)
                }
            }
            
            Text(urlStr)
                .font(.system(size: 12, weight: .medium, design: .monospaced))
                .foregroundColor(Color(hex: "94a3b8"))
                .lineLimit(1)
                .padding(10)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Color(hex: "05070e").opacity(0.6))
                .cornerRadius(8)
        }
    }
}

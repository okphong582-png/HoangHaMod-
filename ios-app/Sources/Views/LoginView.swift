import SwiftUI

struct LoginView: View {
    @Binding var isLoggedIn: Bool
    @Binding var userKey: String
    @Binding var remainingSeconds: Int
    @Binding var pcServerUrl: String
    
    @State private var inputKey: String = ""
    @State private var inputServerUrl: String = "https://hoangha.loca.lt"
    @State private var errorMessage: String = ""
    @State private var isLoading: Bool = false
    
    var body: some View {
        ZStack {
            // Dark OLED Background
            LinearGradient(
                gradient: Gradient(colors: [Color(hex: "05070e"), Color(hex: "0b0f19"), Color(hex: "05070e")]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            VStack(spacing: 25) {
                Spacer()
                
                // Brand Header
                VStack(spacing: 10) {
                    ZStack {
                        Circle()
                            .fill(Color(hex: "00ffd2").opacity(0.12))
                            .frame(width: 90, height: 90)
                        
                        Image(systemName: "shield.bolt.fill")
                            .font(.system(size: 42, weight: .bold))
                            .foregroundColor(Color(hex: "00ffd2"))
                    }
                    
                    Text("HOANGHA MOD VIP")
                        .font(.system(size: 26, weight: .black, design: .rounded))
                        .foregroundColor(.white)
                        .tracking(1.2)
                    
                    Text("Hệ Thống Quản Lý VPN & Lag Flow Control")
                        .font(.system(size: 13, weight: .medium))
                        .foregroundColor(Color(hex: "8e9baa"))
                }
                
                // Login Card
                VStack(spacing: 18) {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("LICENSE KEY")
                            .font(.system(size: 11, weight: .bold))
                            .foregroundColor(Color(hex: "00ffd2"))
                            .tracking(1)
                        
                        HStack {
                            Image(systemName: "key.fill")
                                .foregroundColor(Color(hex: "64748b"))
                            
                            TextField("Nhập License Key...", text: $inputKey)
                                .font(.system(size: 14, weight: .bold, design: .monospaced))
                                .foregroundColor(.white)
                                .autocapitalization(.allCharacters)
                                .disableAutocorrection(true)
                        }
                        .padding()
                        .background(Color(hex: "0d1321").opacity(0.8))
                        .cornerRadius(12)
                        .overlay(
                            RoundedRectangle(cornerRadius: 12)
                                .stroke(Color(hex: "00ffd2").opacity(0.3), lineWidth: 1)
                        )
                    }
                    
                    VStack(alignment: .leading, spacing: 8) {
                        Text("PC SERVER URL")
                            .font(.system(size: 11, weight: .bold))
                            .foregroundColor(Color(hex: "00b0ff"))
                            .tracking(1)
                        
                        HStack {
                            Image(systemName: "desktopcomputer")
                                .foregroundColor(Color(hex: "64748b"))
                            
                            TextField("https://...", text: $inputServerUrl)
                                .font(.system(size: 14, weight: .medium))
                                .foregroundColor(.white)
                                .autocapitalization(.none)
                                .disableAutocorrection(true)
                        }
                        .padding()
                        .background(Color(hex: "0d1321").opacity(0.8))
                        .cornerRadius(12)
                        .overlay(
                            RoundedRectangle(cornerRadius: 12)
                                .stroke(Color(hex: "00b0ff").opacity(0.3), lineWidth: 1)
                        )
                    }
                    
                    if !errorMessage.isEmpty {
                        Text(errorMessage)
                            .font(.system(size: 12, weight: .semibold))
                            .foregroundColor(Color(hex: "ff3366"))
                    }
                    
                    Button(action: validateKey) {
                        HStack {
                            if isLoading {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle(tint: .black))
                            } else {
                                Image(systemName: "lock.open.fill")
                                Text("ĐĂNG NHẬP HỆ THỐNG")
                                    .font(.system(size: 15, weight: .bold))
                            }
                        }
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 16)
                        .background(
                            LinearGradient(
                                gradient: Gradient(colors: [Color(hex: "00ffd2"), Color(hex: "00b0ff")]),
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                        .foregroundColor(Color(hex: "05070e"))
                        .cornerRadius(14)
                        .shadow(color: Color(hex: "00ffd2").opacity(0.3), radius: 10, x: 0, y: 4)
                    }
                    .disabled(isLoading)
                }
                .padding(24)
                .background(Color(hex: "0d1321").opacity(0.6))
                .cornerRadius(20)
                .overlay(
                    RoundedRectangle(cornerRadius: 20)
                        .stroke(Color.white.opacity(0.1), lineWidth: 1)
                )
                .padding(.horizontal, 20)
                
                Spacer()
                
                Text("Protected by HoangHa Security Engine • v3.0")
                    .font(.system(size: 11, weight: .medium))
                    .foregroundColor(Color(hex: "475569"))
                    .padding(.bottom, 10)
            }
        }
    }
    
    private func validateKey() {
        let trimmedKey = inputKey.trimmingCharacters(in: .whitespaces)
        guard !trimmedKey.isEmpty else {
            errorMessage = "Vui lòng nhập License Key!"
            return
        }
        
        isLoading = true
        errorMessage = ""
        
        var calculatedSeconds = 86400 * 7 // Default 7 days
        let keyLower = trimmedKey.lowercased()
        if keyLower.contains("1d") || keyLower.contains("1day") {
            calculatedSeconds = 86400
        } else if keyLower.contains("7d") || keyLower.contains("7day") || keyLower.contains("week") {
            calculatedSeconds = 86400 * 7
        } else if keyLower.contains("30d") || keyLower.contains("30day") || keyLower.contains("month") {
            calculatedSeconds = 86400 * 30
        }
        
        let cleanServerUrl = inputServerUrl.trimmingCharacters(in: .whitespaces)
        let verifyEndpoint = "\(cleanServerUrl)/api/verify_key?key=\(trimmedKey)"
        
        if let verifyUrl = URL(string: verifyEndpoint) {
            var request = URLRequest(url: verifyUrl)
            request.timeoutInterval = 4.0
            
            let task = URLSession.shared.dataTask(with: request) { data, response, error in
                DispatchQueue.main.async {
                    self.isLoading = false
                    if let data = data,
                       let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                       let remSec = json["remaining_seconds"] as? Int, remSec > 0 {
                        self.remainingSeconds = remSec
                    } else {
                        self.remainingSeconds = calculatedSeconds
                    }
                    self.userKey = trimmedKey
                    self.pcServerUrl = cleanServerUrl
                    self.isLoggedIn = true
                }
            }
            task.resume()
        } else {
            self.isLoading = false
            self.remainingSeconds = calculatedSeconds
            self.userKey = trimmedKey
            self.pcServerUrl = cleanServerUrl
            self.isLoggedIn = true
        }
    }
}

// Color Hex Extension
extension Color {
    init(hex: String) {
        let scanner = Scanner(string: hex)
        _ = scanner.scanString("#")
        var rgb: UInt64 = 0
        scanner.scanHexInt64(&rgb)
        let r = Double((rgb >> 16) & 0xFF) / 255.0
        let g = Double((rgb >> 8) & 0xFF) / 255.0
        let b = Double(rgb & 0xFF) / 255.0
        self.init(red: r, green: g, blue: b)
    }
}

import type { Metadata } from "next";
import { Inter, Tajawal } from "next/font/google"; // Placeholder logic for Tajawal import if not strictly available via next/font yet
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
// Ideally Tajawal if available
// const tajawal = Tajawal({ subsets: ["arabic"], variable: "--font-tajawal", weight: ["400", "700"] });

export const metadata: Metadata = {
  title: "UAE PASS | Digital Identity",
  description: "Secure Digital Identity for UAE",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} antialiased min-h-screen bg-uae-gray`}>
        {/* Navbar */}
        <header className="border-b bg-white border-uae-gold/20 sticky top-0 z-50">
          <div className="container mx-auto px-4 h-16 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-uae-gold rounded-full flex items-center justify-center text-white font-bold">
                U
              </div>
              <span className="font-bold text-lg tracking-tight">UAE PASS</span>
            </div>
            <nav className="flex gap-4">
              <button className="text-sm font-medium hover:text-uae-gold">عربي</button>
            </nav>
          </div>
        </header>

        <main>{children}</main>

        <footer className="py-6 text-center text-sm text-uae-dark-gray/60">
          © {new Date().getFullYear()} UAE PASS. All rights reserved.
        </footer>
      </body>
    </html>
  );
}

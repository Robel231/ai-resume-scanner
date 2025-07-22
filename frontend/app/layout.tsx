// frontend/app/layout.tsx

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { AuthProvider } from "./contexts/AuthContext"; // We need this

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Resume Scanner",
  description: "Get instant feedback on your resume",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    // Add suppressHydrationWarning here to fix the error
    <html lang="en" suppressHydrationWarning={true}>
      <body className={inter.className}>
        {/* The AuthProvider needs to be inside the body */}
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
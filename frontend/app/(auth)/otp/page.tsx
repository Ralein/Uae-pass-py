"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export default function OTPPage() {
    const [otp, setOtp] = useState(["", "", "", "", "", ""]);
    const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

    useEffect(() => {
        if (inputRefs.current[0]) {
            inputRefs.current[0].focus();
        }
    }, []);

    const handleChange = (index: number, value: string) => {
        if (isNaN(Number(value))) return;
        const newOtp = [...otp];
        newOtp[index] = value;
        setOtp(newOtp);

        // Focus next input
        if (value !== "" && index < 5 && inputRefs.current[index + 1]) {
            inputRefs.current[index + 1]?.focus();
        }
    };

    const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Backspace" && index > 0 && otp[index] === "") {
            inputRefs.current[index - 1]?.focus();
        }
    };

    return (
        <div className="flex items-center justify-center min-h-[calc(100vh-64px)] p-4">
            <Card className="w-full max-w-md shadow-xl border-uae-gold/10">
                <CardHeader className="text-center space-y-2">
                    <div className="w-12 h-12 bg-uae-gold/10 rounded-full flex items-center justify-center mx-auto mb-2 text-uae-gold font-bold text-xl">
                        🔒
                    </div>
                    <CardTitle className="text-2xl">Verify Identity</CardTitle>
                    <CardDescription>
                        Enter the 6-digit code sent to your mobile
                        <br />
                        <span className="font-medium text-uae-black">+971 50 *** 1234</span>
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    <div className="flex gap-2 justify-center">
                        {otp.map((digit, index) => (
                            <Input
                                key={index}
                                type="text"
                                maxLength={1}
                                value={digit}
                                onChange={(e) => handleChange(index, e.target.value)}
                                onKeyDown={(e) => handleKeyDown(index, e)}
                                ref={(el) => { inputRefs.current[index] = el }} // Correctly assigning ref
                                className="w-12 h-14 text-center text-xl font-bold border-uae-gray focus:border-uae-gold"
                            />
                        ))}
                    </div>

                    <div className="text-center">
                        <Button variant="link" className="text-sm text-muted-foreground p-0 h-auto">
                            Resend Code (59s)
                        </Button>
                    </div>
                </CardContent>
                <CardFooter className="flex flex-col gap-4">
                    <Button className="w-full" disabled={otp.some(d => d === "")}>
                        Verify
                    </Button>
                    <Button variant="ghost" className="w-full" asChild>
                        <Link href="/login">Back to Login</Link>
                    </Button>
                </CardFooter>
            </Card>
        </div>
    );
}

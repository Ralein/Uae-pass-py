"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export default function RegisterPage() {
    const [step, setStep] = useState(1);

    // Form State
    const [formData, setFormData] = useState({
        emiratesId: "",
        fullName: "",
        mobile: "",
        email: "",
        pin: "",
        confirmPin: ""
    });

    const nextStep = () => setStep(step + 1);
    const prevStep = () => setStep(step - 1);

    return (
        <div className="flex items-center justify-center min-h-[calc(100vh-64px)] p-4">
            <Card className="w-full max-w-lg shadow-xl border-uae-gold/10">
                <CardHeader className="text-center">
                    <div className="text-sm font-bold text-uae-gold uppercase tracking-wider mb-2">Step {step} of 3</div>
                    <CardTitle className="text-2xl">
                        {step === 1 && "Scan Emirates ID"}
                        {step === 2 && "Verify Contact Details"}
                        {step === 3 && "Set Secure PIN"}
                    </CardTitle>
                    <CardDescription>
                        {step === 1 && "Use your camera to scan your physical Emirates ID"}
                        {step === 2 && "We need to verify your email and mobile number"}
                        {step === 3 && "Create a 6-digit PIN for quick access"}
                    </CardDescription>
                </CardHeader>

                <CardContent>
                    {step === 1 && (
                        <div className="flex flex-col items-center gap-6 py-6 border-2 border-dashed border-uae-gray rounded-xl bg-uae-gray/20 hover:bg-uae-gray/40 transition-colors cursor-pointer" onClick={nextStep}>
                            <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center text-3xl shadow-sm">📷</div>
                            <div className="text-center">
                                <p className="font-medium">Tap to Scan Front Side</p>
                                <p className="text-xs text-muted-foreground mt-1">Or continue manually below</p>
                            </div>
                        </div>
                    )}

                    {step === 2 && (
                        <div className="space-y-4">
                            <div className="grid gap-2">
                                <label className="text-sm font-medium">Full Name (English)</label>
                                <Input defaultValue="Abdullah Al-User" />
                            </div>
                            <div className="grid gap-2">
                                <label className="text-sm font-medium">Mobile Number</label>
                                <Input defaultValue="+971 50 123 4567" />
                                <p className="text-xs text-uae-green flex items-center gap-1">✓ Verified with Telecom Provider</p>
                            </div>
                            <div className="grid gap-2">
                                <label className="text-sm font-medium">Email Address</label>
                                <Input placeholder="name@example.com" />
                            </div>
                        </div>
                    )}

                    {step === 3 && (
                        <div className="space-y-4">
                            <div className="grid gap-2">
                                <label className="text-sm font-medium">Create PIN</label>
                                <Input type="password" placeholder="••••••" maxLength={6} className="text-center text-xl tracking-widest" />
                            </div>
                            <div className="grid gap-2">
                                <label className="text-sm font-medium">Confirm PIN</label>
                                <Input type="password" placeholder="••••••" maxLength={6} className="text-center text-xl tracking-widest" />
                            </div>
                            <div className="bg-uae-gold/10 p-3 rounded-md text-xs text-uae-dark-gray">
                                PIN must not contain sequential (123456) or repeated (111111) numbers.
                            </div>
                        </div>
                    )}
                </CardContent>

                <CardFooter className="flex justify-between gap-4">
                    {step > 1 ? (
                        <Button variant="outline" onClick={prevStep}>Back</Button>
                    ) : (
                        <Button variant="ghost" asChild><Link href="/login">Cancel</Link></Button>
                    )}

                    <Button onClick={step < 3 ? nextStep : () => alert('Registration Complete!')} className="flex-1">
                        {step < 3 ? "Continue" : "Complete Registration"}
                    </Button>
                </CardFooter>
            </Card>
        </div>
    );
}

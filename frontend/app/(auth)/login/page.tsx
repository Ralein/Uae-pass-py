import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export default function LoginPage() {
    return (
        <div className="flex items-center justify-center min-h-[calc(100vh-64px)] p-4">
            <Card className="w-full max-w-md shadow-xl border-uae-gold/10">
                <CardHeader className="text-center space-y-2">
                    <div className="w-12 h-12 bg-uae-gold/10 rounded-full flex items-center justify-center mx-auto mb-2 text-uae-gold font-bold text-xl">
                        U
                    </div>
                    <CardTitle className="text-2xl">Log In</CardTitle>
                    <CardDescription>
                        Enter your Emirates ID, Email, or Phone to continue
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <label htmlFor="identifier" className="text-sm font-medium">Identifier</label>
                        <Input id="identifier" placeholder="e.g. 784-1234-1234567-1" autoFocus />
                    </div>
                </CardContent>
                <CardFooter className="flex flex-col gap-4">
                    <Button className="w-full">Continue</Button>
                    <div className="text-sm text-center text-muted-foreground">
                        Don't have an account?{" "}
                        <Link href="/register" className="text-uae-gold hover:underline font-medium">
                            Register now
                        </Link>
                    </div>
                </CardFooter>
            </Card>
        </div>
    );
}

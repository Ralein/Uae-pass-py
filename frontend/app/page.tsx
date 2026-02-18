import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] bg-uae-gray relative overflow-hidden">
      {/* Abstract Background Element */}
      <div className="absolute top-0 left-0 w-full h-full opacity-5 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-uae-gold rounded-full blur-[100px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-uae-green rounded-full blur-[100px]" />
      </div>

      <div className="z-10 text-center max-w-2xl px-6">
        <h1 className="text-5xl font-extrabold tracking-tight mb-6 bg-gradient-to-r from-uae-black to-uae-gold bg-clip-text text-transparent">
          The National Digital Identity
        </h1>
        <p className="text-lg text-uae-dark-gray mb-10 leading-relaxed">
          Access government and private sector services securely with a single digital identity.
          Sign documents, verify your identity, and manage your data.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/login">
            <Button size="lg" className="w-full sm:w-auto text-lg px-10 shadow-lg shadow-uae-gold/20">
              Login
            </Button>
          </Link>
          <Link href="/register">
            <Button variant="outline" size="lg" className="w-full sm:w-auto text-lg px-10">
              Register New Account
            </Button>
          </Link>
        </div>

        <div className="mt-16 grid grid-cols-3 gap-8 text-center opacity-80">
          <div>
            <h3 className="font-bold text-2xl text-uae-green">5M+</h3>
            <p className="text-sm">Users</p>
          </div>
          <div>
            <h3 className="font-bold text-2xl text-uae-gold">6000+</h3>
            <p className="text-sm">Services</p>
          </div>
          <div>
            <h3 className="font-bold text-2xl text-uae-black">Secure</h3>
            <p className="text-sm">Verified</p>
          </div>
        </div>
      </div>
    </div>
  );
}

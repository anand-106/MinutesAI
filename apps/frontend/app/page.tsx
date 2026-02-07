"use client";
import Link from "next/link"
import { Spotlight } from "@/components/ui/spotlight-new";
import { SignedIn, SignedOut, SignInButton, SignUpButton, UserButton } from "@clerk/nextjs";
import Image from "next/image";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#131313] relative overflow-x-hidden overflow-y-auto scrollbar scrollbar-none w-full max-w-[100vw]">
      <Spotlight />
      <div className="items-center flex flex-col absolute z-20 w-full ">
        <Header />

      <h1 className="font-bold text-8xl mt-[200px] font-young-serif text-[#7BF080]">
      AI joins your calls
      </h1>
      <h1 className="text-5xl font-semibold mt-4 font-ibm-plex-mono text-[#7BF080]">
      You get the notes
      </h1>
      <h1 className="text-xl font-gsans mt-6 text-white/70">MinutesAI joins, records, transcribes, and summarizes—so you don’t have to.</h1>
      <Link href="/dashboard">
      <button className="cursor-pointer border border-white/20 text-[#7BF080] py-3 px-5 rounded-full text-lg font-semibold mt-10 backdrop-blur-lg">
        Get Started
      </button>
      </Link>
      <div className="w-full mt-[100px]">
        <Features />
      </div>
      </div>
    </div>
  );
}

function Header(){
  return <div className="w-full px-[300px] mt-[50px] ">
    <div className="border border-white/20 backdrop-blur-3xl bg-white/5 h-[70px] rounded-full flex items-center px-10 justify-between">
      <h1 className="font-semibold font-gsans text-xl">Minutes AI</h1>
      <div className="flex items-center text-lg font-medium font-inter gap-5">
      <h1 className="cursor-pointer">Home</h1>
      <h1 className="cursor-pointer">Features</h1>
      <div className="ml-7 flex items-center gap-3 ">

      <SignedOut>
              <SignUpButton>
                <button className="text-[#7BF080] cursor-pointer">
                  Sign In
                </button>
              </SignUpButton>
            </SignedOut>
            <SignedIn>
              <UserButton />
            </SignedIn>
      </div>
      </div>
    </div>
  </div>
}

type FeatureCardProps = {
  title: string;
  description: string;
  alt: string;
  path: string;
  imageZoom?: number;
};

function FeatureCard({ title, description, alt, path, imageZoom = 1 }: FeatureCardProps) {
  return (
    <div className="w-1/2 h-[600px] p-8 flex">
      <div className="border border-white/20 backdrop-blur-xl rounded-2xl flex flex-col flex-1 gap-5 justify-center p-10 w-full">
      <div className="relative flex-1 min-h-0 rounded-lg overflow-hidden">
          <Image 
            src={path}
            alt={alt}
            fill
            className="object-contain"
            style={{ transform: `scale(${imageZoom})` }}
          />
        </div>
        <h1 className="text-[#7BF080] font-semibold font-young-serif text-4xl">
          {title}
        </h1>
        <h1 className="text-white/70 text-xl">{description}</h1>
      </div>
    </div>
  );
}

function Features() {
  const features = [
    {
      title: "Join any meeting with a link",
      description: "Paste a Google Meet (or supported) link. MinutesAI joins as a participant and stays in the background.",
      path: "/images/features/meet-join.webp",
      alt: "meet_join",
      imageZoom: .9,
    },
    {
      title: "Record and transcribe automatically",
      description: "Audio is recorded and transcribed with AI (Deepgram + Groq) so every word is searchable.",
      path: "/images/features/transcribe.webp",
      alt: "transcribe",
      imageZoom: .7,
    },
    {
      title: "AI summaries, your way",
      description: "Get brief or detailed summaries, action items, decisions, or custom formats—all in one view.",
      path: "/images/features/summary.png",
      alt: "summary",
      imageZoom: 1.25,
    },
    {
      title: "Transcript that drives the replay",
      description: "Click any part of the transcript to jump to that moment in the recording. Timestamps in summaries do the same.",
      path: "/images/features/transcript.png",
      alt: "transcript",
      imageZoom: 1,
    },
  ];

  return (
    <div className="w-full flex flex-wrap">
      {features.map((feature, index) => (
        <FeatureCard
          key={index}
          title={feature.title}
          description={feature.description}
          path={feature.path}
          alt={feature.alt}
          imageZoom={feature.imageZoom}
        />
      ))}
    </div>
  );
}

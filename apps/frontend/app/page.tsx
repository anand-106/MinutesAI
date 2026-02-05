"use client";
import Link from "next/link"
import { Spotlight } from "@/components/ui/spotlight-new";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#131313] relative overflow-x-hidden overflow-y-auto scrollbar scrollbar-none w-full max-w-[100vw]">
      <Spotlight />
      <div className="items-center flex flex-col absolute z-20 w-full ">

      <h1 className="font-bold text-8xl mt-[300px] font-young-serif text-[#7BF080]">
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

type FeatureCardProps = {
  title: string;
  description: string;
};

function FeatureCard({ title, description }: FeatureCardProps) {
  return (
    <div className="w-1/2 h-[600px] p-8 flex">
      <div className="border border-white/20 backdrop-blur-xl rounded-2xl flex flex-col flex-1 gap-5 justify-center p-10 w-full">
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
    },
    {
      title: "Record and transcribe automatically",
      description: "Audio is recorded and transcribed with AI (Deepgram + Groq) so every word is searchable.",
    },
    {
      title: "AI summaries, your way",
      description: "Get brief or detailed summaries, action items, decisions, or custom formats—all in one view.",
    },
    {
      title: "Transcript that drives the replay",
      description: "Click any part of the transcript to jump to that moment in the recording. Timestamps in summaries do the same.",
    },
  ];

  return (
    <div className="w-full flex flex-wrap">
      {features.map((feature, index) => (
        <FeatureCard key={index} title={feature.title} description={feature.description} />
      ))}
    </div>
  );
}

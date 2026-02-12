"use client"
import { useMeeting } from "@/hooks/meetings"
import 'video.js/dist/video-js.css';
import { useParams } from "next/navigation"
import { VideoPlayer, VideoPlayerHandle } from "@/app/components/videoPlayer";
import { TranscriptComp } from "@/app/components/transcript";
import { SummaryComp } from "@/app/components/Summary";
import { SignedIn, SignedOut, SignInButton, SignUpButton, UserButton } from "@clerk/nextjs";
import { useRef } from "react";


export default function MeetingPage(){
    const params = useParams()

    const videoPlayerRef = useRef<VideoPlayerHandle>(null);

    const handleSeek = (seconds: number) => {
      videoPlayerRef.current?.seekTo(seconds);
    };

    const meetingID = params.id
    const {data,error,isLoading} = useMeeting(meetingID!.toString())

    if(error){
        console.error(error)
        return <div>
            <h1>Error loading meetings</h1>
        </div>
       }
       if(isLoading)
        return <div>
            <h1>
                Loading Meetings
            </h1>
        </div>

    if(data)
    return  <div className="min-h-screen bg-black">
        <header className="flex justify-between items-center p-4 gap-4 h-16">
            <div>
            <h1 className="font-semibold text-xl font-gsans">Minutes AI</h1>
            </div>
            <div>

            <SignedOut>
              <SignInButton />
              <SignUpButton>
                <button className="bg-[#6c47ff] text-white rounded-full font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 cursor-pointer">
                  Sign Up
                </button>
              </SignUpButton>
            </SignedOut>
            <SignedIn>
              <UserButton />
            </SignedIn>
            </div>
          </header>
        <div className="px-[200px] flex gap-6">
        <div className="w-1/3">

            <VideoPlayer id={meetingID!.toString()}  ref={videoPlayerRef} />
            <TranscriptComp onSeek={handleSeek}  meet_id={meetingID!.toString()} />
        </div>
        <div className="w-1/2">
            <SummaryComp meet_id={meetingID!.toString()} onSeek={handleSeek} />
        </div>
        </div>
    </div>
}


"use client"
import { useMeeting } from "@/hooks/meetings"
import 'video.js/dist/video-js.css';
import { useParams } from "next/navigation"
import { VideoPlayer } from "@/app/components/videoPlayer";
import { TranscriptComp } from "@/app/components/transcript";
import { SummaryComp } from "@/app/components/Summary";


export default function MeetingPage(){
    const params = useParams()

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
    return  <div className="h-full w-screen">
        <h1>Meeting #{meetingID}</h1>
        <div className="px-[200px] flex">
        <div>

            <VideoPlayer id={meetingID!.toString()}  />
            <TranscriptComp  meet_id={meetingID!.toString()} />
        </div>
        <div className="w-1/2">
            <SummaryComp meet_id={meetingID!.toString()}  />
        </div>
        </div>
    </div>
}


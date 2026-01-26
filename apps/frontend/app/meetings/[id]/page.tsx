"use client"
import { useMeeting } from "@/hooks/meetings"
import { useParams } from "next/navigation"


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
    return  <div className="h-screen w-screen">
        <h1>Meeting #{meetingID}</h1>
    </div>
}
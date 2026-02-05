"use client"
import { useMeetings } from "@/hooks/meetings"
import { MeetingsList } from "@/types/types"
import Link from "next/link"
import { secondsToTimestamp } from "../utils/timestampConvert"

export function MeetingsListCard(){

    const {data,error,isLoading} = useMeetings()
 
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
     if(data){
         return <div className="flex gap-4">
             {
                 data.map(meet=>{
                     return <Link href={`meetings/${meet.id}`} key={meet.id} >
                     <MeetingCard meet={meet}  />
                     </Link> 
                 })
             }
         </div>
     }
 }
 
 function MeetingCard({meet}:{meet:MeetingsList}){
     return <div className="flex flex-col rounded-xl border-3 border-[#494C59] p-4 cursor-pointer h-[200px] w-[300px] justify-between">
        <div>

        </div>
        <div className="h-1/3">

        <h1 className="font-inter ">Meeting - {new Date(meet.created_at).toLocaleDateString()}</h1>
        <h1 className="text-[#7BF080]/70">{secondsToTimestamp(meet.duration_seconds!)}</h1>
        </div>
     </div>
 }
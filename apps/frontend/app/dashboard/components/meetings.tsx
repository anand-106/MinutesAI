"use client"
import { useMeetings } from "@/hooks/meetings"
import { MeetingsList } from "@/types/types"
import Link from "next/link"

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
         return <div className="flex">
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
     return <div className="flex flex-col rounded-xl border border-white/20 p-4 cursor-pointer">
        <h1>{new Date(meet.created_at).toLocaleDateString()}</h1>
     </div>
 }
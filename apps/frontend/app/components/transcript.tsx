import { usefetchMeetingDialouges } from "@/hooks/meetings"

export function TranscriptComp({meet_id}:{meet_id:string}){
    const {data,error,isLoading} = usefetchMeetingDialouges(meet_id)
 
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
        console.log(data)
     }
}
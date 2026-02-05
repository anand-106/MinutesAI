import { usefetchMeetingDialouges } from "@/hooks/meetings"
import { Dialouges } from "@/types/types"
import { secondsToTimestamp } from "../utils/timestampConvert"

export function TranscriptComp({meet_id,onSeek}:{meet_id:string,onSeek:(seconds:number)=>void}){
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
        return <div className="flex flex-col gap-2 p-3 overflow-hidden max-h-[60vh]">
            <h1 className="text-2xl font-gsans">TRANSCRIPT</h1>
            <div className="overflow-y-auto gap-2 flex flex-col flex-1 min-h-0 scrollbar scrollbar-track-[#0A0A0A] scrollbar-thumb-[#15171B]">

            {
                data.map(dia=>{
                    return <Dialouge onSeek={onSeek} dialouge={dia} key={dia.id} />
                })
            }
            </div>
        </div>
     }
}

function Dialouge({dialouge,onSeek}:{dialouge:Dialouges,onSeek:(seconds:number)=>void}){
return <div className="bg-[#15171B] rounded-2xl p-4 cursor-pointer"
onClick={()=>onSeek(dialouge.start_time)}
    
onMouseEnter={()=>onSeek(dialouge.start_time)}
>
    <h1 className="mb-1 text-white/70">{dialouge.speaker}</h1>
    <h1>{dialouge.text}</h1>
    <div className="flex justify-end">
        <h1>{secondsToTimestamp(dialouge.start_time)}</h1>
    </div>
</div>
}
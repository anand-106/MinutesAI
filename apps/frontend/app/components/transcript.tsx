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
        return <div className="flex flex-col gap-2 p-3">
            <h1 className="text-2xl font-gsans">TRANSCRIPT</h1>
            <div className="overflow-y-auto gap-2 flex flex-col">

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
    <h1>{dialouge.text}</h1>
    <div className="flex justify-end">
        <h1>{secondsToTimestamp(dialouge.start_time)}</h1>
    </div>
</div>
}
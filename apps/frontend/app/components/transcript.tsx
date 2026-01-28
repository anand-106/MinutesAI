import { usefetchMeetingDialouges } from "@/hooks/meetings"
import { Dialouges } from "@/types/types"

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
        return <div>
            {
                data.map(dia=>{
                    return <Dialouge dialouge={dia} key={dia.id} />
                })
            }
        </div>
     }
}

function Dialouge({dialouge}:{dialouge:Dialouges}){
return <div className="bg-white/20 rounded-2xl p-4">
    <h1>{dialouge.text}</h1>
</div>
}
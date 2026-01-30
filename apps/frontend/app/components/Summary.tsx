import { useFetchSummaries, useSummarizeMeeting } from "@/hooks/meetings"
import { SummaryOut } from "@/types/types"

export  function SummaryComp({meet_id}:{meet_id:string}){

    const {mutate,isPending,isError,data} = useSummarizeMeeting(meet_id,"detailed")
    return <div>
        <h1>Summary</h1>
        <button
        className={`cursor-pointer `}
        onClick={()=>mutate()}
        >Get Summary</button>
        <Summaries meet_id={meet_id} />
    </div>
}

function Summaries({meet_id}:{meet_id:string}){
    const {data,isLoading,error} = useFetchSummaries(meet_id)
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

            return <div>
        <div>Summary</div>
        {
            data.map((smry,idx)=>{
                return <div key={idx} >
                    <Summary smry={smry} />
                </div>
            })
        }
    </div>
    }
}

function Summary({smry}:{smry:SummaryOut}){
return <div>
    <h1>{smry.type}</h1>
    <h1>
        {
            smry.content
        }
    </h1>
</div>
}
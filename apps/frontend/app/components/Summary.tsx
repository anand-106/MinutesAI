import { useFetchSummaries, useSummarizeMeeting } from "@/hooks/meetings"
import { SummaryOut } from "@/types/types"
import Markdown from "react-markdown"
import remarkGfm from 'remark-gfm'

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

            return <div className="px-[50px]">
        <h1 className="text-2xl font-gsans">Summary</h1>
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
    {/* <h1>{smry.type}</h1> */}
    <Markdown remarkPlugins={[remarkGfm]}>{smry.content}</Markdown>
</div>
}
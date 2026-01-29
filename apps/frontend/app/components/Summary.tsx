import { useSummarizeMeeting } from "@/hooks/meetings"

export  function SummaryComp({meet_id}:{meet_id:string}){

    const {mutate,isPending,isError,data} = useSummarizeMeeting(meet_id,"detailed")
    return <div>
        <h1>Summary</h1>
        <button
        className={`cursor-pointer `}
        onClick={()=>mutate()}
        >Get Summary</button>
    </div>
}
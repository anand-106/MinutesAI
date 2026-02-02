import { useFetchSummaries, useSummarizeMeeting } from "@/hooks/meetings"
import { SummaryOut } from "@/types/types"
import Markdown from "react-markdown"
import remarkGfm from 'remark-gfm'
import { processTimeStampString } from "../utils/timestampProcess"

export  function SummaryComp({meet_id,onSeek}:{meet_id:string,onSeek:(seconds:number)=>void}){

    const {mutate,isPending,isError,data} = useSummarizeMeeting(meet_id,"detailed")
    return <div>
        <h1>Summary</h1>
        <button
        className={`cursor-pointer `}
        onClick={()=>mutate()}
        >Get Summary</button>
        <Summaries onSeek={onSeek} meet_id={meet_id} />
    </div>
}

function Summaries({meet_id,onSeek}:{meet_id:string,onSeek:(seconds:number)=>void}){
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
                    <Summary onSeek={onSeek} smry={smry} />
                </div>
            })
        }
    </div>
    }
}

function Summary({ smry ,onSeek}: { smry: SummaryOut ,onSeek:(seconds:number)=>void}) {
    const processed = smry.content.replace(/(\[\[[^\]]+\]\])/g, '`$1`');
  
    return (
      <Markdown
        remarkPlugins={[remarkGfm]}
        components={{
          code: ({ children }) => {
            const text = String(children);
            if (text.startsWith('[[') && text.endsWith(']]')) {
              return <BracketTimestamp onSeek={onSeek} value={text.slice(2, -2)} />;
            }
            return <code>{children}</code>;
          },
        }}
      >
        {processed}
      </Markdown>
    );
  }

function BracketTimestamp({value,onSeek}:{value:string,onSeek:(seconds:number)=>void}){
    return <span className="bracket-token cursor-pointer text-blue-400"
    onClick={()=>onSeek(processTimeStampString(value))}
    >{value}</span>
}
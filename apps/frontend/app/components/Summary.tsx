"use client"

import { useFetchSummaries, useSummarizeMeeting } from "@/hooks/meetings"
import Markdown from "react-markdown"
import remarkGfm from 'remark-gfm'
import { processTimeStampString } from "../utils/timestampProcess"
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { useEffect, useState } from "react"
import { useParams } from "next/navigation"

export function SummaryComp({ meet_id, onSeek }: { meet_id: string; onSeek: (seconds: number) => void }) {
    const { mutate } = useSummarizeMeeting(meet_id);
    return (
        <div>
            <Summaries onSeek={onSeek} meet_id={meet_id} />
        </div>
    );
}

function Summaries({meet_id,onSeek}:{meet_id:string,onSeek:(seconds:number)=>void}){
   
  const [smry,setSmry] = useState("")

            return <div className="px-[50px] bg-[#15171B] py-5 rounded-2xl">
              <div className="flex justify-between mb-5">

        <h1 className="text-2xl font-gsans ">Summary</h1>
        <SummaryDropDown setSmry={setSmry} items={["brief","detailed","action_items","decisions","custom"]} />
              </div>
        <Summary smry={smry} onSeek={onSeek} />
    </div>
    
}

function Summary({ smry ,onSeek}: { smry:string ,onSeek:(seconds:number)=>void}) {
    const processed = smry.replace(/(\[\[[^\]]+\]\])/g, '`$1`');
  
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



const SUMMARY_MODES = ["brief", "detailed", "action_items", "decisions", "custom"] as const;
type SummaryMode = (typeof SUMMARY_MODES)[number];

function SummaryDropDown({
    items,
    setSmry,
}: {
    items: string[];
    setSmry: React.Dispatch<React.SetStateAction<string>>;
}) {
    const [selected, setSelected] = useState(items[0]);
    const params = useParams();
    const meetingID = params.id;
    const { mutate, isPending } = useSummarizeMeeting(meetingID!.toString());

    useEffect(()=>{
      mutate({
        mode:"brief"
      },
    {
      onSuccess:(data) => setSmry(data.content ?? "")
    }
    )
    },[])

    return (
        <DropdownMenu.Root>
            <DropdownMenu.Trigger asChild>
                <button className="px-4 py-1 bg-transparent border border-white/20 text-white rounded-lg cursor-pointer">
                    {isPending ? "..." : selected}
                </button>
            </DropdownMenu.Trigger>

            <DropdownMenu.Content
                className="rounded border border-white/20 bg-[#15171B] p-2"
                sideOffset={5}
            >
                {items.map((itm, idx) => (
                    <DropdownMenu.Item
                        key={idx}
                        onSelect={() => {
                            setSelected(itm);
                            mutate(
                                { mode: itm as SummaryMode },
                                { onSuccess: (data) => setSmry(data.content ?? "") }
                            );
                        }}
                        className={`px-3 py-2 cursor-pointer rounded
                          ${selected === itm ? "bg-white/10 text-white" : "text-white/80 hover:bg-white/5"}
                        `}
                    >
                        {itm}
                    </DropdownMenu.Item>
                ))}
            </DropdownMenu.Content>
        </DropdownMenu.Root>
    );
}
"use client"
import { useMeetings } from "@/hooks/meetings"
import axiosClient from "@/lib/axiosClient"
import { useAuth } from "@clerk/nextjs"
import { useState } from "react"

export default function DashBoard(){
    return <div>
    <h1>DashBoard</h1>
    <MeetingInput />
    </div>
}

function MeetingInput(){
    const [meetLink,setMeetLink] = useState("")

    const {getToken} = useAuth()

    const sendMeetLink = async()=>{
        try{
            const token = await getToken()
            const res = await axiosClient.post('/meetings/join',{
                link:meetLink
            },{
                headers:{
                    Authorization:`Bearer ${token}`
                }
            })

            return res
        }catch(e){
            console.error(e)
        }
    }

    return <div className="">
        <div>

        <input value={meetLink} onChange={(e)=>setMeetLink(e.target.value)} placeholder="Enter meeting link" />
        <button onClick={sendMeetLink} >Enter</button>
        </div>
        <div>
            <MeetingsListCard />
        </div>
    </div>
}

function MeetingsListCard(){

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
        return <div>
            {
                data.map(meet=>{
                    return <MeetingCard meet={meet} />
                })
            }
        </div>
    }
}

function MeetingCard({meet}:{meet:MeetingsList}){
    return <div>
       <h1>{meet.key}</h1>
    </div>
}
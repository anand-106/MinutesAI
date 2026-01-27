"use client"
import axiosClient from "@/lib/axiosClient"
import { useAuth } from "@clerk/nextjs"
import { useState } from "react"
import { MeetingsListCard } from "../components/meetings"

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

    return <div className="w-screen flex flex-col">
        <div>

        <input value={meetLink} onChange={(e)=>setMeetLink(e.target.value)} placeholder="Enter meeting link" />
        <button onClick={sendMeetLink} >Enter</button>
        </div>
        <div>
            <MeetingsListCard />
        </div>
    </div>
}


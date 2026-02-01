"use client"
import axiosClient from "@/lib/axiosClient"
import { SignedIn, SignedOut, SignInButton, SignUpButton, useAuth, UserButton } from "@clerk/nextjs"
import { useState } from "react"
import { MeetingsListCard } from "../components/meetings"

export default function DashBoard(){
    return <div className="w-screen h-screen bg-[#040406]">
        
        <header className="flex justify-between items-center p-4 gap-4 h-16">
            <div>
            <h1 className="font-semibold text-xl font-gsans">Minutes AI</h1>
            </div>
            <div>

            <SignedOut>
              <SignInButton />
              <SignUpButton>
                <button className="bg-[#6c47ff] text-white rounded-full font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 cursor-pointer">
                  Sign Up
                </button>
              </SignUpButton>
            </SignedOut>
            <SignedIn>
              <UserButton />
            </SignedIn>
            </div>
          </header>
          <div className="pt-[200px] pb-[75px] flex justify-center items-center ">

    <MeetingInput />
          </div>
          <div className="w-full px-[300px]">
            <div className="mb-12">
                <h1 className=" font-semibold text-2xl font-gsans">
                    My Calls
                </h1>
            </div>

    <MeetingsListCard />
          </div>

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

    return <div className="h-[60px] border-3 border-[#494C59] rounded-full pl-7 py-1 pr-1 bg-[#131316]">
 


        <input 
        className="h-full w-[500px] outline-0 placeholder:text-[#777A88] font-normal font-inter text-[18px]"
        value={meetLink} onChange={(e)=>setMeetLink(e.target.value)} placeholder="Enter meeting link" />
        <button 
        className="bg-white text-black font-normal font-inter text-[18px] rounded-full w-[120px] h-full cursor-pointer"
        onClick={sendMeetLink} >Enter</button>

    </div>
}


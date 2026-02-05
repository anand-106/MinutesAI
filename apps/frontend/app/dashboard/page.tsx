"use client"
import axiosClient from "@/lib/axiosClient"
import { SignedIn, SignedOut, SignInButton, SignUpButton, useAuth, UserButton } from "@clerk/nextjs"
import { useState } from "react"
import { MeetingsListCard } from "../components/meetings"
import { useMutation } from "@tanstack/react-query"
import * as Dialog from "@radix-ui/react-dialog";

export default function DashBoard(){
    return <div className="w-full min-h-screen bg-[#040406]">
        
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
          <div className="pt-[150px] pb-[75px] flex flex-col gap-10 justify-center items-center ">
            <h1 className="text-7xl font-black font-gsans">Minutes AI</h1>

    <MeetingInput />
          </div>
          <div className="w-full px-[300px]">
            <div className="mb-12">
                <h1 className="text-[#7BF080] font-semibold text-2xl font-gsans">
                    My Calls
                </h1>
            </div>

    <MeetingsListCard />
          </div>

    </div>
}

function MeetingInput(){
    const [meetLink,setMeetLink] = useState("")
    const [open, setOpen] = useState(false);

    const {getToken} = useAuth()

    const sendMeetLink = async()=>{

            const token = await getToken()
            const res = await axiosClient.post('/meetings/join',{
                link:meetLink
            },{
                headers:{
                    Authorization:`Bearer ${token}`
                }
            })

            return res

    }

    const {mutate,isPending} = useMutation({
        mutationFn:sendMeetLink,
        onSuccess:()=>{
            setOpen(true)
        }
    })

    return <div className="h-[60px] border-3 border-[#494C59] rounded-full pl-7 py-1 pr-1 bg-[#131316]">
 


        <input 
        className="h-full w-[500px] outline-0 placeholder:text-[#777A88] font-normal font-inter text-[18px]"
        value={meetLink} onChange={(e)=>setMeetLink(e.target.value)} placeholder="Enter meeting link" />
        <button 
        disabled={isPending}
        className={`bg-white text-black font-normal font-inter text-[18px] rounded-full w-[120px] h-full ${isPending?"cursor-not-allowed":"cursor-pointer"}`}
        onClick={()=>mutate()} >Enter</button>

        <Dialog.Root open={open} onOpenChange={setOpen}>
        <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50" />

<Dialog.Content className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 p-6 rounded-lg">
  <Dialog.Title className="text-lg font-semibold">
    Success
  </Dialog.Title>

  <Dialog.Description className="mt-2 text-sm text-gray-600">
    MinutesAI bot is on the Way!.
  </Dialog.Description>

  <div className="mt-4 flex justify-end">
    <Dialog.Close asChild>
      <button className="px-3 py-1 rounded bg-green-600 text-white">
        OK
      </button>
    </Dialog.Close>
  </div>
</Dialog.Content>
        </Dialog.Portal>
        </Dialog.Root>

    </div>
}


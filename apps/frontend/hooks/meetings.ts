import axiosClient from "@/lib/axiosClient";
import { Dialouges, MeetingsList } from "@/types/types";
import { useAuth } from "@clerk/nextjs";
import { useQuery } from "@tanstack/react-query";


export function useMeetings(){
    
    const {getToken} = useAuth()

    const getMeetings = async () =>{
        const token = await getToken();
    
        const res  = await axiosClient.get('/meetings/',{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
    
        return res.data
    }
    

    return useQuery<MeetingsList[]>({
        queryKey:["meetings"],
        queryFn:getMeetings
    })
}

export function useMeeting(id:string){
    const {getToken} = useAuth()

    const getMeeting = async ()=>{
        const token = await getToken();
    
        const res  = await axiosClient.get(`/meetings/${id}`,{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
    
        return res.data
    }

    return useQuery<MeetingsList>({
        queryKey:[`metting_${id}`],
        queryFn:getMeeting
    })
}

export function useMeetingVideoPresign(id:string){
    const {getToken} = useAuth()

    const getMeetingPresignVideo = async ()=>{
        const token = await getToken();
    
        const res  = await axiosClient.get(`/meetings/${id}/presigned`,{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
    
        return res.data
    }

    return useQuery<{url:string}>({
        queryKey:[`metting_${id}_presign`],
        queryFn:getMeetingPresignVideo
    })
}



export function usefetchMeetingDialouges(meet_id:string){
    const {getToken} = useAuth()
    const getMettingDialouges = async ()=>{
        const token = await getToken();
    
        const res  = await axiosClient.get(`/meetings/${meet_id}/transcription`,{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
        const dialouges:Dialouges[] = res.data

        dialouges.sort((a,b)=>a.sequence-b.sequence)
        
        return dialouges
    }

    return useQuery<Dialouges[]>({
        queryKey:[`metting_${meet_id}_dialouges`],
        queryFn:getMettingDialouges
    })

}

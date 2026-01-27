import axiosClient from "@/lib/axiosClient";
import { MeetingsList } from "@/types/types";
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



import axiosClient from "@/lib/axiosClient";
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
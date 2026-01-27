"use client"
import { useMeetingVideoPresign } from "@/hooks/meetings";
import { useEffect, useRef } from "react"
import videojs from "video.js"
import 'video.js/dist/video-js.css';


export function VideoPlayer({id}:{id:string}){

    const VideoRef= useRef<HTMLVideoElement|null>(null)
    const playerRef = useRef<any>(null)

    const {data,error,isLoading} = useMeetingVideoPresign(id)

    useEffect(()=>{
        if(!VideoRef.current || !data?.url || playerRef.current) return;

        playerRef.current = videojs(VideoRef.current,
            {
                controls: true,
                preload: "metadata",
                fluid: true,
                playbackRates: [0.5, 1, 1.25, 1.5, 2],
                sources: [
                  {
                    src: data.url,
                    type: "video/mp4",
                  },
                ],
              }
        )
        return ()=>{
            if(playerRef.current){
                playerRef.current.dispose()
                playerRef.current = null
            }
        }
    }
,[data?.url]
)

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

    if(data)
    {
        console.log(data.url)
        return  <div >
       <video
       ref={VideoRef}
       id="my-player"
       className="video-js vjs-default-skin w-full h-full"
       controls
       />

       </div>
    }
}

export interface MeetingsList {
    id:string
    key:string
    link:string
    upload_id:string | null
    status: "not_started" | "uploading" | "finished"
    duration_seconds:number | null
    created_at:string
}

export interface Dialouges {
    id:string,
    meeting_id:string,
    speaker:string,
    text:string,
    start_time:number,
    end_time:number,
    sequence:number
}
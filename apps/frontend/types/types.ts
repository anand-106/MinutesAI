
export interface MeetingsList {
    id:string
    key:string
    link:string
    upload_id:string | null
    status: "not_started" | "uploading" | "finished"
    duration_seconds:number | null
    created_at:string
}
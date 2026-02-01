
export function secondsToTimestamp(seconds:number){
    const HR = Math.floor(seconds / 3600);
    const MIN = Math.floor((seconds % 3600) / 60);
    const SEC = Math.floor(seconds % 60);

    return `${String(HR).padStart(2, "0")}:${String(MIN).padStart(2, "0")}:${String(SEC).padStart(2, "0")}`;
}
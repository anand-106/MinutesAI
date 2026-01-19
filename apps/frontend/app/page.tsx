import Link from "next/link"

export default function Home() {
  return (
    <div className=" min-h-screen items-center justify-center flex flex-col">

      <h1>
        Minutes AI
      </h1>
      <Link href="/dashboard">
      <button>
        Get Started
      </button>
      </Link>
    </div>
  );
}

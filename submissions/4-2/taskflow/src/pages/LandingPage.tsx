import { Link } from "react-router"

function LandingPage() {
  return (
    <main>
      <section className="mx-auto max-w-6xl px-6 pb-20 pt-24 lg:pt-32">
        <p className="mb-5 text-sm font-semibold uppercase tracking-widest text-blue-600">
          Personal productivity
        </p>
        <h1 className="max-w-3xl text-5xl font-bold tracking-tight text-slate-950 sm:text-6xl">
          프로젝트와 할 일을
          <br />
          한 곳에서 정리하세요.
        </h1>
        <p className="mt-6 max-w-xl text-lg leading-8 text-slate-500">
          TaskFlow는 프로젝트 안의 할 일을 관리하고, 중요한 작업에 집중할 수 있도록 돕는 개인용 생산성 서비스입니다.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link
            to="/signup"
            className="rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700"
          >
            시작하기
          </Link>
          <Link
            to="/login"
            className="rounded-xl border border-slate-300 bg-white px-5 py-3 font-semibold text-slate-700 transition hover:border-slate-400"
          >
            로그인하고 둘러보기
          </Link>
        </div>
      </section>
    </main>
  )
}

export default LandingPage

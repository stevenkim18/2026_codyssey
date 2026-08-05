import { Link } from "react-router"

function LoginPage() {
  return (
    <main className="mx-auto flex min-h-[calc(100vh-73px)] max-w-md items-center px-6 py-12">
      <section className="w-full rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <p className="text-sm font-semibold text-blue-600">Welcome back</p>
        <h1 className="mt-2 text-3xl font-bold text-slate-950">로그인</h1>
        <p className="mt-2 text-sm text-slate-500">TaskFlow를 계속 사용해보세요.</p>
        <div className="mt-8 space-y-4">
          <label className="block text-sm font-medium text-slate-700">
            이메일
            <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" type="email" placeholder="you@example.com" />
          </label>
          <label className="block text-sm font-medium text-slate-700">
            비밀번호
            <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" type="password" placeholder="••••••••" />
          </label>
          <button className="w-full rounded-xl bg-slate-900 px-4 py-3 font-semibold text-white transition hover:bg-slate-700" type="button">
            로그인
          </button>
        </div>
        <p className="mt-6 text-center text-sm text-slate-500">
          계정이 없나요? <Link className="font-semibold text-blue-600" to="/signup">회원가입</Link>
        </p>
      </section>
    </main>
  )
}

export default LoginPage

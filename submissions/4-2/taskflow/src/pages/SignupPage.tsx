import { Link } from "react-router"

function SignupPage() {
  return (
    <main className="mx-auto flex min-h-[calc(100vh-73px)] max-w-md items-center px-6 py-12">
      <section className="w-full rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <p className="text-sm font-semibold text-blue-600">Create your account</p>
        <h1 className="mt-2 text-3xl font-bold text-slate-950">회원가입</h1>
        <p className="mt-2 text-sm text-slate-500">개인 프로젝트 관리를 시작해보세요.</p>
        <div className="mt-8 space-y-4">
          <label className="block text-sm font-medium text-slate-700">
            이메일
            <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" type="email" placeholder="you@example.com" />
          </label>
          <label className="block text-sm font-medium text-slate-700">
            비밀번호
            <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" type="password" placeholder="8자 이상" />
          </label>
          <label className="block text-sm font-medium text-slate-700">
            비밀번호 확인
            <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" type="password" placeholder="비밀번호를 다시 입력하세요" />
          </label>
          <button className="w-full rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700" type="button">
            회원가입
          </button>
        </div>
        <p className="mt-6 text-center text-sm text-slate-500">
          이미 계정이 있나요? <Link className="font-semibold text-blue-600" to="/login">로그인</Link>
        </p>
      </section>
    </main>
  )
}

export default SignupPage

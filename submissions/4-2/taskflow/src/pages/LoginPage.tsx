import { useState } from "react"
import { Link, Navigate, useLocation, useNavigate, useSearchParams } from "react-router"
import ErrorState from "../components/ErrorState"
import LoadingState from "../components/LoadingState"
import { useAuth } from "../contexts/useAuth"
import { getErrorMessage } from "../lib/errors"

function LoginPage() {
  const { user, isLoading, signIn } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [searchParams] = useSearchParams()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const from = (location.state as { from?: string } | null)?.from ?? "/dashboard"
  const signupComplete = searchParams.get("signup") === "complete"

  if (isLoading) {
    return <LoadingState message="로그인 상태를 확인하고 있습니다..." fullPage />
  }

  if (user) return <Navigate to="/dashboard" replace />

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError("")
    setIsSubmitting(true)

    try {
      await signIn(email.trim(), password)
      navigate(from, { replace: true })
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="mx-auto flex min-h-[calc(100vh-73px)] max-w-md items-center px-6 py-12">
      <section className="w-full rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <p className="text-sm font-semibold text-blue-600">Welcome back</p>
        <h1 className="mt-2 text-3xl font-bold text-slate-950">로그인</h1>
        <p className="mt-2 text-sm text-slate-500">TaskFlow를 계속 사용해보세요.</p>
        {signupComplete && <p className="mt-5 rounded-xl bg-emerald-50 px-4 py-3 text-sm text-emerald-700">회원가입이 완료되었습니다. 로그인해주세요.</p>}
        <form className="mt-8 space-y-4" onSubmit={(event) => void handleSubmit(event)}>
          <label className="block text-sm font-medium text-slate-700">
            이메일
            <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" type="email" placeholder="you@example.com" value={email} onChange={(event) => setEmail(event.target.value)} required autoComplete="email" />
          </label>
          <label className="block text-sm font-medium text-slate-700">
            비밀번호
            <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" type="password" placeholder="••••••••" value={password} onChange={(event) => setPassword(event.target.value)} required autoComplete="current-password" />
          </label>
          {error && <ErrorState message={error} compact />}
          <button className="w-full rounded-xl bg-slate-900 px-4 py-3 font-semibold text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-60" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "로그인 중..." : "로그인"}
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-slate-500">
          계정이 없나요? <Link className="font-semibold text-blue-600" to="/signup">회원가입</Link>
        </p>
      </section>
    </main>
  )
}

export default LoginPage

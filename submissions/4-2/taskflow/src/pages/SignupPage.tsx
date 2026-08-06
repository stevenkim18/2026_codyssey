import { useState } from "react"
import { Link, Navigate, useNavigate } from "react-router"
import ErrorState from "../components/ErrorState"
import LoadingState from "../components/LoadingState"
import { useAuth } from "../contexts/useAuth"
import { getErrorMessage } from "../lib/errors"

function SignupPage() {
  const { user, isLoading, signUp } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [passwordConfirmation, setPasswordConfirmation] = useState("")
  const [error, setError] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  if (isLoading) {
    return <LoadingState message="로그인 상태를 확인하고 있습니다..." fullPage />
  }

  if (user) return <Navigate to="/dashboard" replace />

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError("")

    if (password.length < 8) {
      setError("비밀번호는 8자 이상 입력해주세요.")
      return
    }

    if (password !== passwordConfirmation) {
      setError("비밀번호 확인이 일치하지 않습니다.")
      return
    }

    setIsSubmitting(true)
    try {
      const session = await signUp(email.trim(), password)
      navigate(session ? "/dashboard" : "/login?signup=complete", { replace: true })
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="mx-auto flex min-h-[calc(100vh-73px)] max-w-md items-center px-6 py-12">
      <section className="w-full rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <p className="text-sm font-semibold text-blue-600">Create your account</p>
        <h1 className="mt-2 text-3xl font-bold text-slate-950">회원가입</h1>
        <p className="mt-2 text-sm text-slate-500">개인 프로젝트 관리를 시작해보세요.</p>
        <form className="mt-8 space-y-4" onSubmit={(event) => void handleSubmit(event)}>
          <label className="block text-sm font-medium text-slate-700">
            이메일
            <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" type="email" placeholder="you@example.com" value={email} onChange={(event) => setEmail(event.target.value)} required autoComplete="email" />
          </label>
          <label className="block text-sm font-medium text-slate-700">
            비밀번호
            <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" type="password" placeholder="8자 이상" value={password} onChange={(event) => setPassword(event.target.value)} required autoComplete="new-password" />
          </label>
          <label className="block text-sm font-medium text-slate-700">
            비밀번호 확인
            <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" type="password" placeholder="비밀번호를 다시 입력하세요" value={passwordConfirmation} onChange={(event) => setPasswordConfirmation(event.target.value)} required autoComplete="new-password" />
          </label>
          {error && <ErrorState message={error} compact />}
          <button className="w-full rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "가입 중..." : "회원가입"}
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-slate-500">
          이미 계정이 있나요? <Link className="font-semibold text-blue-600" to="/login">로그인</Link>
        </p>
      </section>
    </main>
  )
}

export default SignupPage

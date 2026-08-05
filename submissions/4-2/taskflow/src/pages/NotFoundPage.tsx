import { Link } from "react-router"

function NotFoundPage() {
  return (
    <main className="mx-auto max-w-2xl px-6 py-24 text-center">
      <p className="text-sm font-semibold uppercase tracking-widest text-blue-600">404</p>
      <h1 className="mt-3 text-4xl font-bold text-slate-950">페이지를 찾을 수 없습니다.</h1>
      <p className="mt-4 text-slate-500">주소를 확인하거나 TaskFlow 홈으로 돌아가세요.</p>
      <Link className="mt-8 inline-flex rounded-xl bg-slate-900 px-5 py-3 font-semibold text-white hover:bg-slate-700" to="/">홈으로 이동</Link>
    </main>
  )
}

export default NotFoundPage

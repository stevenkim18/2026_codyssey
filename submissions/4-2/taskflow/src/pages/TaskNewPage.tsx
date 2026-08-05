import { Link, useParams } from "react-router"
import PageHeader from "../components/PageHeader"

function TaskNewPage() {
  const { id } = useParams()

  return (
    <main className="mx-auto max-w-2xl px-6 py-10">
      <PageHeader eyebrow={`Project ${id ?? ""}`} title="새 할 일" description="프로젝트에 새로운 할 일을 추가합니다." />
      <form className="space-y-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm" onSubmit={(event) => event.preventDefault()}>
        <label className="block text-sm font-medium text-slate-700">
          할 일 제목
          <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" required placeholder="예: React 라우팅 공부하기" />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          설명
          <textarea className="mt-2 min-h-32 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" placeholder="할 일에 대한 설명을 입력하세요." />
        </label>
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block text-sm font-medium text-slate-700">
            상태
            <select className="mt-2 w-full rounded-xl border border-slate-300 bg-white px-4 py-3" defaultValue="todo">
              <option value="todo">할 일</option>
              <option value="in_progress">진행 중</option>
              <option value="done">완료</option>
            </select>
          </label>
          <label className="block text-sm font-medium text-slate-700">
            우선순위
            <select className="mt-2 w-full rounded-xl border border-slate-300 bg-white px-4 py-3" defaultValue="medium">
              <option value="low">낮음</option>
              <option value="medium">보통</option>
              <option value="high">높음</option>
            </select>
          </label>
        </div>
        <label className="block text-sm font-medium text-slate-700">
          마감일
          <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" type="date" />
        </label>
        <div className="flex justify-end gap-3">
          <Link className="rounded-xl border border-slate-300 px-4 py-3 font-semibold text-slate-700" to={`/projects/${id}`}>취소</Link>
          <button className="rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700" type="submit">저장</button>
        </div>
      </form>
    </main>
  )
}

export default TaskNewPage

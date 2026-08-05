import { Link, useParams } from "react-router"
import PageHeader from "../components/PageHeader"
import StatusBadge from "../components/StatusBadge"

function TaskDetailPage() {
  const { id } = useParams()

  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <PageHeader eyebrow={`Task ${id ?? ""}`} title="할 일 상세" action={<Link className="rounded-xl bg-slate-900 px-4 py-3 font-semibold text-white hover:bg-slate-700" to={`/tasks/${id}/edit`}>수정</Link>} />
      <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-wrap gap-2">
          <StatusBadge type="status" value="todo" />
          <StatusBadge type="priority" value="medium" />
        </div>
        <h2 className="mt-5 text-2xl font-bold text-slate-950">할 일 데이터 연결 예정</h2>
        <p className="mt-3 text-slate-500">Supabase 연결 후 실제 할 일의 상세 내용이 표시됩니다.</p>
      </article>
    </main>
  )
}

export default TaskDetailPage

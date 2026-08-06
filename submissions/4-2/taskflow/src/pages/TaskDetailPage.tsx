import { useEffect, useState } from "react"
import { Link, useNavigate, useParams } from "react-router"
import ErrorState from "../components/ErrorState"
import PageHeader from "../components/PageHeader"
import StatusBadge from "../components/StatusBadge"
import EmptyState from "../components/EmptyState"
import LoadingState from "../components/LoadingState"
import { getErrorMessage } from "../lib/errors"
import { deleteTask, getTaskById } from "../lib/taskApi"
import type { Task } from "../types/database"

function TaskDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [task, setTask] = useState<Task | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isDeleting, setIsDeleting] = useState(false)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!id) return
    const taskId = id
    let isMounted = true

    async function loadTask() {
      try {
        const taskData = await getTaskById(taskId)
        if (isMounted) setTask(taskData)
      } catch (requestError) {
        if (isMounted) setError(getErrorMessage(requestError))
      } finally {
        if (isMounted) setIsLoading(false)
      }
    }

    void loadTask()
    return () => {
      isMounted = false
    }
  }, [id])

  async function handleDelete() {
    if (!id || !window.confirm("이 할 일을 삭제할까요?")) return
    setIsDeleting(true)
    setError("")
    try {
      await deleteTask(id)
      navigate(task ? `/projects/${task.project_id}` : "/dashboard")
    } catch (requestError) {
      setError(getErrorMessage(requestError))
      setIsDeleting(false)
    }
  }

  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <PageHeader eyebrow="Task" title={task?.title ?? "할 일 상세"} action={task && <Link className="rounded-xl bg-slate-900 px-4 py-3 font-semibold text-white hover:bg-slate-700" to={`/tasks/${id}/edit`}>수정</Link>} />
      {error && <div className="mb-6"><ErrorState message={error} compact /></div>}
      {isLoading ? <LoadingState message="할 일을 불러오고 있습니다..." /> : task ? <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-wrap gap-2"><StatusBadge type="status" value={task.status} /><StatusBadge type="priority" value={task.priority} /></div>
        <h2 className="mt-5 text-2xl font-bold text-slate-950">{task.title}</h2>
        <p className="mt-3 whitespace-pre-wrap text-slate-500">{task.description || "상세 설명이 없습니다."}</p>
        <dl className="mt-8 grid gap-4 border-t border-slate-100 pt-5 text-sm sm:grid-cols-2"><div><dt className="text-slate-400">마감일</dt><dd className="mt-1 font-medium text-slate-700">{task.due_date || "설정하지 않음"}</dd></div><div><dt className="text-slate-400">프로젝트 ID</dt><dd className="mt-1 truncate font-medium text-slate-700">{task.project_id}</dd></div></dl>
        <div className="mt-8 flex justify-between"><Link className="text-sm font-semibold text-blue-600 hover:text-blue-700" to={`/projects/${task.project_id}`}>프로젝트로 돌아가기</Link><button className="text-sm font-semibold text-red-600 hover:text-red-700 disabled:opacity-50" type="button" onClick={() => void handleDelete()} disabled={isDeleting}>{isDeleting ? "삭제 중..." : "삭제"}</button></div>
      </article> : <EmptyState title="할 일을 찾을 수 없습니다." description="삭제되었거나 접근할 수 없는 할 일입니다." action={<Link className="inline-flex rounded-xl bg-slate-900 px-4 py-3 font-semibold text-white hover:bg-slate-700" to="/dashboard">대시보드로</Link>} />}
    </main>
  )
}

export default TaskDetailPage

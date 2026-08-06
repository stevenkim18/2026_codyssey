import { useEffect, useState } from "react"
import { Link, useNavigate, useParams } from "react-router"
import ErrorState from "../components/ErrorState"
import LoadingState from "../components/LoadingState"
import PageHeader from "../components/PageHeader"
import { useAuth } from "../contexts/useAuth"
import { getErrorMessage } from "../lib/errors"
import { getProjectById } from "../lib/projectApi"
import { createTask } from "../lib/taskApi"
import type { TaskPriority, TaskStatus } from "../types/database"

function TaskNewPage() {
  const { id } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [projectName, setProjectName] = useState("")
  const [isProjectLoading, setIsProjectLoading] = useState(true)
  const [projectError, setProjectError] = useState("")
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [status, setStatus] = useState<TaskStatus>("todo")
  const [priority, setPriority] = useState<TaskPriority>("medium")
  const [dueDate, setDueDate] = useState("")
  const [error, setError] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    if (!id) return
    const projectId = id
    let isMounted = true

    async function loadProject() {
      try {
        const project = await getProjectById(projectId)
        if (isMounted) setProjectName(project.name)
      } catch (requestError) {
        if (isMounted) setProjectError(getErrorMessage(requestError))
      } finally {
        if (isMounted) setIsProjectLoading(false)
      }
    }

    void loadProject()
    return () => {
      isMounted = false
    }
  }, [id])

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!id || !user) return
    setError("")
    if (!title.trim()) {
      setError("할 일 제목을 입력해주세요.")
      return
    }
    setIsSubmitting(true)

    try {
      await createTask(user.id, {
        project_id: id,
        title: title.trim(),
        description: description.trim() || null,
        status,
        priority,
        due_date: dueDate || null,
      })
      navigate(`/projects/${id}`)
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="mx-auto max-w-2xl px-6 py-10">
      <PageHeader eyebrow={projectName || "Project"} title="새 할 일" description="프로젝트에 새로운 할 일을 추가합니다." />
      {isProjectLoading ? <LoadingState message="프로젝트 정보를 불러오고 있습니다..." /> : projectError ? <ErrorState message={projectError} /> : <form className="space-y-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm" onSubmit={(event) => void handleSubmit(event)}>
        <label className="block text-sm font-medium text-slate-700">
          할 일 제목
          <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" required placeholder="예: React 라우팅 공부하기" value={title} onChange={(event) => setTitle(event.target.value)} />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          설명
          <textarea className="mt-2 min-h-32 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" placeholder="할 일에 대한 설명을 입력하세요." value={description} onChange={(event) => setDescription(event.target.value)} />
        </label>
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block text-sm font-medium text-slate-700">
            상태
            <select className="mt-2 w-full rounded-xl border border-slate-300 bg-white px-4 py-3" value={status} onChange={(event) => setStatus(event.target.value as TaskStatus)}>
              <option value="todo">할 일</option>
              <option value="in_progress">진행 중</option>
              <option value="done">완료</option>
            </select>
          </label>
          <label className="block text-sm font-medium text-slate-700">
            우선순위
            <select className="mt-2 w-full rounded-xl border border-slate-300 bg-white px-4 py-3" value={priority} onChange={(event) => setPriority(event.target.value as TaskPriority)}>
              <option value="low">낮음</option>
              <option value="medium">보통</option>
              <option value="high">높음</option>
            </select>
          </label>
        </div>
        <label className="block text-sm font-medium text-slate-700">
          마감일
          <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" type="date" value={dueDate} onChange={(event) => setDueDate(event.target.value)} />
        </label>
        {error && <ErrorState message={error} compact />}
        <div className="flex justify-end gap-3">
          <Link className="rounded-xl border border-slate-300 px-4 py-3 font-semibold text-slate-700" to={`/projects/${id}`}>취소</Link>
          <button className="rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60" type="submit" disabled={isSubmitting}>{isSubmitting ? "저장 중..." : "저장"}</button>
        </div>
      </form>}
    </main>
  )
}

export default TaskNewPage

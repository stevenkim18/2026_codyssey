import { useEffect, useState } from "react"
import { Link, useNavigate, useParams } from "react-router"
import ErrorState from "../components/ErrorState"
import PageHeader from "../components/PageHeader"
import EmptyState from "../components/EmptyState"
import LoadingState from "../components/LoadingState"
import TaskCard from "../components/TaskCard"
import { getErrorMessage } from "../lib/errors"
import { archiveProject, deleteProject, getProjectById } from "../lib/projectApi"
import { getTasksByProject } from "../lib/taskApi"
import type { Project, Task } from "../types/database"

function ProjectDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [project, setProject] = useState<Project | null>(null)
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isArchiving, setIsArchiving] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!id) return
    const projectId = id
    let isMounted = true

    async function loadProjectDetail() {
      try {
        const [projectData, taskData] = await Promise.all([getProjectById(projectId), getTasksByProject(projectId)])
        if (isMounted) {
          setProject(projectData)
          setTasks(taskData)
        }
      } catch (requestError) {
        if (isMounted) setError(getErrorMessage(requestError))
      } finally {
        if (isMounted) setIsLoading(false)
      }
    }

    void loadProjectDetail()
    return () => {
      isMounted = false
    }
  }, [id])

  async function handleDelete() {
    if (!id || !window.confirm("이 프로젝트와 포함된 할 일을 삭제할까요?")) return
    setIsDeleting(true)
    setError("")
    try {
      await deleteProject(id)
      navigate("/projects")
    } catch (requestError) {
      setError(getErrorMessage(requestError))
      setIsDeleting(false)
    }
  }

  async function handleArchive() {
    if (!id || !window.confirm("이 프로젝트를 보관할까요? 목록에서 숨겨집니다.")) return
    setIsArchiving(true)
    setError("")
    try {
      await archiveProject(id)
      navigate("/projects")
    } catch (requestError) {
      setError(getErrorMessage(requestError))
      setIsArchiving(false)
    }
  }

  const completedCount = tasks.filter((task) => task.status === "done").length
  const progress = tasks.length === 0 ? 0 : Math.round((completedCount / tasks.length) * 100)

  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <PageHeader
        eyebrow="Project"
        title={project?.name ?? "프로젝트 상세"}
        description={project?.description ?? "이 프로젝트에 포함된 할 일을 관리합니다."}
        action={<div className="flex flex-wrap gap-3"><Link className="rounded-xl border border-slate-300 px-4 py-3 font-semibold text-slate-700 hover:border-slate-400" to={`/projects/${id}/edit`}>프로젝트 수정</Link><Link className="rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700" to={`/projects/${id}/tasks/new`}>할 일 추가</Link></div>}
      />
      {error && <div className="mb-6"><ErrorState message={error} compact /></div>}
      {isLoading ? <LoadingState message="프로젝트를 불러오고 있습니다..." /> : project ? <>
        <section className="mb-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between text-sm"><span className="font-semibold text-slate-900">진행률</span><span className="text-slate-500">{completedCount}/{tasks.length} 완료</span></div>
          <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-blue-600 transition-all" style={{ width: `${progress}%` }} /></div>
          <div className="mt-5 flex flex-wrap items-center justify-between gap-3"><span className="text-sm text-slate-500">{progress}% 진행</span><div className="flex gap-4"><button className="text-sm font-semibold text-slate-500 hover:text-slate-700 disabled:opacity-50" type="button" onClick={() => void handleArchive()} disabled={isArchiving || isDeleting}>{isArchiving ? "보관 중..." : "프로젝트 보관"}</button><button className="text-sm font-semibold text-red-600 hover:text-red-700 disabled:opacity-50" type="button" onClick={() => void handleDelete()} disabled={isArchiving || isDeleting}>{isDeleting ? "삭제 중..." : "프로젝트 삭제"}</button></div></div>
        </section>
        {tasks.length === 0 ? <EmptyState title="아직 할 일이 없습니다." description="이 프로젝트에 첫 번째 할 일을 추가해보세요." action={<Link className="inline-flex rounded-xl bg-slate-900 px-4 py-3 font-semibold text-white hover:bg-slate-700" to={`/projects/${id}/tasks/new`}>할 일 추가</Link>} /> : <div className="grid gap-4 md:grid-cols-2">{tasks.map((task) => <TaskCard key={task.id} task={task} />)}</div>}
      </> : <EmptyState title="프로젝트를 찾을 수 없습니다." description="삭제되었거나 접근할 수 없는 프로젝트입니다." action={<Link className="inline-flex rounded-xl bg-slate-900 px-4 py-3 font-semibold text-white hover:bg-slate-700" to="/projects">프로젝트 목록으로</Link>} />}
    </main>
  )
}

export default ProjectDetailPage

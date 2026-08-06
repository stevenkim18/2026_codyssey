import { Link } from "react-router"
import EmptyState from "../components/EmptyState"
import ErrorState from "../components/ErrorState"
import LoadingState from "../components/LoadingState"
import PageHeader from "../components/PageHeader"
import ProjectCard from "../components/ProjectCard"
import { useAuth } from "../contexts/useAuth"
import { useProjects } from "../hooks/useProjects"

function ProjectListPage() {
  const { user } = useAuth()
  const { projects, tasks, isLoading, error, reload } = useProjects(user?.id)

  const taskCounts = tasks.reduce<Record<string, number>>((counts, task) => {
    counts[task.project_id] = (counts[task.project_id] ?? 0) + 1
    return counts
  }, {})

  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <PageHeader
        eyebrow="Projects"
        title="프로젝트"
        description="목표별로 할 일을 묶어 관리해보세요."
        action={<Link className="rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700" to="/projects/new">새 프로젝트</Link>}
      />
      {error && <div className="mb-6"><ErrorState message={error} onRetry={reload} /></div>}
      {isLoading ? (
        <LoadingState message="프로젝트를 불러오고 있습니다..." />
      ) : projects.length === 0 ? (
        <EmptyState
          title="아직 프로젝트가 없습니다."
          description="첫 번째 프로젝트를 만들고 해야 할 일을 정리해보세요."
          action={<Link className="inline-flex rounded-xl bg-slate-900 px-4 py-3 font-semibold text-white hover:bg-slate-700" to="/projects/new">프로젝트 만들기</Link>}
        />
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {projects.map((project) => <ProjectCard key={project.id} project={project} taskCount={taskCounts[project.id] ?? 0} />)}
        </div>
      )}
    </main>
  )
}

export default ProjectListPage

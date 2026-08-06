import { useState } from "react"
import { Link } from "react-router"
import EmptyState from "../components/EmptyState"
import ErrorState from "../components/ErrorState"
import LoadingState from "../components/LoadingState"
import PageHeader from "../components/PageHeader"
import TaskCard from "../components/TaskCard"
import { useAuth } from "../contexts/useAuth"
import { getErrorMessage } from "../lib/errors"
import { createDemoData, demoProjectNames } from "../lib/demoData"
import { useProjects } from "../hooks/useProjects"

function DashboardPage() {
  const { user } = useAuth()
  const { projects, tasks, isLoading, error: loadError, reload } = useProjects(user?.id)
  const [isSeeding, setIsSeeding] = useState(false)
  const [actionError, setActionError] = useState("")
  const [notice, setNotice] = useState("")

  const error = actionError || loadError

  const completedTaskCount = tasks.filter((task) => task.status === "done").length
  const recentTasks = tasks.slice(0, 4)
  const hasDemoData = projects.some((project) => demoProjectNames.includes(project.name))

  async function handleCreateDemoData() {
    if (!user) {
      setActionError("로그인 상태를 확인하지 못했습니다. 페이지를 새로고침해주세요.")
      return
    }

    if (hasDemoData) {
      setNotice("샘플 데이터가 이미 등록되어 있습니다.")
      return
    }
    setActionError("")
    setNotice("")
    setIsSeeding(true)

    try {
      const result = await createDemoData(user.id)
      setNotice(`샘플 프로젝트 ${result.projectCount}개와 할 일 ${result.taskCount}개를 추가했습니다.`)
      reload()
    } catch (requestError) {
      setActionError(getErrorMessage(requestError))
    } finally {
      setIsSeeding(false)
    }
  }

  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <PageHeader
        eyebrow="Overview"
        title="오늘의 작업을 확인하세요."
        description="프로젝트와 할 일의 진행 상황을 한눈에 확인하는 공간입니다."
        action={<div className="flex flex-wrap gap-3"><Link className="rounded-xl border border-slate-300 px-4 py-3 font-semibold text-slate-700 hover:border-slate-400" to="/projects/new">새 프로젝트</Link>{!isLoading && !hasDemoData && <button className="rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60" type="button" onClick={() => void handleCreateDemoData()} disabled={isSeeding}>{isSeeding ? "샘플 데이터 추가 중..." : "샘플 데이터 넣기"}</button>}</div>}
      />
      {error && <div className="mb-6"><ErrorState message={error} onRetry={loadError ? reload : undefined} /></div>}
      {notice && <p className="mb-6 rounded-xl bg-emerald-50 px-4 py-3 text-sm text-emerald-700" role="status">{notice}</p>}
      <div className="grid gap-4 sm:grid-cols-3">
        {[
          { label: "전체 프로젝트", value: projects.length },
          { label: "전체 할 일", value: tasks.length },
          { label: "완료한 할 일", value: completedTaskCount },
        ].map((stat) => (
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm" key={stat.label}>
            <p className="text-sm text-slate-500">{stat.label}</p>
            <p className="mt-3 text-3xl font-bold text-slate-950">{isLoading ? "-" : stat.value}</p>
          </div>
        ))}
      </div>
      <section className="mt-8">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-bold text-slate-950">최근 할 일</h2>
          <Link className="text-sm font-semibold text-blue-600 hover:text-blue-700" to="/projects">프로젝트 보기</Link>
        </div>
        {isLoading ? (
          <LoadingState />
        ) : recentTasks.length === 0 ? (
          <EmptyState
            title="아직 등록된 할 일이 없습니다."
            description="직접 프로젝트를 만들거나 샘플 데이터로 화면을 먼저 확인해보세요."
            action={!hasDemoData ? <button className="rounded-xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60" type="button" onClick={() => void handleCreateDemoData()} disabled={isSeeding}>{isSeeding ? "샘플 데이터 추가 중..." : "샘플 데이터 넣기"}</button> : <Link className="inline-flex rounded-xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white hover:bg-slate-700" to="/projects">프로젝트에서 할 일 추가하기</Link>}
          />
        ) : (
          <div className="grid gap-4 md:grid-cols-2">
            {recentTasks.map((task) => <TaskCard key={task.id} task={task} />)}
          </div>
        )}
      </section>
    </main>
  )
}

export default DashboardPage
